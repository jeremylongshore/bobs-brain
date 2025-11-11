import { getAsyncContext } from "./async-context.js";
import { lazy } from "./async.js";
import { getContext, runWithContext } from "./context.js";
import { parseSchema } from "./schema.js";
import {
  SPAN_TYPE_ATTR,
  runInNewSpan,
  setCustomMetadataAttributes
} from "./tracing.js";
import { StatusCodes, StatusSchema } from "./statusTypes.js";
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
    input = parseSchema(input, {
      schema: config.inputSchema,
      jsonSchema: config.inputJsonSchema
    });
    let traceId;
    let spanId;
    let output = await runInNewSpan(
      {
        metadata: {
          name: actionName
        },
        labels: {
          [SPAN_TYPE_ATTR]: "action",
          "genkit:metadata:subtype": config.actionType,
          ...options?.telemetryLabels
        }
      },
      async (metadata, span) => {
        setCustomMetadataAttributes({
          subtype: config.actionType
        });
        if (options?.context) {
          setCustomMetadataAttributes({
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
              ...options?.context ?? getContext()
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
          const output2 = await runWithContext(options?.context, actFn);
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
    output = parseSchema(output, {
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
        ...opts?.context ?? getContext()
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
  const actionPromise = lazy(
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
  return getAsyncContext().run(
    streamingAlsKey,
    streamingCallback || sentinelNoopStreamingCallback,
    fn
  );
}
function getStreamingCallback() {
  const cb = getAsyncContext().getStore(streamingAlsKey);
  if (cb === sentinelNoopStreamingCallback) {
    return void 0;
  }
  return cb;
}
const runtimeContextAslKey = "core.action.runtimeContext";
function isInRuntimeContext() {
  return getAsyncContext().getStore(runtimeContextAslKey) === "runtime";
}
function runInActionRuntimeContext(fn) {
  return getAsyncContext().run(runtimeContextAslKey, "runtime", fn);
}
function runOutsideActionRuntimeContext(fn) {
  return getAsyncContext().run(runtimeContextAslKey, "outside", fn);
}
export {
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
};
//# sourceMappingURL=action.mjs.map