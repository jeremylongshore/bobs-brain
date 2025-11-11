import { version } from "./__codegen/version.js";
const GENKIT_VERSION = version;
const GENKIT_CLIENT_HEADER = `genkit-node/${GENKIT_VERSION} gl-node/${process.versions.node}`;
const GENKIT_REFLECTION_API_SPEC_VERSION = 1;
import { z } from "zod";
export * from "./action.js";
import { getAsyncContext } from "./async-context.js";
import {
  OperationSchema,
  backgroundAction,
  defineBackgroundAction,
  isBackgroundAction,
  registerBackgroundAction
} from "./background-action.js";
import {
  apiKey,
  getContext,
  runWithContext
} from "./context.js";
import {
  defineDynamicActionProvider
} from "./dynamic-action-provider.js";
import {
  GenkitError,
  UnstableApiError,
  UserFacingError,
  assertUnstable,
  getCallableJSON,
  getHttpStatus
} from "./error.js";
import {
  defineFlow,
  flow,
  run
} from "./flow.js";
export * from "./plugin.js";
export * from "./reflection.js";
import { defineJsonSchema, defineSchema } from "./schema.js";
export * from "./telemetryTypes.js";
export * from "./utils.js";
const clientHeaderGlobalKey = "__genkit_ClientHeader";
function getClientHeader() {
  if (global[clientHeaderGlobalKey]) {
    return GENKIT_CLIENT_HEADER + " " + global[clientHeaderGlobalKey];
  }
  return GENKIT_CLIENT_HEADER;
}
function setClientHeader(header) {
  global[clientHeaderGlobalKey] = header;
}
export {
  GENKIT_CLIENT_HEADER,
  GENKIT_REFLECTION_API_SPEC_VERSION,
  GENKIT_VERSION,
  GenkitError,
  OperationSchema,
  UnstableApiError,
  UserFacingError,
  apiKey,
  assertUnstable,
  backgroundAction,
  defineBackgroundAction,
  defineDynamicActionProvider,
  defineFlow,
  defineJsonSchema,
  defineSchema,
  flow,
  getAsyncContext,
  getCallableJSON,
  getClientHeader,
  getContext,
  getHttpStatus,
  isBackgroundAction,
  registerBackgroundAction,
  run,
  runWithContext,
  setClientHeader,
  z
};
//# sourceMappingURL=index.mjs.map