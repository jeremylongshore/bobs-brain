"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);
var action_exports = {};
__export(action_exports, {
  defineGenerateAction: () => defineGenerateAction,
  generateHelper: () => generateHelper,
  inferRoleFromParts: () => inferRoleFromParts,
  shouldInjectFormatInstructions: () => shouldInjectFormatInstructions
});
module.exports = __toCommonJS(action_exports);
var import_core = require("@genkit-ai/core");
var import_logging = require("@genkit-ai/core/logging");
var import_tracing = require("@genkit-ai/core/tracing");
var import_formats = require("../formats/index.js");
var import_generate = require("../generate.js");
var import_chunk = require("../generate/chunk.js");
var import_model = require("../model.js");
var import_resource = require("../resource.js");
var import_tool = require("../tool.js");
var import_resolve_tool_requests = require("./resolve-tool-requests.js");
function defineGenerateAction(registry) {
  return (0, import_core.defineAction)(
    registry,
    {
      actionType: "util",
      name: "generate",
      inputSchema: import_model.GenerateActionOptionsSchema,
      outputSchema: import_model.GenerateResponseSchema,
      streamSchema: import_model.GenerateResponseChunkSchema
    },
    async (request, { streamingRequested, sendChunk }) => {
      const generateFn = (sendChunk2) => generate(registry, {
        rawRequest: request,
        currentTurn: 0,
        messageIndex: 0,
        // Generate util action does not support middleware. Maybe when we add named/registered middleware....
        middleware: [],
        streamingCallback: sendChunk2
      });
      return streamingRequested ? generateFn(
        (c) => sendChunk(c.toJSON ? c.toJSON() : c)
      ) : generateFn();
    }
  );
}
async function generateHelper(registry, options) {
  const currentTurn = options.currentTurn ?? 0;
  const messageIndex = options.messageIndex ?? 0;
  return await (0, import_tracing.runInNewSpan)(
    registry,
    {
      metadata: {
        name: options.rawRequest.stepName || "generate"
      },
      labels: {
        [import_tracing.SPAN_TYPE_ATTR]: "util"
      }
    },
    async (metadata) => {
      metadata.name = options.rawRequest.stepName || "generate";
      metadata.input = options.rawRequest;
      const output = await generate(registry, {
        rawRequest: options.rawRequest,
        middleware: options.middleware,
        currentTurn,
        messageIndex,
        abortSignal: options.abortSignal,
        streamingCallback: options.streamingCallback
      });
      metadata.output = JSON.stringify(output);
      return output;
    }
  );
}
async function resolveParameters(registry, request) {
  const [model, tools, resources, format] = await Promise.all([
    (0, import_model.resolveModel)(registry, request.model, { warnDeprecated: true }).then(
      (r) => r.modelAction
    ),
    (0, import_tool.resolveTools)(registry, request.tools),
    (0, import_resource.resolveResources)(registry, request.resources),
    (0, import_formats.resolveFormat)(registry, request.output)
  ]);
  return { model, tools, resources, format };
}
function applyFormat(rawRequest, resolvedFormat) {
  const outRequest = { ...rawRequest };
  if (rawRequest.output?.jsonSchema && !rawRequest.output?.format) {
    outRequest.output = { ...rawRequest.output, format: "json" };
  }
  const instructions = (0, import_formats.resolveInstructions)(
    resolvedFormat,
    outRequest.output?.jsonSchema,
    outRequest?.output?.instructions
  );
  if (resolvedFormat) {
    if (shouldInjectFormatInstructions(resolvedFormat.config, rawRequest?.output)) {
      outRequest.messages = (0, import_formats.injectInstructions)(
        outRequest.messages,
        instructions
      );
    }
    outRequest.output = {
      // use output config from the format
      ...resolvedFormat.config,
      // if anything is set explicitly, use that
      ...outRequest.output
    };
  }
  return outRequest;
}
function shouldInjectFormatInstructions(formatConfig, rawRequestConfig) {
  return formatConfig?.defaultInstructions !== false || rawRequestConfig?.instructions;
}
function applyTransferPreamble(rawRequest, transferPreamble) {
  if (!transferPreamble) {
    return rawRequest;
  }
  return (0, import_core.stripUndefinedProps)({
    ...rawRequest,
    messages: [
      ...(0, import_generate.tagAsPreamble)(transferPreamble.messages),
      ...rawRequest.messages.filter((m) => !m.metadata?.preamble)
    ],
    toolChoice: transferPreamble.toolChoice || rawRequest.toolChoice,
    tools: transferPreamble.tools || rawRequest.tools,
    config: transferPreamble.config || rawRequest.config
  });
}
async function generate(registry, {
  rawRequest,
  middleware,
  currentTurn,
  messageIndex,
  abortSignal,
  streamingCallback
}) {
  const { model, tools, resources, format } = await resolveParameters(
    registry,
    rawRequest
  );
  rawRequest = applyFormat(rawRequest, format);
  rawRequest = await applyResources(registry, rawRequest, resources);
  await (0, import_resolve_tool_requests.assertValidToolNames)(tools);
  const {
    revisedRequest,
    interruptedResponse,
    toolMessage: resumedToolMessage
  } = await (0, import_resolve_tool_requests.resolveResumeOption)(registry, rawRequest);
  if (interruptedResponse) {
    throw new import_core.GenkitError({
      status: "FAILED_PRECONDITION",
      message: "One or more tools triggered an interrupt during a restarted execution.",
      detail: { message: interruptedResponse.message }
    });
  }
  rawRequest = revisedRequest;
  const request = await actionToGenerateRequest(
    rawRequest,
    tools,
    format,
    model
  );
  const previousChunks = [];
  let chunkRole = "model";
  const makeChunk = (role, chunk) => {
    if (role !== chunkRole && previousChunks.length) messageIndex++;
    chunkRole = role;
    const prevToSend = [...previousChunks];
    previousChunks.push(chunk);
    return new import_chunk.GenerateResponseChunk(chunk, {
      index: messageIndex,
      role,
      previousChunks: prevToSend,
      parser: format?.handler(request.output?.schema).parseChunk
    });
  };
  if (resumedToolMessage && streamingCallback) {
    streamingCallback(makeChunk("tool", resumedToolMessage));
  }
  var response;
  const dispatch = async (index, req) => {
    if (!middleware || index === middleware.length) {
      return await model(req, {
        abortSignal,
        onChunk: streamingCallback && ((chunk) => streamingCallback && streamingCallback(makeChunk("model", chunk)))
      });
    }
    const currentMiddleware = middleware[index];
    return currentMiddleware(
      req,
      async (modifiedReq) => dispatch(index + 1, modifiedReq || req)
    );
  };
  const modelResponse = await dispatch(0, request);
  if (model.__action.actionType === "background-model") {
    response = new import_generate.GenerateResponse(
      { operation: modelResponse },
      {
        request,
        parser: format?.handler(request.output?.schema).parseMessage
      }
    );
  } else {
    response = new import_generate.GenerateResponse(modelResponse, {
      request,
      parser: format?.handler(request.output?.schema).parseMessage
    });
  }
  if (model.__action.actionType === "background-model") {
    return response.toJSON();
  }
  response.assertValid();
  const generatedMessage = response.message;
  const toolRequests = generatedMessage.content.filter(
    (part) => !!part.toolRequest
  );
  if (rawRequest.returnToolRequests || toolRequests.length === 0) {
    if (toolRequests.length === 0) response.assertValidSchema(request);
    return response.toJSON();
  }
  const maxIterations = rawRequest.maxTurns ?? 5;
  if (currentTurn + 1 > maxIterations) {
    throw new import_generate.GenerationResponseError(
      response,
      `Exceeded maximum tool call iterations (${maxIterations})`,
      "ABORTED",
      { request }
    );
  }
  const { revisedModelMessage, toolMessage, transferPreamble } = await (0, import_resolve_tool_requests.resolveToolRequests)(registry, rawRequest, generatedMessage);
  if (revisedModelMessage) {
    return {
      ...response.toJSON(),
      finishReason: "interrupted",
      finishMessage: "One or more tool calls resulted in interrupts.",
      message: revisedModelMessage
    };
  }
  streamingCallback?.(
    makeChunk("tool", {
      content: toolMessage.content
    })
  );
  let nextRequest = {
    ...rawRequest,
    messages: [...rawRequest.messages, generatedMessage.toJSON(), toolMessage]
  };
  nextRequest = applyTransferPreamble(nextRequest, transferPreamble);
  return await generateHelper(registry, {
    rawRequest: nextRequest,
    middleware,
    currentTurn: currentTurn + 1,
    messageIndex: messageIndex + 1,
    streamingCallback,
    abortSignal
  });
}
async function actionToGenerateRequest(options, resolvedTools, resolvedFormat, model) {
  const modelInfo = model.__action.metadata?.model;
  if ((options.tools?.length ?? 0) > 0 && modelInfo?.supports && !modelInfo?.supports?.tools) {
    import_logging.logger.warn(
      `The model '${model.__action.name}' does not support tools (you set: ${options.tools?.length} tools). The model may not behave the way you expect.`
    );
  }
  if (options.toolChoice && modelInfo?.supports && !modelInfo?.supports?.toolChoice) {
    import_logging.logger.warn(
      `The model '${model.__action.name}' does not support the 'toolChoice' option (you set: ${options.toolChoice}). The model may not behave the way you expect.`
    );
  }
  const out = {
    messages: options.messages,
    config: options.config,
    docs: options.docs,
    tools: resolvedTools?.map(import_tool.toToolDefinition) || [],
    output: (0, import_core.stripUndefinedProps)({
      constrained: options.output?.constrained,
      contentType: options.output?.contentType,
      format: options.output?.format,
      schema: options.output?.jsonSchema
    })
  };
  if (options.toolChoice) {
    out.toolChoice = options.toolChoice;
  }
  if (out.output && !out.output.schema) delete out.output.schema;
  return out;
}
function inferRoleFromParts(parts) {
  const uniqueRoles = /* @__PURE__ */ new Set();
  for (const part of parts) {
    const role = getRoleFromPart(part);
    uniqueRoles.add(role);
    if (uniqueRoles.size > 1) {
      throw new Error("Contents contain mixed roles");
    }
  }
  return Array.from(uniqueRoles)[0];
}
function getRoleFromPart(part) {
  if (part.toolRequest !== void 0) return "model";
  if (part.toolResponse !== void 0) return "tool";
  if (part.text !== void 0) return "user";
  if (part.media !== void 0) return "user";
  if (part.data !== void 0) return "user";
  throw new Error("No recognized fields in content");
}
async function applyResources(registry, rawRequest, resources) {
  if (!rawRequest.messages.find((m) => !!m.content.find((c) => c.resource))) {
    return rawRequest;
  }
  const updatedMessages = [];
  for (const m of rawRequest.messages) {
    if (!m.content.find((c) => c.resource)) {
      updatedMessages.push(m);
      continue;
    }
    const updatedContent = [];
    for (const p of m.content) {
      if (!p.resource) {
        updatedContent.push(p);
        continue;
      }
      const resource = await (0, import_resource.findMatchingResource)(
        registry,
        resources,
        p.resource
      );
      if (!resource) {
        throw new import_core.GenkitError({
          status: "NOT_FOUND",
          message: `failed to find matching resource for ${p.resource.uri}`
        });
      }
      const resourceParts = await resource(p.resource);
      updatedContent.push(...resourceParts.content);
    }
    updatedMessages.push({
      ...m,
      content: updatedContent
    });
  }
  return {
    ...rawRequest,
    messages: updatedMessages
  };
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  defineGenerateAction,
  generateHelper,
  inferRoleFromParts,
  shouldInjectFormatInstructions
});
//# sourceMappingURL=action.js.map