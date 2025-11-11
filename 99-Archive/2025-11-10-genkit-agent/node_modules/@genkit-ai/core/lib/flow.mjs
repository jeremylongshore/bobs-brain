import { action } from "./action.js";
import { SPAN_TYPE_ATTR, runInNewSpan } from "./tracing.js";
function flow(config, fn) {
  const resolvedConfig = typeof config === "string" ? { name: config } : config;
  return flowAction(resolvedConfig, fn);
}
function defineFlow(registry, config, fn) {
  const f = flow(config, fn);
  registry.registerAction("flow", f);
  return f;
}
function flowAction(config, fn) {
  return action(
    {
      actionType: "flow",
      name: config.name,
      inputSchema: config.inputSchema,
      outputSchema: config.outputSchema,
      streamSchema: config.streamSchema,
      metadata: config.metadata
    },
    async (input, { sendChunk, context, trace, abortSignal, streamingRequested }) => {
      const ctx = sendChunk;
      ctx.sendChunk = sendChunk;
      ctx.context = context;
      ctx.trace = trace;
      ctx.abortSignal = abortSignal;
      ctx.streamingRequested = streamingRequested;
      return fn(input, ctx);
    }
  );
}
function run(name, funcOrInput, fnOrRegistry, _) {
  let func;
  let input;
  let hasInput = false;
  if (typeof funcOrInput === "function") {
    func = funcOrInput;
  } else {
    input = funcOrInput;
    hasInput = true;
  }
  if (typeof fnOrRegistry === "function") {
    func = fnOrRegistry;
  }
  if (!func) {
    throw new Error("unable to resolve run function");
  }
  return runInNewSpan(
    {
      metadata: { name },
      labels: {
        [SPAN_TYPE_ATTR]: "flowStep"
      }
    },
    async (meta) => {
      meta.input = input;
      const output = hasInput ? await func(input) : await func();
      meta.output = JSON.stringify(output);
      return output;
    }
  );
}
export {
  defineFlow,
  flow,
  run
};
//# sourceMappingURL=flow.mjs.map