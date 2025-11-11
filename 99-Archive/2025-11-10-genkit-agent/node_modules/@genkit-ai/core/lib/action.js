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
  StatusCodes: () => import_statusTypes.StatusCodes,
  StatusSchema: () => import_statusTypes.StatusSchema,
  action: () => action,
  actionWithMiddleware: () => actionWithMiddleware,
  defineAction: () => defineAction,
  defineActionAsync: () => defineActionAsync,
  getStreamingCallback: () => getStreamingCallback,
  isAction: () => isAction,
  isInRuntimeContext: () => isInRuntimeContext,
  runInActionRuntimeContext: () => runInActionRuntimeContext,
  runOutsideActionRuntimeContext: () => runOutsideActionRuntimeContext,
  runWithStreamingCallback: () => runWithStreamingCallback,
  sentinelNoopStreamingCallback: () => sentinelNoopStreamingCallback
});
module.exports = __toCommonJS(action_exports);
var import_async_context = require("./async-context.js");
var import_async = require("./async.js");
var import_context = require("./context.js");
var import_schema = require("./schema.js");
var import_tracing = require("./tracing.js");
var import_statusTypes = require("./statusTypes.js");
const makeNoopAbortSignal = () => new AbortController().signal;
function actionWithMiddleware(action2, middleware) {
  const wrapped = async (req, options) => {
    return (await wrapped.run(req, options)).result;
  };
  wrapped.__action = action2.__action;
  wrapped.run = async (req, options) => {
    let telemetry;
    const dispatch = async (index, req2, opts) => {
      if (index === middleware.length) {
        const result = await action2.run(req2, opts);
        telemetry = result.telemetry;
        return result.result;
      }
      const currentMiddleware = middleware[index];
      if (currentMiddleware.length === 3) {
        return currentMiddleware(
          req2,
          opts,
          async (modifiedReq, modifiedOptions) => dispatch(index + 1, modifiedReq || req2, modifiedOptions || opts)
        );
      } else if (currentMiddleware.length === 2) {
        return currentMiddleware(
          req2,
          async (modifiedReq) => dispatch(index + 1, modifiedReq || req2, opts)
        );
      } else {
        throw new Error("unspported middleware function shape");
      }
    };
    wrapped.stream = action2.stream;
    return { result: await dispatch(0, req, options), telemetry };
  };
  return wrapped;
}
function action(config, fn) {
  const actionName = typeof config.name === "string" ? config.name : `${config.name.pluginId}/${config.name.actionId}`;
  const actionMetadata = {
    name: actionName,
    description: config.description,
    inputSchema: config.inputSchema,
    inputJsonSchema: config.inputJsonSchema,
    outputSchema: config.outputSchema,
    outputJsonSchema: config.outputJsonSchema,
    streamSchema: config.streamSchema,
    metadata: config.metadata,
    actionType: config.actionType
  };
  const actionFn = async (input, options) => {
    return (await actionFn.run(input, options)).result;
  };
  actionFn.__action = { ...actionMetadata };
  actionFn.run = async (input, options) => {
    input = (0, import_schema.parseSchema)(input, {
      schema: config.inputSchema,
      jsonSchema: config.inputJsonSchema
    });
    let traceId;
    let spanId;
    let output = await (0, import_tracing.runInNewSpan)(
      {
        metadata: {
          name: actionName
        },
        labels: {
          [import_tracing.SPAN_TYPE_ATTR]: "action",
          "genkit:metadata:subtype": config.actionType,
          ...options?.telemetryLabels
        }
      },
      async (metadata, span) => {
        (0, import_tracing.setCustomMetadataAttributes)({
          subtype: config.actionType
        });
        if (options?.context) {
          (0, import_tracing.setCustomMetadataAttributes)({
            context: JSON.stringify(options.context)
          });
        }
        traceId = span.spanContext().traceId;
        spanId = span.spanContext().spanId;
        metadata.name = actionName;
        metadata.input = input;
        try {
          const actFn = () => fn(input, {
            ...options,
            // Context can either be explicitly set, or inherited from the parent action.
            context: {
              ...actionFn.__registry?.context,
              ...options?.context ?? (0, import_context.getContext)()
            },
            streamingRequested: !!options?.onChunk && options.onChunk !== sentinelNoopStreamingCallback,
            sendChunk: options?.onChunk ?? sentinelNoopStreamingCallback,
            trace: {
              traceId,
              spanId
            },
            registry: actionFn.__registry,
            abortSignal: options?.abortSignal ?? makeNoopAbortSignal()
          });
          const output2 = await (0, import_context.runWithContext)(options?.context, actFn);
          metadata.output = JSON.stringify(output2);
          return output2;
        } catch (err) {
          if (typeof err === "object") {
            err.traceId = traceId;
          }
          throw err;
        }
      }
    );
    output = (0, import_schema.parseSchema)(output, {
      schema: config.outputSchema,
      jsonSchema: config.outputJsonSchema
    });
    return {
      result: output,
      telemetry: {
        traceId,
        spanId
      }
    };
  };
  actionFn.stream = (input, opts) => {
    let chunkStreamController;
    const chunkStream = new ReadableStream({
      start(controller) {
        chunkStreamController = controller;
      },
      pull() {
      },
      cancel() {
      }
    });
    const invocationPromise = actionFn.run(config.inputSchema ? config.inputSchema.parse(input) : input, {
      onChunk: (chunk) => {
        chunkStreamController.enqueue(chunk);
      },
      context: {
        ...actionFn.__registry?.context,
        ...opts?.context ?? (0, import_context.getContext)()
      },
      abortSignal: opts?.abortSignal,
      telemetryLabels: opts?.telemetryLabels
    }).then((s) => s.result).finally(() => {
      chunkStreamController.close();
    });
    return {
      output: invocationPromise,
      stream: async function* () {
        const reader = chunkStream.getReader();
        while (true) {
          const chunk = await reader.read();
          if (chunk.value) {
            yield chunk.value;
          }
          if (chunk.done) {
            break;
          }
        }
        return await invocationPromise;
      }()
    };
  };
  if (config.use) {
    return actionWithMiddleware(actionFn, config.use);
  }
  return actionFn;
}
function isAction(a) {
  return typeof a === "function" && "__action" in a;
}
function defineAction(registry, config, fn) {
  if (isInRuntimeContext()) {
    throw new Error(
      "Cannot define new actions at runtime.\nSee: https://github.com/firebase/genkit/blob/main/docs/errors/no_new_actions_at_runtime.md"
    );
  }
  const act = action(config, async (i, options) => {
    await registry.initializeAllPlugins();
    return await runInActionRuntimeContext(() => fn(i, options));
  });
  act.__action.actionType = config.actionType;
  registry.registerAction(config.actionType, act);
  return act;
}
function defineActionAsync(registry, actionType, name, config, onInit) {
  const actionName = typeof name === "string" ? name : `${name.pluginId}/${name.actionId}`;
  const actionPromise = (0, import_async.lazy)(
    () => config.then((resolvedConfig) => {
      const act = action(
        resolvedConfig,
        async (i, options) => {
          await registry.initializeAllPlugins();
          return await runInActionRuntimeContext(
            () => resolvedConfig.fn(i, options)
          );
        }
      );
      act.__action.actionType = actionType;
      onInit?.(act);
      return act;
    })
  );
  registry.registerActionAsync(actionType, actionName, actionPromise);
  return actionPromise;
}
const streamingAlsKey = "core.action.streamingCallback";
const sentinelNoopStreamingCallback = () => null;
function runWithStreamingCallback(streamingCallback, fn) {
  return (0, import_async_context.getAsyncContext)().run(
    streamingAlsKey,
    streamingCallback || sentinelNoopStreamingCallback,
    fn
  );
}
function getStreamingCallback() {
  const cb = (0, import_async_context.getAsyncContext)().getStore(streamingAlsKey);
  if (cb === sentinelNoopStreamingCallback) {
    return void 0;
  }
  return cb;
}
const runtimeContextAslKey = "core.action.runtimeContext";
function isInRuntimeContext() {
  return (0, import_async_context.getAsyncContext)().getStore(runtimeContextAslKey) === "runtime";
}
function runInActionRuntimeContext(fn) {
  return (0, import_async_context.getAsyncContext)().run(runtimeContextAslKey, "runtime", fn);
}
function runOutsideActionRuntimeContext(fn) {
  return (0, import_async_context.getAsyncContext)().run(runtimeContextAslKey, "outside", fn);
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  StatusCodes,
  StatusSchema,
  action,
  actionWithMiddleware,
  defineAction,
  defineActionAsync,
  getStreamingCallback,
  isAction,
  isInRuntimeContext,
  runInActionRuntimeContext,
  runOutsideActionRuntimeContext,
  runWithStreamingCallback,
  sentinelNoopStreamingCallback
});
//# sourceMappingURL=action.js.map