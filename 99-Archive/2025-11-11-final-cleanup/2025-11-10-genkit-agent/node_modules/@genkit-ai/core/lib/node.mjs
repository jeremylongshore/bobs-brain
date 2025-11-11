import { initNodeAsyncContext } from "./node-async-context.js";
import { initNodeTelemetryProvider } from "./tracing/node-telemetry-provider.js";
function initNodeFeatures() {
  initNodeAsyncContext();
  initNodeTelemetryProvider();
}
export {
  initNodeFeatures
};
//# sourceMappingURL=node.mjs.map