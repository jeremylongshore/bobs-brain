import { NodeSDK } from "@opentelemetry/sdk-node";
import {
  BatchSpanProcessor,
  SimpleSpanProcessor
} from "@opentelemetry/sdk-trace-base";
import { logger } from "../logging.js";
import { setTelemetryProvider } from "../tracing.js";
import { isDevEnv } from "../utils.js";
import { TraceServerExporter, setTelemetryServerUrl } from "./exporter.js";
let telemetrySDK = null;
let nodeOtelConfig = null;
function initNodeTelemetryProvider() {
  setTelemetryProvider({
    enableTelemetry,
    flushTracing
  });
}
async function enableTelemetry(telemetryConfig) {
  if (process.env.GENKIT_TELEMETRY_SERVER) {
    setTelemetryServerUrl(process.env.GENKIT_TELEMETRY_SERVER);
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
  telemetrySDK = new NodeSDK(nodeOtelConfig);
  telemetrySDK.start();
  process.on("SIGTERM", async () => await cleanUpTracing());
}
async function cleanUpTracing() {
  if (!telemetrySDK) {
    return;
  }
  await maybeFlushMetrics();
  await telemetrySDK.shutdown();
  logger.debug("OpenTelemetry SDK shut down.");
  telemetrySDK = null;
}
function createTelemetryServerProcessor() {
  const exporter = new TraceServerExporter();
  return isDevEnv() ? new SimpleSpanProcessor(exporter) : new BatchSpanProcessor(exporter);
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
export {
  initNodeTelemetryProvider
};
//# sourceMappingURL=node-telemetry-provider.mjs.map