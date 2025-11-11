import { Channel } from "@genkit-ai/core/async";
import {
  ATTR_PREFIX,
  SPAN_TYPE_ATTR,
  runInNewSpan
} from "@genkit-ai/core/tracing";
import {
  generate
} from "./index.js";
import {
  runWithSession
} from "./session.js";
const MAIN_THREAD = "main";
const SESSION_ID_ATTR = `${ATTR_PREFIX}:sessionId`;
const THREAD_NAME_ATTR = `${ATTR_PREFIX}:threadName`;
class Chat {
  constructor(session, requestBase, options) {
    this.session = session;
    this.sessionId = options.id;
    this.threadName = options.thread;
    this.requestBase = requestBase?.then((rb) => {
      const requestBase2 = { ...rb };
      if (requestBase2 && requestBase2["prompt"]) {
        const basePrompt = requestBase2["prompt"];
        let promptMessage;
        if (typeof basePrompt === "string") {
          promptMessage = {
            role: "user",
            content: [{ text: basePrompt }]
          };
        } else if (Array.isArray(basePrompt)) {
          promptMessage = {
            role: "user",
            content: basePrompt
          };
        } else {
          promptMessage = {
            role: "user",
            content: [basePrompt]
          };
        }
        requestBase2.messages = [...requestBase2.messages ?? [], promptMessage];
      }
      if (hasPreamble(requestBase2.messages)) {
        requestBase2.messages = [
          // if request base contains a preamble, always put it first
          ...getPreamble(requestBase2.messages) ?? [],
          // strip out the preamble from history
          ...stripPreamble(options.messages) ?? [],
          // add whatever non-preamble remains from request
          ...stripPreamble(requestBase2.messages) ?? []
        ];
      } else {
        requestBase2.messages = [
          ...options.messages ?? [],
          ...requestBase2.messages ?? []
        ];
      }
      this._messages = requestBase2.messages;
      return requestBase2;
    });
    this._messages = options.messages;
  }
  requestBase;
  sessionId;
  _messages;
  threadName;
  async send(options) {
    return runWithSession(
      this.session.registry,
      this.session,
      () => runInNewSpan(
        this.session.registry,
        {
          metadata: {
            name: "send"
          },
          labels: {
            [SPAN_TYPE_ATTR]: "helper",
            [SESSION_ID_ATTR]: this.session.id,
            [THREAD_NAME_ATTR]: this.threadName
          }
        },
        async (metadata) => {
          const resolvedOptions = resolveSendOptions(options);
          let streamingCallback = void 0;
          if (resolvedOptions.onChunk || resolvedOptions.streamingCallback) {
            streamingCallback = resolvedOptions.onChunk ?? resolvedOptions.streamingCallback;
          }
          const request = {
            ...await this.requestBase,
            messages: this.messages,
            ...resolvedOptions
          };
          metadata.input = resolvedOptions;
          const response = await generate(this.session.registry, {
            ...request,
            onChunk: streamingCallback
          });
          this.requestBase = Promise.resolve({
            ...await this.requestBase,
            // these things may get changed by tools calling within generate.
            tools: response?.request?.tools?.map((td) => td.name),
            toolChoice: response?.request?.toolChoice,
            config: response?.request?.config
          });
          await this.updateMessages(response.messages);
          metadata.output = JSON.stringify(response);
          return response;
        }
      )
    );
  }
  sendStream(options) {
    const channel = new Channel();
    const resolvedOptions = resolveSendOptions(options);
    const sent = this.send({
      ...resolvedOptions,
      onChunk: (chunk) => channel.send(chunk)
    });
    sent.then(
      () => channel.close(),
      (err) => channel.error(err)
    );
    return {
      response: sent,
      stream: channel
    };
  }
  get messages() {
    return this._messages ?? [];
  }
  async updateMessages(messages) {
    this._messages = messages;
    await this.session.updateMessages(this.threadName, messages);
  }
}
function hasPreamble(msgs) {
  return !!msgs?.find((m) => m.metadata?.preamble);
}
function getPreamble(msgs) {
  return msgs?.filter((m) => m.metadata?.preamble);
}
function stripPreamble(msgs) {
  return msgs?.filter((m) => !m.metadata?.preamble);
}
function resolveSendOptions(options) {
  let resolvedOptions;
  if (typeof options === "string") {
    resolvedOptions = {
      prompt: options
    };
  } else if (Array.isArray(options)) {
    resolvedOptions = {
      prompt: options
    };
  } else {
    resolvedOptions = options;
  }
  return resolvedOptions;
}
export {
  Chat,
  MAIN_THREAD,
  SESSION_ID_ATTR,
  THREAD_NAME_ATTR
};
//# sourceMappingURL=chat.mjs.map