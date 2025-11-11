export { z } from 'zod';
export { q as Action, t as ActionAsyncParams, p as ActionFnArg, A as ActionMetadata, s as ActionParams, n as ActionResult, o as ActionRunOptions, B as BackgroundAction, a as BackgroundActionFnArg, c as BackgroundActionParams, e as BackgroundActionRunOptions, G as GenkitError, Q as InitializedPlugin, J as JSONSchema, v as Middleware, M as MiddlewareWithOptions, f as Operation, O as OperationSchema, R as Plugin, N as PluginProvider, P as Provider, u as SimpleMiddleware, D as StreamingCallback, S as StreamingResponse, U as UnstableApiError, g as UserFacingError, x as action, w as actionWithMiddleware, h as assertUnstable, b as backgroundAction, z as defineAction, C as defineActionAsync, d as defineBackgroundAction, l as defineJsonSchema, m as defineSchema, j as getCallableJSON, k as getHttpStatus, H as getStreamingCallback, y as isAction, i as isBackgroundAction, I as isInRuntimeContext, r as registerBackgroundAction, K as runInActionRuntimeContext, L as runOutsideActionRuntimeContext, F as runWithStreamingCallback, E as sentinelNoopStreamingCallback } from './action-W3NVe6d0.js';
export { getAsyncContext } from './async-context.js';
export { ActionContext, ApiKeyContext, ContextProvider, RequestData, apiKey, getContext, runWithContext } from './context.js';
export { DapConfig, DapFn, DynamicActionProviderAction, defineDynamicActionProvider } from './dynamic-action-provider.js';
export { Flow, FlowConfig, FlowFn, FlowSideChannel, defineFlow, flow, run } from './flow.js';
export { ReflectionServer, ReflectionServerOptions, RunActionResponse, RunActionResponseSchema } from './reflection.js';
export { TelemetryConfig } from './telemetryTypes.js';
export { deleteUndefinedProps, featureMetadataPrefix, getCurrentEnv, isDevEnv, stripUndefinedProps } from './utils.js';
export { Status, StatusCodes, StatusName, StatusSchema } from './statusTypes.js';
export { JSONSchema7 } from 'json-schema';
import 'dotprompt';
import 'ajv';
import '@opentelemetry/sdk-node';

/**
 * Copyright 2024 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
/**
 * Genkit library version.
 */
declare const GENKIT_VERSION = "1.22.0";
/**
 * Genkit client header for API calls.
 */
declare const GENKIT_CLIENT_HEADER: string;
declare const GENKIT_REFLECTION_API_SPEC_VERSION = 1;

/** Additional attribution information to include in the x-goog-api-client header. */
declare function getClientHeader(): string;
/** Sets additional attribution information to include in the x-goog-api-client header. */
declare function setClientHeader(header: string): void;

export { GENKIT_CLIENT_HEADER, GENKIT_REFLECTION_API_SPEC_VERSION, GENKIT_VERSION, getClientHeader, setClientHeader };
