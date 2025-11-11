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
var chat_exports = {};
__export(chat_exports, {
  Chat: () => Chat,
  MAIN_THREAD: () => MAIN_THREAD,
  SESSION_ID_ATTR: () => SESSION_ID_ATTR,
  THREAD_NAME_ATTR: () => THREAD_NAME_ATTR
});
module.exports = __toCommonJS(chat_exports);
var import_async = require("@genkit-ai/core/async");
var import_tracing = require("@genkit-ai/core/tracing");
var import_index = require("./index.js");
var import_session = require("./session.js");
const MAIN_THREAD = "main";
const SESSION_ID_ATTR = `${import_tracing.ATTR_PREFIX}:sessionId`;
const THREAD_NAME_ATTR = `${import_tracing.ATTR_PREFIX}:threadName`;
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
    return (0, import_session.runWithSession)(
      this.session.registry,
      this.session,
      () => (0, import_tracing.runInNewSpan)(
        this.session.registry,
        {
          metadata: {
            name: "send"
          },
          labels: {
            [import_tracing.SPAN_TYPE_ATTR]: "helper",
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
          const response = await (0, import_index.generate)(this.session.registry, {
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
    const channel = new import_async.Channel();
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
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  Chat,
  MAIN_THREAD,
  SESSION_ID_ATTR,
  THREAD_NAME_ATTR
});
//# sourceMappingURL=chat.js.map