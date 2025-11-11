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
export {
  logger
};
//# sourceMappingURL=logging.mjs.map