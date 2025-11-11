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
var logging_exports = {};
__export(logging_exports, {
  logger: () => logger
});
module.exports = __toCommonJS(logging_exports);
const LOG_LEVELS = ["debug", "info", "warn", "error"];
const loggerKey = "__genkit_logger";
const _defaultLogger = {
  shouldLog(targetLevel) {
    return LOG_LEVELS.indexOf(this.level) <= LOG_LEVELS.indexOf(targetLevel);
  },
  debug(...args) {
    this.shouldLog("debug") && console.debug(...args);
  },
  info(...args) {
    this.shouldLog("info") && console.info(...args);
  },
  warn(...args) {
    this.shouldLog("warn") && console.warn(...args);
  },
  error(...args) {
    this.shouldLog("error") && console.error(...args);
  },
  level: "info"
};
function getLogger() {
  if (!global[loggerKey]) {
    global[loggerKey] = _defaultLogger;
  }
  return global[loggerKey];
}
class Logger {
  defaultLogger = _defaultLogger;
  init(fn) {
    global[loggerKey] = fn;
  }
  info(...args) {
    getLogger().info.apply(getLogger(), args);
  }
  debug(...args) {
    getLogger().debug.apply(getLogger(), args);
  }
  error(...args) {
    getLogger().error.apply(getLogger(), args);
  }
  warn(...args) {
    getLogger().warn.apply(getLogger(), args);
  }
  setLogLevel(level) {
    getLogger().level = level;
  }
  logStructured(msg, metadata) {
    getLogger().info(msg, metadata);
  }
  logStructuredError(msg, metadata) {
    getLogger().error(msg, metadata);
  }
}
const logger = new Logger();
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  logger
});
//# sourceMappingURL=logging.js.map