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
var node_telemetry_provider_exports = {};
__export(node_telemetry_provider_exports, {
  initNodeTelemetryProvider: () => initNodeTelemetryProvider
});
module.exports = __toCommonJS(node_telemetry_provider_exports);
var import_sdk_node = require("@opentelemetry/sdk-node");
var import_sdk_trace_base = require("@opentelemetry/sdk-trace-base");
var import_logging = require("../logging.js");
var import_tracing = require("../tracing.js");
var import_utils = require("../utils.js");
var import_exporter = require("./exporter.js");
let telemetrySDK = null;
let nodeOtelConfig = null;
function initNodeTelemetryProvider() {
  (0, import_tracing.setTelemetryProvider)({
    enableTelemetry,
    flushTracing
  });
}
async function enableTelemetry(telemetryConfig) {
  if (process.env.GENKIT_TELEMETRY_SERVER) {
    (0, import_exporter.setTelemetryServerUrl)(process.env.GENKIT_TELEMETRY_SERVER);
  }
  telemetryConfig = telemetryConfig instanceof Promise ? await telemetryConfig : telemetryConfig;
  nodeOtelConfig = telemetryConfig || {};
  const processors = [createTelemetryServerProcessor()];
  if (nodeOtelConfig.traceExporter) {
    throw new Error("Please specify spanProcessors instead.");
  }
  if (nodeOtelConfig.spanProcessors) {
    processors.push(...nodeOtelConfig.spanProcessors);
  }
  if (nodeOtelConfig.spanProcessor) {
    processors.push(nodeOtelConfig.spanProcessor);
    delete nodeOtelConfig.spanProcessor;
  }
  nodeOtelConfig.spanProcessors = processors;
  telemetrySDK = new import_sdk_node.NodeSDK(nodeOtelConfig);
  telemetrySDK.start();
  process.on("SIGTERM", async () => await cleanUpTracing());
}
async function cleanUpTracing() {
  if (!telemetrySDK) {
    return;
  }
  await maybeFlushMetrics();
  await telemetrySDK.shutdown();
  import_logging.logger.debug("OpenTelemetry SDK shut down.");
  telemetrySDK = null;
}
function createTelemetryServerProcessor() {
  const exporter = new import_exporter.TraceServerExporter();
  return (0, import_utils.isDevEnv)() ? new import_sdk_trace_base.SimpleSpanProcessor(exporter) : new import_sdk_trace_base.BatchSpanProcessor(exporter);
}
function maybeFlushMetrics() {
  if (nodeOtelConfig?.metricReader) {
    return nodeOtelConfig.metricReader.forceFlush();
  }
  return Promise.resolve();
}
async function flushTracing() {
  if (nodeOtelConfig?.spanProcessors) {
    await Promise.all(nodeOtelConfig.spanProcessors.map((p) => p.forceFlush()));
  }
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  initNodeTelemetryProvider
});
//# sourceMappingURL=node-telemetry-provider.js.map