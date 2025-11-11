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
var session_exports = {};
__export(session_exports, {
  Session: () => Session,
  SessionError: () => SessionError,
  getCurrentSession: () => getCurrentSession,
  inMemorySessionStore: () => inMemorySessionStore,
  runWithSession: () => runWithSession
});
module.exports = __toCommonJS(session_exports);
var import_core = require("@genkit-ai/core");
var import_uuid = require("uuid");
var import_chat = require("./chat.js");
var import_index = require("./index.js");
class Session {
  constructor(registry, options) {
    this.registry = registry;
    this.id = options?.id ?? (0, import_uuid.v4)();
    this.sessionData = options?.sessionData ?? {
      id: this.id
    };
    if (!this.sessionData) {
      this.sessionData = { id: this.id };
    }
    if (!this.sessionData.threads) {
      this.sessionData.threads = {};
    }
    this.store = options?.store ?? new InMemorySessionStore();
  }
  id;
  sessionData;
  store;
  get state() {
    return this.sessionData.state;
  }
  /**
   * Update session state data.
   */
  async updateState(data) {
    let sessionData = this.sessionData;
    if (!sessionData) {
      sessionData = {};
    }
    sessionData.state = data;
    this.sessionData = sessionData;
    await this.store.save(this.id, sessionData);
  }
  /**
   * Update messages for a given thread.
   */
  async updateMessages(thread, messages) {
    let sessionData = this.sessionData;
    if (!sessionData) {
      sessionData = {};
    }
    if (!sessionData.threads) {
      sessionData.threads = {};
    }
    sessionData.threads[thread] = messages.map(
      (m) => m.toJSON ? m.toJSON() : m
    );
    this.sessionData = sessionData;
    await this.store.save(this.id, sessionData);
  }
  chat(optionsOrPreambleOrThreadName, maybeOptionsOrPreamble, maybeOptions) {
    return runWithSession(this.registry, this, () => {
      let options;
      let threadName = import_chat.MAIN_THREAD;
      let preamble;
      if (optionsOrPreambleOrThreadName) {
        if (typeof optionsOrPreambleOrThreadName === "string") {
          threadName = optionsOrPreambleOrThreadName;
        } else if ((0, import_index.isExecutablePrompt)(optionsOrPreambleOrThreadName)) {
          preamble = optionsOrPreambleOrThreadName;
        } else {
          options = optionsOrPreambleOrThreadName;
        }
      }
      if (maybeOptionsOrPreamble) {
        if ((0, import_index.isExecutablePrompt)(maybeOptionsOrPreamble)) {
          preamble = maybeOptionsOrPreamble;
        } else {
          options = maybeOptionsOrPreamble;
        }
      }
      if (maybeOptions) {
        options = maybeOptions;
      }
      let requestBase;
      if (preamble) {
        const renderOptions = options;
        requestBase = preamble.render(renderOptions?.input, renderOptions).then((rb) => {
          return {
            ...rb,
            messages: (0, import_index.tagAsPreamble)(rb?.messages)
          };
        });
      } else {
        const baseOptions = { ...options };
        const messages = [];
        if (baseOptions.system) {
          messages.push({
            role: "system",
            content: import_index.Message.parseContent(baseOptions.system)
          });
        }
        delete baseOptions.system;
        if (baseOptions.messages) {
          messages.push(...baseOptions.messages);
        }
        baseOptions.messages = (0, import_index.tagAsPreamble)(messages);
        requestBase = Promise.resolve(baseOptions);
      }
      return new import_chat.Chat(this, requestBase, {
        thread: threadName,
        id: this.id,
        messages: (this.sessionData?.threads && this.sessionData?.threads[threadName]) ?? []
      });
    });
  }
  /**
   * Executes provided function within this session context allowing calling
   * `ai.currentSession().state`
   */
  run(fn) {
    return runWithSession(this.registry, this, fn);
  }
  toJSON() {
    return this.sessionData;
  }
}
const sessionAlsKey = "ai.session";
function runWithSession(registry, session, fn) {
  return (0, import_core.getAsyncContext)().run(sessionAlsKey, session, fn);
}
function getCurrentSession(registry) {
  return (0, import_core.getAsyncContext)().getStore(sessionAlsKey);
}
class SessionError extends Error {
  constructor(msg) {
    super(msg);
  }
}
function inMemorySessionStore() {
  return new InMemorySessionStore();
}
class InMemorySessionStore {
  data = {};
  async get(sessionId) {
    return this.data[sessionId];
  }
  async save(sessionId, sessionData) {
    this.data[sessionId] = sessionData;
  }
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  Session,
  SessionError,
  getCurrentSession,
  inMemorySessionStore,
  runWithSession
});
//# sourceMappingURL=session.js.map