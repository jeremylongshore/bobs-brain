import { getAsyncContext } from "@genkit-ai/core";
import { v4 as uuidv4 } from "uuid";
import {
  Chat,
  MAIN_THREAD
} from "./chat.js";
import {
  Message,
  isExecutablePrompt,
  tagAsPreamble
} from "./index.js";
class Session {
  constructor(registry, options) {
    this.registry = registry;
    this.id = options?.id ?? uuidv4();
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
      let threadName = MAIN_THREAD;
      let preamble;
      if (optionsOrPreambleOrThreadName) {
        if (typeof optionsOrPreambleOrThreadName === "string") {
          threadName = optionsOrPreambleOrThreadName;
        } else if (isExecutablePrompt(optionsOrPreambleOrThreadName)) {
          preamble = optionsOrPreambleOrThreadName;
        } else {
          options = optionsOrPreambleOrThreadName;
        }
      }
      if (maybeOptionsOrPreamble) {
        if (isExecutablePrompt(maybeOptionsOrPreamble)) {
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
            messages: tagAsPreamble(rb?.messages)
          };
        });
      } else {
        const baseOptions = { ...options };
        const messages = [];
        if (baseOptions.system) {
          messages.push({
            role: "system",
            content: Message.parseContent(baseOptions.system)
          });
        }
        delete baseOptions.system;
        if (baseOptions.messages) {
          messages.push(...baseOptions.messages);
        }
        baseOptions.messages = tagAsPreamble(messages);
        requestBase = Promise.resolve(baseOptions);
      }
      return new Chat(this, requestBase, {
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
  return getAsyncContext().run(sessionAlsKey, session, fn);
}
function getCurrentSession(registry) {
  return getAsyncContext().getStore(sessionAlsKey);
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
export {
  Session,
  SessionError,
  getCurrentSession,
  inMemorySessionStore,
  runWithSession
};
//# sourceMappingURL=session.mjs.map