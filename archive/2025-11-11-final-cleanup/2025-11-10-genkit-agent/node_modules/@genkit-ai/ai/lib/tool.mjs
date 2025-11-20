import {
  action,
  assertUnstable,
  defineAction,
  isAction,
  stripUndefinedProps,
  z
} from "@genkit-ai/core";
import { parseSchema, toJsonSchema } from "@genkit-ai/core/schema";
import { setCustomMetadataAttributes } from "@genkit-ai/core/tracing";
import { isExecutablePrompt } from "./prompt.js";
function asTool(registry, action2) {
  if (action2.__action?.metadata?.type === "tool") {
    return action2;
  }
  const fn = (input) => {
    setCustomMetadataAttributes({ subtype: "tool" });
    return action2(input);
  };
  fn.__action = {
    ...action2.__action,
    metadata: { ...action2.__action.metadata, type: "tool" }
  };
  return fn;
}
async function resolveTools(registry, tools) {
  if (!tools || tools.length === 0) {
    return [];
  }
  return await Promise.all(
    tools.map(async (ref) => {
      if (typeof ref === "string") {
        return await lookupToolByName(registry, ref);
      } else if (isAction(ref)) {
        return asTool(registry, ref);
      } else if (isExecutablePrompt(ref)) {
        return await ref.asTool();
      } else if (ref.name) {
        return await lookupToolByName(
          registry,
          ref.metadata?.originalName || ref.name
        );
      }
      throw new Error("Tools must be strings, tool definitions, or actions.");
    })
  );
}
async function lookupToolByName(registry, name) {
  const tool2 = await registry.lookupAction(name) || await registry.lookupAction(`/tool/${name}`) || await registry.lookupAction(`/prompt/${name}`) || await registry.lookupAction(`/dynamic-action-provider/${name}`);
  if (!tool2) {
    throw new Error(`Tool ${name} not found`);
  }
  return tool2;
}
function toToolDefinition(tool2) {
  const originalName = tool2.__action.name;
  let name = originalName;
  if (originalName.includes("/")) {
    name = originalName.substring(originalName.lastIndexOf("/") + 1);
  }
  const out = {
    name,
    description: tool2.__action.description || "",
    outputSchema: toJsonSchema({
      schema: tool2.__action.outputSchema ?? z.void(),
      jsonSchema: tool2.__action.outputJsonSchema
    }),
    inputSchema: toJsonSchema({
      schema: tool2.__action.inputSchema ?? z.void(),
      jsonSchema: tool2.__action.inputJsonSchema
    })
  };
  if (originalName !== name) {
    out.metadata = { originalName };
  }
  return out;
}
function defineTool(registry, config, fn) {
  const a = defineAction(
    registry,
    {
      ...config,
      actionType: "tool",
      metadata: { ...config.metadata || {}, type: "tool" }
    },
    (i, runOptions) => {
      return fn(i, {
        ...runOptions,
        context: { ...runOptions.context },
        interrupt: interruptTool(registry)
      });
    }
  );
  implementTool(a, config, registry);
  return a;
}
function implementTool(a, config, registry) {
  a.respond = (interrupt2, responseData, options) => {
    if (registry) {
      assertUnstable(
        registry,
        "beta",
        "The 'tool.reply' method is part of the 'interrupts' beta feature."
      );
    }
    parseSchema(responseData, {
      jsonSchema: config.outputJsonSchema,
      schema: config.outputSchema
    });
    return {
      toolResponse: stripUndefinedProps({
        name: interrupt2.toolRequest.name,
        ref: interrupt2.toolRequest.ref,
        output: responseData
      }),
      metadata: {
        interruptResponse: options?.metadata || true
      }
    };
  };
  a.restart = (interrupt2, resumedMetadata, options) => {
    if (registry) {
      assertUnstable(
        registry,
        "beta",
        "The 'tool.restart' method is part of the 'interrupts' beta feature."
      );
    }
    let replaceInput = options?.replaceInput;
    if (replaceInput) {
      replaceInput = parseSchema(replaceInput, {
        schema: config.inputSchema,
        jsonSchema: config.inputJsonSchema
      });
    }
    return {
      toolRequest: stripUndefinedProps({
        name: interrupt2.toolRequest.name,
        ref: interrupt2.toolRequest.ref,
        input: replaceInput || interrupt2.toolRequest.input
      }),
      metadata: stripUndefinedProps({
        ...interrupt2.metadata,
        resumed: resumedMetadata || true,
        // annotate the original input if replacing it
        replacedInput: replaceInput ? interrupt2.toolRequest.input : void 0
      })
    };
  };
}
function isToolRequest(part) {
  return !!part.toolRequest;
}
function isToolResponse(part) {
  return !!part.toolResponse;
}
function isDynamicTool(t) {
  return isAction(t) && !t.__registry;
}
function interrupt(config) {
  const { requestMetadata, ...toolConfig } = config;
  return tool(toolConfig, async (input, { interrupt: interrupt2 }) => {
    if (!config.requestMetadata) interrupt2();
    else if (typeof config.requestMetadata === "object")
      interrupt2(config.requestMetadata);
    else interrupt2(await Promise.resolve(config.requestMetadata(input)));
  });
}
function defineInterrupt(registry, config) {
  const i = interrupt(config);
  registry.registerAction("tool", i);
  return i;
}
class ToolInterruptError extends Error {
  constructor(metadata) {
    super();
    this.metadata = metadata;
    this.name = "ToolInterruptError";
  }
}
function interruptTool(registry) {
  return (metadata) => {
    if (registry) {
      assertUnstable(registry, "beta", "Tool interrupts are a beta feature.");
    }
    throw new ToolInterruptError(metadata);
  };
}
function tool(config, fn) {
  return dynamicTool(config, fn);
}
function dynamicTool(config, fn) {
  const a = action(
    {
      ...config,
      actionType: "tool",
      metadata: { ...config.metadata || {}, type: "tool", dynamic: true }
    },
    (i, runOptions) => {
      const interrupt2 = interruptTool(runOptions.registry);
      if (fn) {
        return fn(i, {
          ...runOptions,
          context: { ...runOptions.context },
          interrupt: interrupt2
        });
      }
      return interrupt2();
    }
  );
  implementTool(a, config);
  a.attach = (_) => a;
  return a;
}
export {
  ToolInterruptError,
  asTool,
  defineInterrupt,
  defineTool,
  dynamicTool,
  interrupt,
  isDynamicTool,
  isToolRequest,
  isToolResponse,
  lookupToolByName,
  resolveTools,
  toToolDefinition,
  tool
};
//# sourceMappingURL=tool.mjs.map