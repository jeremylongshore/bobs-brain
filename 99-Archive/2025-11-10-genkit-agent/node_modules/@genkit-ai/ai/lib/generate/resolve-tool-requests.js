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
var resolve_tool_requests_exports = {};
__export(resolve_tool_requests_exports, {
  assertValidToolNames: () => assertValidToolNames,
  resolveRestartedTools: () => resolveRestartedTools,
  resolveResumeOption: () => resolveResumeOption,
  resolveToolRequest: () => resolveToolRequest,
  resolveToolRequests: () => resolveToolRequests,
  toPendingOutput: () => toPendingOutput,
  toToolMap: () => toToolMap
});
module.exports = __toCommonJS(resolve_tool_requests_exports);
var import_core = require("@genkit-ai/core");
var import_logging = require("@genkit-ai/core/logging");
var import_prompt = require("../prompt.js");
var import_tool = require("../tool.js");
function toToolMap(tools) {
  assertValidToolNames(tools);
  const out = {};
  for (const tool of tools) {
    const name = tool.__action.name;
    const shortName = name.substring(name.lastIndexOf("/") + 1);
    out[shortName] = tool;
  }
  return out;
}
function assertValidToolNames(tools) {
  const nameMap = {};
  for (const tool of tools) {
    const name = tool.__action.name;
    const shortName = name.substring(name.lastIndexOf("/") + 1);
    if (nameMap[shortName]) {
      throw new import_core.GenkitError({
        status: "INVALID_ARGUMENT",
        message: `Cannot provide two tools with the same name: '${name}' and '${nameMap[shortName]}'`
      });
    }
    nameMap[shortName] = name;
  }
}
function toRunOptions(part) {
  const out = { metadata: part.metadata };
  if (part.metadata?.resumed) out.resumed = part.metadata.resumed;
  return out;
}
function toPendingOutput(part, response) {
  return {
    ...part,
    metadata: {
      ...part.metadata,
      pendingOutput: response.toolResponse.output
    }
  };
}
async function resolveToolRequest(rawRequest, part, toolMap, runOptions) {
  const tool = toolMap[part.toolRequest.name];
  if (!tool) {
    throw new import_core.GenkitError({
      status: "NOT_FOUND",
      message: `Tool ${part.toolRequest.name} not found`,
      detail: { request: rawRequest }
    });
  }
  if ((0, import_prompt.isPromptAction)(tool)) {
    const preamble = await tool(part.toolRequest.input);
    const response = {
      toolResponse: {
        name: part.toolRequest.name,
        ref: part.toolRequest.ref,
        output: `transferred to ${part.toolRequest.name}`
      }
    };
    return { preamble, response };
  }
  try {
    const output = await tool(part.toolRequest.input, toRunOptions(part));
    const response = (0, import_core.stripUndefinedProps)({
      toolResponse: {
        name: part.toolRequest.name,
        ref: part.toolRequest.ref,
        output
      }
    });
    return { response };
  } catch (e) {
    if (e instanceof import_tool.ToolInterruptError || // There's an inexplicable case when the above type check fails, only in tests.
    e.name === "ToolInterruptError") {
      const ie = e;
      import_logging.logger.debug(
        `tool '${toolMap[part.toolRequest?.name].__action.name}' triggered an interrupt${ie.metadata ? `: ${JSON.stringify(ie.metadata)}` : ""}`
      );
      const interrupt = {
        toolRequest: part.toolRequest,
        metadata: { ...part.metadata, interrupt: ie.metadata || true }
      };
      return { interrupt };
    }
    throw e;
  }
}
async function resolveToolRequests(registry, rawRequest, generatedMessage) {
  const toolMap = toToolMap(await (0, import_tool.resolveTools)(registry, rawRequest.tools));
  const responseParts = [];
  let hasInterrupts = false;
  let transferPreamble;
  const revisedModelMessage = {
    ...generatedMessage,
    content: [...generatedMessage.content]
  };
  await Promise.all(
    revisedModelMessage.content.map(async (part, i) => {
      if (!part.toolRequest) return;
      const { preamble, response, interrupt } = await resolveToolRequest(
        rawRequest,
        part,
        toolMap
      );
      if (preamble) {
        if (transferPreamble) {
          throw new import_core.GenkitError({
            status: "INVALID_ARGUMENT",
            message: `Model attempted to transfer to multiple prompt tools.`
          });
        }
        transferPreamble = preamble;
      }
      if (response) {
        responseParts.push(response);
        revisedModelMessage.content.splice(
          i,
          1,
          toPendingOutput(part, response)
        );
      }
      if (interrupt) {
        revisedModelMessage.content.splice(i, 1, interrupt);
        hasInterrupts = true;
      }
    })
  );
  if (hasInterrupts) {
    return { revisedModelMessage };
  }
  return {
    toolMessage: { role: "tool", content: responseParts },
    transferPreamble
  };
}
function findCorrespondingToolRequest(parts, part) {
  const name = part.toolRequest?.name || part.toolResponse?.name;
  const ref = part.toolRequest?.ref || part.toolResponse?.ref;
  return parts.find(
    (p) => p.toolRequest?.name === name && p.toolRequest?.ref === ref
  );
}
function findCorrespondingToolResponse(parts, part) {
  const name = part.toolRequest?.name || part.toolResponse?.name;
  const ref = part.toolRequest?.ref || part.toolResponse?.ref;
  return parts.find(
    (p) => p.toolResponse?.name === name && p.toolResponse?.ref === ref
  );
}
async function resolveResumedToolRequest(rawRequest, part, toolMap) {
  if (part.metadata?.pendingOutput) {
    const { pendingOutput, ...metadata } = part.metadata;
    const toolResponse = {
      toolResponse: {
        name: part.toolRequest.name,
        ref: part.toolRequest.ref,
        output: pendingOutput
      },
      metadata: { ...metadata, source: "pending" }
    };
    return (0, import_core.stripUndefinedProps)({
      toolResponse,
      toolRequest: { ...part, metadata }
    });
  }
  const providedResponse = findCorrespondingToolResponse(
    rawRequest.resume?.respond || [],
    part
  );
  if (providedResponse) {
    const toolResponse = providedResponse;
    const { interrupt, ...metadata } = part.metadata || {};
    return (0, import_core.stripUndefinedProps)({
      toolResponse,
      toolRequest: {
        ...part,
        metadata: { ...metadata, resolvedInterrupt: interrupt }
      }
    });
  }
  const restartRequest = findCorrespondingToolRequest(
    rawRequest.resume?.restart || [],
    part
  );
  if (restartRequest) {
    const { response, interrupt, preamble } = await resolveToolRequest(
      rawRequest,
      restartRequest,
      toolMap
    );
    if (preamble) {
      throw new import_core.GenkitError({
        status: "INTERNAL",
        message: `Prompt tool '${restartRequest.toolRequest.name}' executed inside 'restart' resolution. This should never happen.`
      });
    }
    if (interrupt) return { interrupt };
    if (response) {
      const toolResponse = response;
      const { interrupt: interrupt2, ...metadata } = part.metadata || {};
      return (0, import_core.stripUndefinedProps)({
        toolResponse,
        toolRequest: {
          ...part,
          metadata: { ...metadata, resolvedInterrupt: interrupt2 }
        }
      });
    }
  }
  throw new import_core.GenkitError({
    status: "INVALID_ARGUMENT",
    message: `Unresolved tool request '${part.toolRequest.name}${part.toolRequest.ref ? `#${part.toolRequest.ref}` : ""}' was not handled by the 'resume' argument. You must supply replies or restarts for all interrupted tool requests.'`
  });
}
async function resolveResumeOption(registry, rawRequest) {
  if (!rawRequest.resume) return { revisedRequest: rawRequest };
  const toolMap = toToolMap(await (0, import_tool.resolveTools)(registry, rawRequest.tools));
  const messages = rawRequest.messages;
  const lastMessage = messages.at(-1);
  if (!lastMessage || lastMessage.role !== "model" || !lastMessage.content.find((p) => p.toolRequest)) {
    throw new import_core.GenkitError({
      status: "FAILED_PRECONDITION",
      message: `Cannot 'resume' generation unless the previous message is a model message with at least one tool request.`
    });
  }
  const toolResponses = [];
  let interrupted = false;
  lastMessage.content = await Promise.all(
    lastMessage.content.map(async (part) => {
      if (!(0, import_tool.isToolRequest)(part)) return part;
      const resolved = await resolveResumedToolRequest(
        rawRequest,
        part,
        toolMap
      );
      if (resolved.interrupt) {
        interrupted = true;
        return resolved.interrupt;
      }
      toolResponses.push(resolved.toolResponse);
      return resolved.toolRequest;
    })
  );
  if (interrupted) {
    return {
      interruptedResponse: {
        finishReason: "interrupted",
        finishMessage: "One or more tools triggered interrupts while resuming generation. The model was not called.",
        message: lastMessage
      }
    };
  }
  const numToolRequests = lastMessage.content.filter(
    (p) => !!p.toolRequest
  ).length;
  if (toolResponses.length !== numToolRequests) {
    throw new import_core.GenkitError({
      status: "FAILED_PRECONDITION",
      message: `Expected ${numToolRequests} tool responses but resolved to ${toolResponses.length}.`,
      detail: { toolResponses, message: lastMessage }
    });
  }
  const toolMessage = {
    role: "tool",
    content: toolResponses,
    metadata: {
      resumed: rawRequest.resume.metadata || true
    }
  };
  return (0, import_core.stripUndefinedProps)({
    revisedRequest: {
      ...rawRequest,
      resume: void 0,
      messages: [...messages, toolMessage]
    },
    toolMessage
  });
}
async function resolveRestartedTools(registry, rawRequest) {
  const toolMap = toToolMap(await (0, import_tool.resolveTools)(registry, rawRequest.tools));
  const lastMessage = rawRequest.messages.at(-1);
  if (!lastMessage || lastMessage.role !== "model") return [];
  const restarts = lastMessage.content.filter(
    (p) => p.toolRequest && p.metadata?.resumed
  );
  return await Promise.all(
    restarts.map(async (p) => {
      const { response, interrupt } = await resolveToolRequest(
        rawRequest,
        p,
        toolMap
      );
      if (interrupt) return interrupt;
      return toPendingOutput(p, response);
    })
  );
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  assertValidToolNames,
  resolveRestartedTools,
  resolveResumeOption,
  resolveToolRequest,
  resolveToolRequests,
  toPendingOutput,
  toToolMap
});
//# sourceMappingURL=resolve-tool-requests.js.map