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
var generate_exports = {};
__export(generate_exports, {
  GenerateResponse: () => import_response.GenerateResponse,
  GenerateResponseChunk: () => import_chunk.GenerateResponseChunk,
  GenerationBlockedError: () => GenerationBlockedError,
  GenerationResponseError: () => GenerationResponseError,
  generate: () => generate,
  generateOperation: () => generateOperation,
  generateStream: () => generateStream,
  tagAsPreamble: () => tagAsPreamble,
  toGenerateActionOptions: () => toGenerateActionOptions,
  toGenerateRequest: () => toGenerateRequest
});
module.exports = __toCommonJS(generate_exports);
var import_core = require("@genkit-ai/core");
var import_async = require("@genkit-ai/core/async");
var import_registry = require("@genkit-ai/core/registry");
var import_schema = require("@genkit-ai/core/schema");
var import_formats = require("./formats/index.js");
var import_action = require("./generate/action.js");
var import_chunk = require("./generate/chunk.js");
var import_response = require("./generate/response.js");
var import_message = require("./message.js");
var import_model = require("./model.js");
var import_prompt = require("./prompt.js");
var import_resource = require("./resource.js");
var import_tool = require("./tool.js");
async function toGenerateRequest(registry, options) {
  const messages = [];
  if (options.system) {
    messages.push({
      role: "system",
      content: import_message.Message.parseContent(options.system)
    });
  }
  if (options.messages) {
    messages.push(...options.messages.map((m) => import_message.Message.parseData(m)));
  }
  if (options.prompt) {
    messages.push({
      role: "user",
      content: import_message.Message.parseContent(options.prompt)
    });
  }
  if (messages.length === 0) {
    throw new import_core.GenkitError({
      status: "INVALID_ARGUMENT",
      message: "at least one message is required in generate request"
    });
  }
  if (options.resume && !(messages.at(-1)?.role === "model" && messages.at(-1)?.content.find((p) => !!p.toolRequest))) {
    throw new import_core.GenkitError({
      status: "FAILED_PRECONDITION",
      message: `Last message must be a 'model' role with at least one tool request to 'resume' generation.`,
      detail: messages.at(-1)
    });
  }
  let tools;
  if (options.tools) {
    tools = await (0, import_tool.resolveTools)(registry, options.tools);
  }
  let resources;
  if (options.resources) {
    resources = await (0, import_resource.resolveResources)(registry, options.resources);
  }
  const resolvedSchema = (0, import_schema.toJsonSchema)({
    schema: options.output?.schema,
    jsonSchema: options.output?.jsonSchema
  });
  const resolvedFormat = await (0, import_formats.resolveFormat)(registry, options.output);
  const instructions = (0, import_formats.resolveInstructions)(
    resolvedFormat,
    resolvedSchema,
    options?.output?.instructions
  );
  const out = {
    messages: (0, import_action.shouldInjectFormatInstructions)(
      resolvedFormat?.config,
      options.output
    ) ? (0, import_formats.injectInstructions)(messages, instructions) : messages,
    config: options.config,
    docs: options.docs,
    tools: tools?.map(import_tool.toToolDefinition) || [],
    resources: resources?.map((a) => a.__action) || [],
    output: {
      ...resolvedFormat?.config || {},
      ...options.output,
      schema: resolvedSchema
    }
  };
  if (!out?.output?.schema) delete out?.output?.schema;
  return out;
}
class GenerationResponseError extends import_core.GenkitError {
  detail;
  constructor(response, message, status, detail) {
    super({
      status: status || "FAILED_PRECONDITION",
      message
    });
    this.detail = { response, ...detail };
  }
}
async function toolsToActionRefs(registry, toolOpt) {
  if (!toolOpt) return;
  const tools = [];
  for (const t of toolOpt) {
    if (typeof t === "string") {
      const names = await resolveFullToolNames(registry, t);
      tools.push(...names);
    } else if ((0, import_core.isAction)(t) || (0, import_tool.isDynamicTool)(t)) {
      tools.push(`/${t.__action.metadata?.type}/${t.__action.name}`);
    } else if ((0, import_prompt.isExecutablePrompt)(t)) {
      const promptToolAction = await t.asTool();
      tools.push(`/prompt/${promptToolAction.__action.name}`);
    } else {
      throw new Error(`Unable to determine type of tool: ${JSON.stringify(t)}`);
    }
  }
  return tools;
}
async function resourcesToActionRefs(registry, resOpt) {
  if (!resOpt) return;
  const resources = [];
  for (const r of resOpt) {
    if (typeof r === "string") {
      const names = await resolveFullResourceNames(registry, r);
      resources.push(...names);
    } else if ((0, import_core.isAction)(r)) {
      resources.push(`/resource/${r.__action.name}`);
    } else {
      throw new Error(`Unable to resolve resource: ${JSON.stringify(r)}`);
    }
  }
  return resources;
}
function messagesFromOptions(options) {
  const messages = [];
  if (options.system) {
    messages.push({
      role: "system",
      content: import_message.Message.parseContent(options.system)
    });
  }
  if (options.messages) {
    messages.push(...options.messages);
  }
  if (options.prompt) {
    messages.push({
      role: "user",
      content: import_message.Message.parseContent(options.prompt)
    });
  }
  if (messages.length === 0) {
    throw new import_core.GenkitError({
      status: "INVALID_ARGUMENT",
      message: "at least one message is required in generate request"
    });
  }
  return messages;
}
class GenerationBlockedError extends GenerationResponseError {
}
async function generate(registry, options) {
  const resolvedOptions = {
    ...await Promise.resolve(options)
  };
  const resolvedFormat = await (0, import_formats.resolveFormat)(registry, resolvedOptions.output);
  registry = maybeRegisterDynamicTools(registry, resolvedOptions);
  registry = maybeRegisterDynamicResources(registry, resolvedOptions);
  const params = await toGenerateActionOptions(registry, resolvedOptions);
  const tools = await toolsToActionRefs(registry, resolvedOptions.tools);
  const resources = await resourcesToActionRefs(
    registry,
    resolvedOptions.resources
  );
  const streamingCallback = stripNoop(
    resolvedOptions.onChunk ?? resolvedOptions.streamingCallback
  );
  const response = await (0, import_core.runWithContext)(
    resolvedOptions.context,
    () => (0, import_action.generateHelper)(registry, {
      rawRequest: params,
      middleware: resolvedOptions.use,
      abortSignal: resolvedOptions.abortSignal,
      streamingCallback
    })
  );
  const request = await toGenerateRequest(registry, {
    ...resolvedOptions,
    tools,
    resources
  });
  return new import_response.GenerateResponse(response, {
    request: response.request ?? request,
    parser: resolvedFormat?.handler(request.output?.schema).parseMessage
  });
}
async function generateOperation(registry, options) {
  (0, import_core.assertUnstable)(registry, "beta", "generateOperation is a beta feature.");
  options = await options;
  const resolvedModel = await (0, import_model.resolveModel)(registry, options.model);
  if (!resolvedModel.modelAction.__action.metadata?.model.supports?.longRunning) {
    throw new import_core.GenkitError({
      status: "INVALID_ARGUMENT",
      message: `Model '${resolvedModel.modelAction.__action.name}' does not support long running operations.`
    });
  }
  const { operation } = await generate(registry, options);
  if (!operation) {
    throw new import_core.GenkitError({
      status: "FAILED_PRECONDITION",
      message: `Model '${resolvedModel.modelAction.__action.name}' did not return an operation.`
    });
  }
  return operation;
}
function maybeRegisterDynamicTools(registry, options) {
  let hasDynamicTools = false;
  options?.tools?.forEach((t) => {
    if ((0, import_tool.isDynamicTool)(t)) {
      if (!hasDynamicTools) {
        hasDynamicTools = true;
        registry = import_registry.Registry.withParent(registry);
      }
      registry.registerAction("tool", t);
    }
  });
  return registry;
}
function maybeRegisterDynamicResources(registry, options) {
  let hasDynamicResources = false;
  options?.resources?.forEach((r) => {
    if ((0, import_resource.isDynamicResourceAction)(r)) {
      if (!hasDynamicResources) {
        hasDynamicResources = true;
        registry = import_registry.Registry.withParent(registry);
      }
      registry.registerAction("resource", r);
    }
  });
  return registry;
}
async function toGenerateActionOptions(registry, options) {
  const resolvedModel = await (0, import_model.resolveModel)(registry, options.model);
  const tools = await toolsToActionRefs(registry, options.tools);
  const resources = await resourcesToActionRefs(registry, options.resources);
  const messages = messagesFromOptions(options);
  const resolvedSchema = (0, import_schema.toJsonSchema)({
    schema: options.output?.schema,
    jsonSchema: options.output?.jsonSchema
  });
  if ((options.output?.schema || options.output?.jsonSchema) && !options.output?.format) {
    options.output.format = "json";
  }
  const params = {
    model: resolvedModel.modelAction.__action.name,
    docs: options.docs,
    messages,
    tools,
    resources,
    toolChoice: options.toolChoice,
    config: {
      version: resolvedModel.version,
      ...stripUndefinedOptions(resolvedModel.config),
      ...stripUndefinedOptions(options.config)
    },
    output: options.output && {
      ...options.output,
      format: options.output.format,
      jsonSchema: resolvedSchema
    },
    // coerce reply and restart into arrays for the action schema
    resume: options.resume && {
      respond: [options.resume.respond || []].flat(),
      restart: [options.resume.restart || []].flat(),
      metadata: options.resume.metadata
    },
    returnToolRequests: options.returnToolRequests,
    maxTurns: options.maxTurns,
    stepName: options.stepName
  };
  if (Object.keys(params.config).length === 0 && !options.config) {
    delete params.config;
  }
  return params;
}
function stripNoop(callback) {
  if (callback === import_core.sentinelNoopStreamingCallback) {
    return void 0;
  }
  return callback;
}
function stripUndefinedOptions(input) {
  if (!input) return input;
  const copy = { ...input };
  Object.keys(input).forEach((key) => {
    if (copy[key] === void 0) {
      delete copy[key];
    }
  });
  return copy;
}
async function resolveFullToolNames(registry, name) {
  let names;
  const parts = name.split(":");
  if (parts.length > 1) {
    names = await registry.resolveActionNames(
      `/dynamic-action-provider/${name}`
    );
    if (names.length) {
      return names;
    }
  }
  if (await registry.lookupAction(`/tool/${name}`)) {
    return [`/tool/${name}`];
  }
  if (await registry.lookupAction(`/prompt/${name}`)) {
    return [`/prompt/${name}`];
  }
  throw new Error(`Unable to resolve tool: ${name}`);
}
async function resolveFullResourceNames(registry, name) {
  let names;
  const parts = name.split(":");
  if (parts.length > 1) {
    names = await registry.resolveActionNames(
      `/dynamic-action-provider/${name}`
    );
    if (names.length) {
      return names;
    }
  }
  if (await registry.lookupAction(`/resource/${name}`)) {
    return [`/resource/${name}`];
  }
  throw new Error(`Unable to resolve resource: ${name}`);
}
function generateStream(registry, options) {
  const channel = new import_async.Channel();
  const generated = Promise.resolve(options).then(
    (resolvedOptions) => generate(registry, {
      ...resolvedOptions,
      onChunk: (chunk) => channel.send(chunk)
    })
  );
  generated.then(
    () => channel.close(),
    (err) => channel.error(err)
  );
  return {
    response: generated,
    stream: channel
  };
}
function tagAsPreamble(msgs) {
  if (!msgs) {
    return void 0;
  }
  return msgs.map((m) => ({
    ...m,
    metadata: {
      ...m.metadata,
      preamble: true
    }
  }));
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  GenerateResponse,
  GenerateResponseChunk,
  GenerationBlockedError,
  GenerationResponseError,
  generate,
  generateOperation,
  generateStream,
  tagAsPreamble,
  toGenerateActionOptions,
  toGenerateRequest
});
//# sourceMappingURL=generate.js.map