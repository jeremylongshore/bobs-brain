import { GenkitError, stripUndefinedProps } from "@genkit-ai/core";
import { logger } from "@genkit-ai/core/logging";
import { isPromptAction } from "../prompt.js";
import {
  ToolInterruptError,
  isToolRequest,
  resolveTools
} from "../tool.js";
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
      throw new GenkitError({
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
    throw new GenkitError({
      status: "NOT_FOUND",
      message: `Tool ${part.toolRequest.name} not found`,
      detail: { request: rawRequest }
    });
  }
  if (isPromptAction(tool)) {
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
    const response = stripUndefinedProps({
      toolResponse: {
        name: part.toolRequest.name,
        ref: part.toolRequest.ref,
        output
      }
    });
    return { response };
  } catch (e) {
    if (e instanceof ToolInterruptError || // There's an inexplicable case when the above type check fails, only in tests.
    e.name === "ToolInterruptError") {
      const ie = e;
      logger.debug(
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
  const toolMap = toToolMap(await resolveTools(registry, rawRequest.tools));
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
          throw new GenkitError({
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
    return stripUndefinedProps({
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
    return stripUndefinedProps({
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
      throw new GenkitError({
        status: "INTERNAL",
        message: `Prompt tool '${restartRequest.toolRequest.name}' executed inside 'restart' resolution. This should never happen.`
      });
    }
    if (interrupt) return { interrupt };
    if (response) {
      const toolResponse = response;
      const { interrupt: interrupt2, ...metadata } = part.metadata || {};
      return stripUndefinedProps({
        toolResponse,
        toolRequest: {
          ...part,
          metadata: { ...metadata, resolvedInterrupt: interrupt2 }
        }
      });
    }
  }
  throw new GenkitError({
    status: "INVALID_ARGUMENT",
    message: `Unresolved tool request '${part.toolRequest.name}${part.toolRequest.ref ? `#${part.toolRequest.ref}` : ""}' was not handled by the 'resume' argument. You must supply replies or restarts for all interrupted tool requests.'`
  });
}
async function resolveResumeOption(registry, rawRequest) {
  if (!rawRequest.resume) return { revisedRequest: rawRequest };
  const toolMap = toToolMap(await resolveTools(registry, rawRequest.tools));
  const messages = rawRequest.messages;
  const lastMessage = messages.at(-1);
  if (!lastMessage || lastMessage.role !== "model" || !lastMessage.content.find((p) => p.toolRequest)) {
    throw new GenkitError({
      status: "FAILED_PRECONDITION",
      message: `Cannot 'resume' generation unless the previous message is a model message with at least one tool request.`
    });
  }
  const toolResponses = [];
  let interrupted = false;
  lastMessage.content = await Promise.all(
    lastMessage.content.map(async (part) => {
      if (!isToolRequest(part)) return part;
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
    throw new GenkitError({
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
  return stripUndefinedProps({
    revisedRequest: {
      ...rawRequest,
      resume: void 0,
      messages: [...messages, toolMessage]
    },
    toolMessage
  });
}
async function resolveRestartedTools(registry, rawRequest) {
  const toolMap = toToolMap(await resolveTools(registry, rawRequest.tools));
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
export {
  assertValidToolNames,
  resolveRestartedTools,
  resolveResumeOption,
  resolveToolRequest,
  resolveToolRequests,
  toPendingOutput,
  toToolMap
};
//# sourceMappingURL=resolve-tool-requests.mjs.map