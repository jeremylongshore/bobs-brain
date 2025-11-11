"use strict";
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
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
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);
var reflection_exports = {};
__export(reflection_exports, {
  ReflectionServer: () => ReflectionServer,
  RunActionResponseSchema: () => RunActionResponseSchema
});
module.exports = __toCommonJS(reflection_exports);
var import_express = __toESM(require("express"));
var import_promises = __toESM(require("fs/promises"));
var import_get_port = __toESM(require("get-port"));
var import_path = __toESM(require("path"));
var z = __toESM(require("zod"));
var import_action = require("./action.js");
var import_index = require("./index.js");
var import_logging = require("./logging.js");
var import_schema = require("./schema.js");
var import_tracing = require("./tracing.js");
const RunActionResponseSchema = z.object({
  result: z.unknown().optional(),
  error: z.unknown().optional(),
  telemetry: z.object({
    traceId: z.string().optional()
  }).optional()
});
class ReflectionServer {
  /** List of all running servers needed to be cleaned up on process exit. */
  static RUNNING_SERVERS = [];
  /** Registry instance to be used for API calls. */
  registry;
  /** Options for the reflection server. */
  options;
  /** Port the server is actually running on. This may differ from `options.port` if the original was occupied. Null if server is not running. */
  port = null;
  /** Express server instance. Null if server is not running. */
  server = null;
  /** Path to the runtime file. Null if server is not running. */
  runtimeFilePath = null;
  constructor(registry, options) {
    this.registry = registry;
    this.options = {
      port: 3100,
      bodyLimit: "30mb",
      configuredEnvs: ["dev"],
      ...options
    };
  }
  get runtimeId() {
    return `${process.pid}${this.port !== null ? `-${this.port}` : ""}`;
  }
  /**
   * Finds a free port to run the server on based on the original chosen port and environment.
   */
  async findPort() {
    const chosenPort = this.options.port;
    const freePort = await (0, import_get_port.default)({
      port: (0, import_get_port.makeRange)(chosenPort, chosenPort + 100)
    });
    if (freePort !== chosenPort) {
      import_logging.logger.warn(
        `Port ${chosenPort} is already in use, using next available port ${freePort} instead.`
      );
    }
    return freePort;
  }
  /**
   * Starts the server.
   *
   * The server will be registered to be shut down on process exit.
   */
  async start() {
    const server = (0, import_express.default)();
    server.use(import_express.default.json({ limit: this.options.bodyLimit }));
    server.use((req, res, next) => {
      res.header("x-genkit-version", import_index.GENKIT_VERSION);
      next();
    });
    server.get("/api/__health", async (req, response) => {
      if (req.query["id"] && req.query["id"] !== this.runtimeId) {
        response.status(503).send("Invalid runtime ID");
        return;
      }
      await this.registry.listActions();
      response.status(200).send("OK");
    });
    server.get("/api/__quitquitquit", async (_, response) => {
      import_logging.logger.debug("Received quitquitquit");
      response.status(200).send("OK");
      await this.stop();
    });
    server.get("/api/actions", async (_, response, next) => {
      import_logging.logger.debug("Fetching actions.");
      try {
        const actions = await this.registry.listResolvableActions();
        const convertedActions = {};
        Object.keys(actions).forEach((key) => {
          const action = actions[key];
          convertedActions[key] = {
            key,
            name: action.name,
            description: action.description,
            metadata: action.metadata
          };
          if (action.inputSchema || action.inputJsonSchema) {
            convertedActions[key].inputSchema = (0, import_schema.toJsonSchema)({
              schema: action.inputSchema,
              jsonSchema: action.inputJsonSchema
            });
          }
          if (action.outputSchema || action.outputJsonSchema) {
            convertedActions[key].outputSchema = (0, import_schema.toJsonSchema)({
              schema: action.outputSchema,
              jsonSchema: action.outputJsonSchema
            });
          }
        });
        response.send(convertedActions);
      } catch (err) {
        const { message, stack } = err;
        next({ message, stack });
      }
    });
    server.post("/api/runAction", async (request, response, next) => {
      const { key, input, context, telemetryLabels } = request.body;
      const { stream } = request.query;
      import_logging.logger.debug(`Running action \`${key}\` with stream=${stream}...`);
      try {
        const action = await this.registry.lookupAction(key);
        if (!action) {
          response.status(404).send(`action ${key} not found`);
          return;
        }
        if (stream === "true") {
          try {
            const callback = (chunk) => {
              response.write(JSON.stringify(chunk) + "\n");
            };
            const result = await action.run(input, {
              context,
              onChunk: callback,
              telemetryLabels
            });
            await (0, import_tracing.flushTracing)();
            response.write(
              JSON.stringify({
                result: result.result,
                telemetry: {
                  traceId: result.telemetry.traceId
                }
              })
            );
            response.end();
          } catch (err) {
            const { message, stack } = err;
            const errorResponse = {
              code: import_action.StatusCodes.INTERNAL,
              message,
              details: {
                stack
              }
            };
            if (err.traceId) {
              errorResponse.details.traceId = err.traceId;
            }
            response.write(
              JSON.stringify({
                error: errorResponse
              })
            );
            response.end();
          }
        } else {
          const result = await action.run(input, { context, telemetryLabels });
          await (0, import_tracing.flushTracing)();
          response.send({
            result: result.result,
            telemetry: {
              traceId: result.telemetry.traceId
            }
          });
        }
      } catch (err) {
        const { message, stack, traceId } = err;
        next({ message, stack, traceId });
      }
    });
    server.get("/api/envs", async (_, response) => {
      response.json(this.options.configuredEnvs);
    });
    server.post("/api/notify", async (request, response) => {
      const { telemetryServerUrl, reflectionApiSpecVersion } = request.body;
      if (!process.env.GENKIT_TELEMETRY_SERVER) {
        if (typeof telemetryServerUrl === "string") {
          (0, import_tracing.setTelemetryServerUrl)(telemetryServerUrl);
          import_logging.logger.debug(
            `Connected to telemetry server on ${telemetryServerUrl}`
          );
        }
      }
      if (reflectionApiSpecVersion !== import_index.GENKIT_REFLECTION_API_SPEC_VERSION) {
        if (!reflectionApiSpecVersion || reflectionApiSpecVersion < import_index.GENKIT_REFLECTION_API_SPEC_VERSION) {
          import_logging.logger.warn(
            "WARNING: Genkit CLI version may be outdated. Please update `genkit-cli` to the latest version."
          );
        } else {
          import_logging.logger.warn(
            `Genkit CLI is newer than runtime library. Some feature may not be supported. Consider upgrading your runtime library version (debug info: expected ${import_index.GENKIT_REFLECTION_API_SPEC_VERSION}, got ${reflectionApiSpecVersion}).`
          );
        }
      }
      response.status(200).send("OK");
    });
    server.use((err, req, res, next) => {
      import_logging.logger.error(err.stack);
      const error = err;
      const { message, stack } = error;
      const errorResponse = {
        code: import_action.StatusCodes.INTERNAL,
        message,
        details: {
          stack
        }
      };
      if (err.traceId) {
        errorResponse.details.traceId = err.traceId;
      }
      res.status(500).json(errorResponse);
    });
    this.port = await this.findPort();
    this.server = server.listen(this.port, async () => {
      import_logging.logger.debug(
        `Reflection server (${process.pid}) running on http://localhost:${this.port}`
      );
      ReflectionServer.RUNNING_SERVERS.push(this);
      await this.writeRuntimeFile();
    });
  }
  /**
   * Stops the server and removes it from the list of running servers to clean up on exit.
   */
  async stop() {
    if (!this.server) {
      return;
    }
    return new Promise(async (resolve, reject) => {
      await this.cleanupRuntimeFile();
      this.server.close(async (err) => {
        if (err) {
          import_logging.logger.error(
            `Error shutting down reflection server on port ${this.port}: ${err}`
          );
          reject(err);
        }
        const index = ReflectionServer.RUNNING_SERVERS.indexOf(this);
        if (index > -1) {
          ReflectionServer.RUNNING_SERVERS.splice(index, 1);
        }
        import_logging.logger.debug(
          `Reflection server on port ${this.port} has successfully shut down.`
        );
        this.port = null;
        this.server = null;
        resolve();
      });
    });
  }
  /**
   * Writes the runtime file to the project root.
   */
  async writeRuntimeFile() {
    try {
      const rootDir = await findProjectRoot();
      const runtimesDir = import_path.default.join(rootDir, ".genkit", "runtimes");
      const date = /* @__PURE__ */ new Date();
      const time = date.getTime();
      const timestamp = date.toISOString();
      this.runtimeFilePath = import_path.default.join(
        runtimesDir,
        `${this.runtimeId}-${time}.json`
      );
      const fileContent = JSON.stringify(
        {
          id: process.env.GENKIT_RUNTIME_ID || this.runtimeId,
          pid: process.pid,
          name: this.options.name,
          reflectionServerUrl: `http://localhost:${this.port}`,
          timestamp,
          genkitVersion: `nodejs/${import_index.GENKIT_VERSION}`,
          reflectionApiSpecVersion: import_index.GENKIT_REFLECTION_API_SPEC_VERSION
        },
        null,
        2
      );
      await import_promises.default.mkdir(runtimesDir, { recursive: true });
      await import_promises.default.writeFile(this.runtimeFilePath, fileContent, "utf8");
      import_logging.logger.debug(`Runtime file written: ${this.runtimeFilePath}`);
    } catch (error) {
      import_logging.logger.error(`Error writing runtime file: ${error}`);
    }
  }
  /**
   * Cleans up the port file.
   */
  async cleanupRuntimeFile() {
    if (!this.runtimeFilePath) {
      return;
    }
    try {
      const fileContent = await import_promises.default.readFile(this.runtimeFilePath, "utf8");
      const data = JSON.parse(fileContent);
      if (data.pid === process.pid) {
        await import_promises.default.unlink(this.runtimeFilePath);
        import_logging.logger.debug(`Runtime file cleaned up: ${this.runtimeFilePath}`);
      }
    } catch (error) {
      import_logging.logger.error(`Error cleaning up runtime file: ${error}`);
    }
  }
  /**
   * Stops all running reflection servers.
   */
  static async stopAll() {
    return Promise.all(
      ReflectionServer.RUNNING_SERVERS.map((server) => server.stop())
    );
  }
}
async function findProjectRoot() {
  let currentDir = process.cwd();
  while (currentDir !== import_path.default.parse(currentDir).root) {
    const packageJsonPath = import_path.default.join(currentDir, "package.json");
    try {
      await import_promises.default.access(packageJsonPath);
      return currentDir;
    } catch {
      currentDir = import_path.default.dirname(currentDir);
    }
  }
  throw new Error("Could not find project root (package.json not found)");
}
if (typeof module !== "undefined" && "hot" in module) {
  module.hot.accept();
  module.hot.dispose(async () => {
    import_logging.logger.debug("Cleaning up reflection server(s) before module reload...");
    await ReflectionServer.stopAll();
  });
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  ReflectionServer,
  RunActionResponseSchema
});
//# sourceMappingURL=reflection.js.map