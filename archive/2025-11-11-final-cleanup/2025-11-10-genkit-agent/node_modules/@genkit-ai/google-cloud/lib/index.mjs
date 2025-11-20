import { getCurrentEnv } from "genkit";
import { logger } from "genkit/logging";
import { enableTelemetry } from "genkit/tracing";
import { credentialsFromEnvironment } from "./auth.js";
import { GcpLogger } from "./gcpLogger.js";
import { GcpOpenTelemetry } from "./gcpOpenTelemetry.js";
import { TelemetryConfigs } from "./telemetry/defaults.js";
function enableGoogleCloudTelemetry(options) {
  return enableTelemetry(
    configureGcpPlugin(options).then(async (pluginConfig) => {
      logger.init(await new GcpLogger(pluginConfig).getLogger(getCurrentEnv()));
      return new GcpOpenTelemetry(pluginConfig).getConfig();
    })
  );
}
async function configureGcpPlugin(options) {
  const envOptions = await credentialsFromEnvironment();
  return {
    projectId: options?.projectId || envOptions.projectId,
    credentials: options?.credentials || envOptions.credentials,
    ...TelemetryConfigs.defaults(options)
  };
}
export * from "./gcpLogger.js";
export * from "./gcpOpenTelemetry.js";
export {
  enableGoogleCloudTelemetry
};
//# sourceMappingURL=index.mjs.map