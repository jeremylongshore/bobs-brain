import { JSONSchema7 } from 'json-schema';
import * as z from 'zod';
import { z as z$1 } from 'zod';
import { ActionContext } from './context.js';
import { StatusName } from './statusTypes.js';
import { Dotprompt } from 'dotprompt';
import { JSONSchemaType, ErrorObject } from 'ajv';

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

interface Provider<T> {
    id: string;
    value: T;
}
interface PluginProvider {
    name: string;
    initializer: () => InitializedPlugin | void | Promise<InitializedPlugin | void>;
    resolver?: (action: ActionType, target: string) => Promise<void>;
    listActions?: () => Promise<ActionMetadata[]>;
}
interface InitializedPlugin {
    models?: Action<z$1.ZodTypeAny, z$1.ZodTypeAny>[];
    retrievers?: Action<z$1.ZodTypeAny, z$1.ZodTypeAny>[];
    embedders?: Action<z$1.ZodTypeAny, z$1.ZodTypeAny>[];
    indexers?: Action<z$1.ZodTypeAny, z$1.ZodTypeAny>[];
    evaluators?: Action<z$1.ZodTypeAny, z$1.ZodTypeAny>[];
    /** @deprecated */
    flowStateStore?: Provider<any> | Provider<any>[];
    /** @deprecated */
    traceStore?: Provider<any> | Provider<any>[];
    /** @deprecated */
    telemetry?: any;
}
type Plugin<T extends any[]> = (...args: T) => PluginProvider;

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
 * Zod schema of an opration representing a background task.
 */
declare const OperationSchema: z.ZodObject<{
    action: z.ZodOptional<z.ZodString>;
    id: z.ZodString;
    done: z.ZodOptional<z.ZodBoolean>;
    output: z.ZodOptional<z.ZodAny>;
    error: z.ZodOptional<z.ZodObject<{
        message: z.ZodString;
    }, "passthrough", z.ZodTypeAny, z.objectOutputType<{
        message: z.ZodString;
    }, z.ZodTypeAny, "passthrough">, z.objectInputType<{
        message: z.ZodString;
    }, z.ZodTypeAny, "passthrough">>>;
    metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodAny>>;
}, "strip", z.ZodTypeAny, {
    id: string;
    error?: z.objectOutputType<{
        message: z.ZodString;
    }, z.ZodTypeAny, "passthrough"> | undefined;
    output?: any;
    metadata?: Record<string, any> | undefined;
    action?: string | undefined;
    done?: boolean | undefined;
}, {
    id: string;
    error?: z.objectInputType<{
        message: z.ZodString;
    }, z.ZodTypeAny, "passthrough"> | undefined;
    output?: any;
    metadata?: Record<string, any> | undefined;
    action?: string | undefined;
    done?: boolean | undefined;
}>;
/**
 * Background operation.
 */
interface Operation<O = any> {
    action?: string;
    id: string;
    done?: boolean;
    output?: O;
    error?: {
        message: string;
        [key: string]: unknown;
    };
    metadata?: Record<string, any>;
}
/**
 * Background action. Unlike regular action, background action can run for a long time in the background.
 * The returned operation can used to check the status of the background operation and retrieve the response.
 */
interface BackgroundAction<I extends z.ZodTypeAny = z.ZodTypeAny, O extends z.ZodTypeAny = z.ZodTypeAny, RunOptions extends BackgroundActionRunOptions = BackgroundActionRunOptions> {
    __action: ActionMetadata<I, O>;
    readonly startAction: Action<I, typeof OperationSchema>;
    readonly checkAction: Action<typeof OperationSchema, typeof OperationSchema>;
    readonly cancelAction?: Action<typeof OperationSchema, typeof OperationSchema>;
    readonly supportsCancel: boolean;
    start(input?: z.infer<I>, options?: RunOptions): Promise<Operation<z.infer<O>>>;
    check(operation: Operation<z.infer<O>>): Promise<Operation<z.infer<O>>>;
    cancel(operation: Operation<z.infer<O>>): Promise<Operation<z.infer<O>>>;
}
declare function lookupBackgroundAction<I extends z.ZodTypeAny = z.ZodTypeAny, O extends z.ZodTypeAny = z.ZodTypeAny>(registry: Registry, key: string): Promise<BackgroundAction<I, O> | undefined>;
/**
 * Options (side channel) data to pass to the model.
 */
interface BackgroundActionRunOptions {
    /**
     * Additional runtime context data (ex. auth context data).
     */
    context?: ActionContext;
    /**
     * Additional span attributes to apply to OT spans.
     */
    telemetryLabels?: Record<string, string>;
}
/**
 * Options (side channel) data to pass to the model.
 */
interface BackgroundActionFnArg<S> {
    /**
     * Additional runtime context data (ex. auth context data).
     */
    context?: ActionContext;
    /**
     * Trace context containing trace and span IDs.
     */
    trace: {
        traceId: string;
        spanId: string;
    };
}
/**
 * Action factory params.
 */
type BackgroundActionParams<I extends z.ZodTypeAny, O extends z.ZodTypeAny, S extends z.ZodTypeAny = z.ZodTypeAny> = {
    name: string;
    start: (input: z.infer<I>, options: BackgroundActionFnArg<z.infer<S>>) => Promise<Operation<z.infer<O>>>;
    check: (input: Operation<z.infer<O>>) => Promise<Operation<z.infer<O>>>;
    cancel?: (input: Operation<z.infer<O>>) => Promise<Operation<z.infer<O>>>;
    actionType: ActionType;
    description?: string;
    inputSchema?: I;
    inputJsonSchema?: JSONSchema7;
    outputSchema?: O;
    outputJsonSchema?: JSONSchema7;
    metadata?: Record<string, any>;
    use?: Middleware<z.infer<I>, z.infer<O>>[];
    streamSchema?: S;
};
/**
 * Defines an action with the given config and registers it in the registry.
 */
declare function defineBackgroundAction<I extends z.ZodTypeAny, O extends z.ZodTypeAny, S extends z.ZodTypeAny = z.ZodTypeAny>(registry: Registry, config: BackgroundActionParams<I, O, S>): BackgroundAction<I, O>;
declare function registerBackgroundAction(registry: Registry, act: BackgroundAction<any, any>, opts?: {
    namespace?: string;
}): void;
/**
 * Creates a background action with the given config.
 */
declare function backgroundAction<I extends z.ZodTypeAny, O extends z.ZodTypeAny, S extends z.ZodTypeAny = z.ZodTypeAny>(config: BackgroundActionParams<I, O, S>): BackgroundAction<I, O>;
declare function isBackgroundAction(a: unknown): a is BackgroundAction;

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

interface HttpErrorWireFormat {
    details?: unknown;
    message: string;
    status: StatusName;
}
/**
 * Base error class for Genkit errors.
 */
declare class GenkitError extends Error {
    source?: string;
    status: StatusName;
    detail?: any;
    code: number;
    originalMessage: string;
    constructor({ status, message, detail, source, }: {
        status: StatusName;
        message: string;
        detail?: any;
        source?: string;
    });
    /**
     * Returns a JSON-serializable representation of this object.
     */
    toJSON(): HttpErrorWireFormat;
}
declare class UnstableApiError extends GenkitError {
    constructor(level: 'beta', message?: string);
}
/**
 * assertUnstable allows features to raise exceptions when using Genkit from *more* stable initialized instances.
 *
 * @param level The maximum stability channel allowed.
 * @param message An optional message describing which feature is not allowed.
 */
declare function assertUnstable(registry: Registry, level: 'beta', message?: string): void;
/**
 * Creates a new class of Error for issues to be returned to users.
 * Using this error allows a web framework handler (e.g. express, next) to know it
 * is safe to return the message in a request. Other kinds of errors will
 * result in a generic 500 message to avoid the possibility of internal
 * exceptions being leaked to attackers.
 * In JSON requests, code will be an HTTP code and error will be a response body.
 * In streaming requests, { code, message } will be passed as the error message.
 */
declare class UserFacingError extends GenkitError {
    constructor(status: StatusName, message: string, details?: any);
}
declare function getHttpStatus(e: any): number;
declare function getCallableJSON(e: any): HttpErrorWireFormat;
/**
 * Extracts error message from the given error object, or if input is not an error then just turn the error into a string.
 */
declare function getErrorMessage(e: any): string;
/**
 * Extracts stack trace from the given error object, or if input is not an error then returns undefined.
 */
declare function getErrorStack(e: any): string | undefined;

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
 * JSON schema.
 */
type JSONSchema = JSONSchemaType<any> | any;
/**
 * Wrapper object for various ways schema can be provided.
 */
interface ProvidedSchema {
    jsonSchema?: JSONSchema;
    schema?: z$1.ZodTypeAny;
}
/**
 * Schema validation error.
 */
declare class ValidationError extends GenkitError {
    constructor({ data, errors, schema, }: {
        data: any;
        errors: ValidationErrorDetail[];
        schema: JSONSchema;
    });
}
/**
 * Converts a Zod schema into a JSON schema, utilizing an in-memory cache for known objects.
 * @param options Provide a json schema and/or zod schema. JSON schema has priority.
 * @returns A JSON schema.
 */
declare function toJsonSchema({ jsonSchema, schema, }: ProvidedSchema): JSONSchema | undefined;
/**
 * Schema validation error details.
 */
interface ValidationErrorDetail {
    path: string;
    message: string;
}
/**
 * Validation response.
 */
type ValidationResponse = {
    valid: true;
    errors: never;
} | {
    valid: false;
    errors: ErrorObject[];
};
/**
 * Validates the provided data against the provided schema.
 */
declare function validateSchema(data: unknown, options: ProvidedSchema): {
    valid: boolean;
    errors?: any[];
    schema: JSONSchema;
};
/**
 * Parses raw data object against the provided schema.
 */
declare function parseSchema<T = unknown>(data: unknown, options: ProvidedSchema): T;
/**
 * Registers provided schema as a named schema object in the Genkit registry.
 *
 * @hidden
 */
declare function defineSchema<T extends z$1.ZodTypeAny>(registry: Registry, name: string, schema: T): T;
/**
 * Registers provided JSON schema as a named schema object in the Genkit registry.
 *
 * @hidden
 */
declare function defineJsonSchema(registry: Registry, name: string, jsonSchema: JSONSchema): any;

type AsyncProvider<T> = () => Promise<T>;
/**
 * Type of a runnable action.
 */
declare const ACTION_TYPES: readonly ["custom", "dynamic-action-provider", "embedder", "evaluator", "executable-prompt", "flow", "indexer", "model", "background-model", "check-operation", "cancel-operation", "prompt", "reranker", "retriever", "tool", "util", "resource"];
type ActionType = (typeof ACTION_TYPES)[number];
declare function isActionType(value: string): value is ActionType;
/**
 * A schema is either a Zod schema or a JSON schema.
 */
interface Schema {
    schema?: z.ZodTypeAny;
    jsonSchema?: JSONSchema;
}
interface ParsedRegistryKey {
    dynamicActionHost?: string;
    actionType: ActionType;
    pluginName?: string;
    actionName: string;
}
/**
 * Parses the registry key into key parts as per the key format convention. Ex:
 *  - mcp-host:tool/my-tool
 *  - /model/googleai/gemini-2.0-flash
 *  - /prompt/my-plugin/folder/my-prompt
 *  - /util/generate
 */
declare function parseRegistryKey(registryKey: string): ParsedRegistryKey | undefined;
type ActionsRecord = Record<string, Action<z.ZodTypeAny, z.ZodTypeAny>>;
type ActionMetadataRecord = Record<string, ActionMetadata>;
/**
 * The registry is used to store and lookup actions, trace stores, flow state stores, plugins, and schemas.
 */
declare class Registry {
    private actionsById;
    private pluginsByName;
    private schemasByName;
    private valueByTypeAndName;
    private allPluginsInitialized;
    apiStability: 'stable' | 'beta';
    readonly dotprompt: Dotprompt;
    readonly parent?: Registry;
    /** Additional runtime context data for flows and tools. */
    context?: ActionContext;
    constructor(parent?: Registry);
    /**
     * Creates a new registry overlaid onto the provided registry.
     * @param parent The parent registry.
     * @returns The new overlaid registry.
     */
    static withParent(parent: Registry): Registry;
    resolveActionNames(key: string): Promise<string[]>;
    /**
     * Looks up an action in the registry.
     * @param key The key of the action to lookup.
     * @returns The action.
     */
    lookupAction<I extends z.ZodTypeAny, O extends z.ZodTypeAny, R extends Action<I, O>>(key: string): Promise<R>;
    /**
     * Looks up a background action from the registry.
     * @param key The key of the action to lookup.
     * @returns The action.
     */
    lookupBackgroundAction(key: string): Promise<BackgroundAction | undefined>;
    /**
     * Registers an action in the registry.
     * @param type The type of the action to register.
     * @param action The action to register.
     */
    registerAction<I extends z.ZodTypeAny, O extends z.ZodTypeAny>(type: ActionType, action: Action<I, O>, opts?: {
        namespace?: string;
    }): void;
    /**
     * Registers an action promise in the registry.
     */
    registerActionAsync<I extends z.ZodTypeAny, O extends z.ZodTypeAny>(type: ActionType, name: string, action: PromiseLike<Action<I, O>>, opts?: {
        namespace?: string;
    }): void;
    /**
     * Returns all actions that have been registered in the registry.
     * @returns All actions in the registry as a map of <key, action>.
     */
    listActions(): Promise<ActionsRecord>;
    /**
     * Returns all actions that are resolvable by plugins as well as those that are already
     * in the registry.
     *
     * NOTE: this method should not be used in latency sensitive code paths.
     * It may rely on "admin" API calls such as "list models", which may cause increased cold start latency.
     *
     * @returns All resolvable action metadata as a map of <key, action metadata>.
     */
    listResolvableActions(): Promise<ActionMetadataRecord>;
    /**
     * Initializes all plugins in the registry.
     */
    initializeAllPlugins(): Promise<void>;
    /**
     * Registers a plugin provider. This plugin must be initialized before it can be used by calling {@link initializePlugin} or {@link initializeAllPlugins}.
     * @param name The name of the plugin to register.
     * @param provider The plugin provider.
     */
    registerPluginProvider(name: string, provider: PluginProvider): void;
    /**
     * Looks up a plugin.
     * @param name The name of the plugin to lookup.
     * @returns The plugin provider.
     */
    lookupPlugin(name: string): PluginProvider | undefined;
    /**
     * Resolves a new Action dynamically by registering it.
     * @param pluginName The name of the plugin
     * @param actionType The type of the action
     * @param actionName The name of the action
     * @returns
     */
    resolvePluginAction(pluginName: string, actionType: ActionType, actionName: string): Promise<void>;
    getDynamicAction(key: ParsedRegistryKey): Promise<Action<z.ZodTypeAny, z.ZodTypeAny> | undefined>;
    /**
     * Initializes a plugin already registered with {@link registerPluginProvider}.
     * @param name The name of the plugin to initialize.
     * @returns The plugin.
     */
    initializePlugin(name: string): Promise<void | InitializedPlugin>;
    /**
     * Registers a schema.
     * @param name The name of the schema to register.
     * @param data The schema to register (either a Zod schema or a JSON schema).
     */
    registerSchema(name: string, data: Schema): void;
    registerValue(type: string, name: string, value: any): void;
    lookupValue<T = unknown>(type: string, key: string): Promise<T | undefined>;
    listValues<T>(type: string): Promise<Record<string, T>>;
    /**
     * Looks up a schema.
     * @param name The name of the schema to lookup.
     * @returns The schema.
     */
    lookupSchema(name: string): Schema | undefined;
}
/**
 * An object that has a reference to Genkit Registry.
 */
interface HasRegistry {
    get registry(): Registry;
}

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
 * Action metadata.
 */
interface ActionMetadata<I extends z.ZodTypeAny = z.ZodTypeAny, O extends z.ZodTypeAny = z.ZodTypeAny, S extends z.ZodTypeAny = z.ZodTypeAny> {
    actionType?: ActionType;
    name: string;
    description?: string;
    inputSchema?: I;
    inputJsonSchema?: JSONSchema7;
    outputSchema?: O;
    outputJsonSchema?: JSONSchema7;
    streamSchema?: S;
    metadata?: Record<string, any>;
}
/**
 * Results of an action run. Includes telemetry.
 */
interface ActionResult<O> {
    result: O;
    telemetry: {
        traceId: string;
        spanId: string;
    };
}
/**
 * Options (side channel) data to pass to the model.
 */
interface ActionRunOptions<S> {
    /**
     * Streaming callback (optional).
     */
    onChunk?: StreamingCallback<S>;
    /**
     * Additional runtime context data (ex. auth context data).
     */
    context?: ActionContext;
    /**
     * Additional span attributes to apply to OT spans.
     */
    telemetryLabels?: Record<string, string>;
    /**
     * Abort signal for the action request.
     */
    abortSignal?: AbortSignal;
}
/**
 * Options (side channel) data to pass to the model.
 */
interface ActionFnArg<S> {
    /**
     * Whether the caller of the action requested streaming.
     */
    streamingRequested: boolean;
    /**
     * Streaming callback (optional).
     */
    sendChunk: StreamingCallback<S>;
    /**
     * Additional runtime context data (ex. auth context data).
     */
    context?: ActionContext;
    /**
     * Trace context containing trace and span IDs.
     */
    trace: {
        traceId: string;
        spanId: string;
    };
    /**
     * Abort signal for the action request.
     */
    abortSignal: AbortSignal;
    registry?: Registry;
}
/**
 * Streaming response from an action.
 */
interface StreamingResponse<O extends z.ZodTypeAny = z.ZodTypeAny, S extends z.ZodTypeAny = z.ZodTypeAny> {
    /** Iterator over the streaming chunks. */
    stream: AsyncGenerator<z.infer<S>>;
    /** Final output of the action. */
    output: Promise<z.infer<O>>;
}
/**
 * Self-describing, validating, observable, locally and remotely callable function.
 */
type Action<I extends z.ZodTypeAny = z.ZodTypeAny, O extends z.ZodTypeAny = z.ZodTypeAny, S extends z.ZodTypeAny = z.ZodTypeAny, RunOptions extends ActionRunOptions<S> = ActionRunOptions<S>> = ((input?: z.infer<I>, options?: RunOptions) => Promise<z.infer<O>>) & {
    __action: ActionMetadata<I, O, S>;
    __registry?: Registry;
    run(input?: z.infer<I>, options?: ActionRunOptions<z.infer<S>>): Promise<ActionResult<z.infer<O>>>;
    stream(input?: z.infer<I>, opts?: ActionRunOptions<z.infer<S>>): StreamingResponse<O, S>;
};
/**
 * Action factory params.
 */
type ActionParams<I extends z.ZodTypeAny, O extends z.ZodTypeAny, S extends z.ZodTypeAny = z.ZodTypeAny> = {
    name: string | {
        pluginId: string;
        actionId: string;
    };
    description?: string;
    inputSchema?: I;
    inputJsonSchema?: JSONSchema7;
    outputSchema?: O;
    outputJsonSchema?: JSONSchema7;
    metadata?: Record<string, any>;
    use?: Middleware<z.infer<I>, z.infer<O>, z.infer<S>>[];
    streamSchema?: S;
    actionType: ActionType;
};
type ActionAsyncParams<I extends z.ZodTypeAny, O extends z.ZodTypeAny, S extends z.ZodTypeAny = z.ZodTypeAny> = ActionParams<I, O, S> & {
    fn: (input: z.infer<I>, options: ActionFnArg<z.infer<S>>) => Promise<z.infer<O>>;
};
type SimpleMiddleware<I = any, O = any> = (req: I, next: (req?: I) => Promise<O>) => Promise<O>;
type MiddlewareWithOptions<I = any, O = any, S = any> = (req: I, options: ActionRunOptions<S> | undefined, next: (req?: I, options?: ActionRunOptions<S>) => Promise<O>) => Promise<O>;
/**
 * Middleware function for actions.
 */
type Middleware<I = any, O = any, S = any> = SimpleMiddleware<I, O> | MiddlewareWithOptions<I, O, S>;
/**
 * Creates an action with provided middleware.
 */
declare function actionWithMiddleware<I extends z.ZodTypeAny, O extends z.ZodTypeAny, S extends z.ZodTypeAny = z.ZodTypeAny>(action: Action<I, O, S>, middleware: Middleware<z.infer<I>, z.infer<O>, z.infer<S>>[]): Action<I, O, S>;
/**
 * Creates an action with the provided config.
 */
declare function action<I extends z.ZodTypeAny, O extends z.ZodTypeAny, S extends z.ZodTypeAny = z.ZodTypeAny>(config: ActionParams<I, O, S>, fn: (input: z.infer<I>, options: ActionFnArg<z.infer<S>>) => Promise<z.infer<O>>): Action<I, O, z.infer<S>>;
declare function isAction(a: unknown): a is Action;
/**
 * Defines an action with the given config and registers it in the registry.
 */
declare function defineAction<I extends z.ZodTypeAny, O extends z.ZodTypeAny, S extends z.ZodTypeAny = z.ZodTypeAny>(registry: Registry, config: ActionParams<I, O, S>, fn: (input: z.infer<I>, options: ActionFnArg<z.infer<S>>) => Promise<z.infer<O>>): Action<I, O, S>;
/**
 * Defines an action with the given config promise and registers it in the registry.
 */
declare function defineActionAsync<I extends z.ZodTypeAny, O extends z.ZodTypeAny, S extends z.ZodTypeAny = z.ZodTypeAny>(registry: Registry, actionType: ActionType, name: string | {
    pluginId: string;
    actionId: string;
}, config: PromiseLike<ActionAsyncParams<I, O, S>>, onInit?: (action: Action<I, O, S>) => void): PromiseLike<Action<I, O, S>>;
type StreamingCallback<T> = (chunk: T) => void;
declare const sentinelNoopStreamingCallback: () => null;
/**
 * Executes provided function with streaming callback in async local storage which can be retrieved
 * using {@link getStreamingCallback}.
 */
declare function runWithStreamingCallback<S, O>(streamingCallback: StreamingCallback<S> | undefined, fn: () => O): O;
/**
 * Retrieves the {@link StreamingCallback} previously set by {@link runWithStreamingCallback}
 *
 * @hidden
 */
declare function getStreamingCallback<S>(): StreamingCallback<S> | undefined;
/**
 * Checks whether the caller is currently in the runtime context of an action.
 */
declare function isInRuntimeContext(): boolean;
/**
 * Execute the provided function in the action runtime context.
 */
declare function runInActionRuntimeContext<R>(fn: () => R): R;
/**
 * Execute the provided function outside the action runtime context.
 */
declare function runOutsideActionRuntimeContext<R>(fn: () => R): R;

export { type ProvidedSchema as $, type ActionMetadata as A, type BackgroundAction as B, defineActionAsync as C, type StreamingCallback as D, sentinelNoopStreamingCallback as E, runWithStreamingCallback as F, GenkitError as G, getStreamingCallback as H, isInRuntimeContext as I, type JSONSchema as J, runInActionRuntimeContext as K, runOutsideActionRuntimeContext as L, type MiddlewareWithOptions as M, type PluginProvider as N, OperationSchema as O, type Provider as P, type InitializedPlugin as Q, type Plugin as R, type StreamingResponse as S, type ActionType as T, UnstableApiError as U, Registry as V, type HasRegistry as W, lookupBackgroundAction as X, type HttpErrorWireFormat as Y, getErrorMessage as Z, getErrorStack as _, type BackgroundActionFnArg as a, ValidationError as a0, toJsonSchema as a1, type ValidationErrorDetail as a2, type ValidationResponse as a3, validateSchema as a4, parseSchema as a5, type AsyncProvider as a6, isActionType as a7, type Schema as a8, parseRegistryKey as a9, type ActionsRecord as aa, type ActionMetadataRecord as ab, backgroundAction as b, type BackgroundActionParams as c, defineBackgroundAction as d, type BackgroundActionRunOptions as e, type Operation as f, UserFacingError as g, assertUnstable as h, isBackgroundAction as i, getCallableJSON as j, getHttpStatus as k, defineJsonSchema as l, defineSchema as m, type ActionResult as n, type ActionRunOptions as o, type ActionFnArg as p, type Action as q, registerBackgroundAction as r, type ActionParams as s, type ActionAsyncParams as t, type SimpleMiddleware as u, type Middleware as v, actionWithMiddleware as w, action as x, isAction as y, defineAction as z };
