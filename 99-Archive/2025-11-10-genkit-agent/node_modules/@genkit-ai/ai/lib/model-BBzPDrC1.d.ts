import { Action, StreamingCallback, z, SimpleMiddleware, ActionMetadata, BackgroundAction, ActionFnArg, Operation } from '@genkit-ai/core';
import { Registry } from '@genkit-ai/core/registry';
import { M as MediaPart, D as Document } from './document-SEV6zxye.js';
import { ModelInfo, GenerateActionOptionsSchema, GenerateResponseSchema, GenerateResponseChunkSchema, GenerateActionOptions, GenerateResponseData, GenerateActionOutputConfig, Part, Role, GenerateRequestSchema, GenerateRequest, GenerateResponseChunkData, MessageData, CandidateData, GenerationUsage } from './model-types.js';
import { Formatter } from './formats/types.js';
import { GenerateResponseChunk } from './generate/chunk.js';

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
 * Preprocess a GenerateRequest to download referenced http(s) media URLs and
 * inline them as data URIs.
 */
declare function downloadRequestMedia(options?: {
    maxBytes?: number;
    filter?: (part: MediaPart) => boolean;
}): ModelMiddleware;
/**
 * Validates that a GenerateRequest does not include unsupported features.
 */
declare function validateSupport(options: {
    name: string;
    supports?: ModelInfo['supports'];
}): ModelMiddleware;
/**
 * Provide a simulated system prompt for models that don't support it natively.
 */
declare function simulateSystemPrompt(options?: {
    preface: string;
    acknowledgement: string;
}): ModelMiddleware;
interface AugmentWithContextOptions {
    /** Preceding text to place before the rendered context documents. */
    preface?: string | null;
    /** A function to render a document into a text part to be included in the message. */
    itemTemplate?: (d: Document, options?: AugmentWithContextOptions) => string;
    /** The metadata key to use for citation reference. Pass `null` to provide no citations. */
    citationKey?: string | null;
}
declare const CONTEXT_PREFACE = "\n\nUse the following information to complete your task:\n\n";
declare function augmentWithContext(options?: AugmentWithContextOptions): ModelMiddleware;
interface SimulatedConstrainedGenerationOptions {
    instructionsRenderer?: (schema: Record<string, any>) => string;
}
/**
 * Model middleware that simulates constrained generation by injecting generation
 * instructions into the user message.
 */
declare function simulateConstrainedGeneration(options?: SimulatedConstrainedGenerationOptions): ModelMiddleware;

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

type GenerateAction = Action<typeof GenerateActionOptionsSchema, typeof GenerateResponseSchema, typeof GenerateResponseChunkSchema>;
/** Defines (registers) a utilty generate action. */
declare function defineGenerateAction(registry: Registry): GenerateAction;
/**
 * Encapsulates all generate logic. This is similar to `generateAction` except not an action and can take middleware.
 */
declare function generateHelper(registry: Registry, options: {
    rawRequest: GenerateActionOptions;
    middleware?: ModelMiddleware[];
    currentTurn?: number;
    messageIndex?: number;
    abortSignal?: AbortSignal;
    streamingCallback?: StreamingCallback<GenerateResponseChunk>;
}): Promise<GenerateResponseData>;
declare function shouldInjectFormatInstructions(formatConfig?: Formatter['config'], rawRequestConfig?: z.infer<typeof GenerateActionOutputConfig>): string | boolean | undefined;
declare function inferRoleFromParts(parts: Part[]): Role;

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

type ModelAction<CustomOptionsSchema extends z.ZodTypeAny = z.ZodTypeAny> = Action<typeof GenerateRequestSchema, typeof GenerateResponseSchema, typeof GenerateResponseChunkSchema> & {
    __configSchema: CustomOptionsSchema;
};
type BackgroundModelAction<CustomOptionsSchema extends z.ZodTypeAny = z.ZodTypeAny> = BackgroundAction<typeof GenerateRequestSchema, typeof GenerateResponseSchema> & {
    __configSchema: CustomOptionsSchema;
};
type ModelMiddleware = SimpleMiddleware<z.infer<typeof GenerateRequestSchema>, z.infer<typeof GenerateResponseSchema>>;
type DefineModelOptions<CustomOptionsSchema extends z.ZodTypeAny = z.ZodTypeAny> = {
    name: string;
    /** Known version names for this model, e.g. `gemini-1.0-pro-001`. */
    versions?: string[];
    /** Capabilities this model supports. */
    supports?: ModelInfo['supports'];
    /** Custom options schema for this model. */
    configSchema?: CustomOptionsSchema;
    /** Descriptive name for this model e.g. 'Google AI - Gemini Pro'. */
    label?: string;
    /** Middleware to be used with this model. */
    use?: ModelMiddleware[];
};
declare function model<CustomOptionsSchema extends z.ZodTypeAny = z.ZodTypeAny>(options: DefineModelOptions<CustomOptionsSchema>, runner: (request: GenerateRequest<CustomOptionsSchema>, options: ActionFnArg<GenerateResponseChunkData>) => Promise<GenerateResponseData>): ModelAction<CustomOptionsSchema>;
/**
 * Defines a new model and adds it to the registry.
 */
declare function defineModel<CustomOptionsSchema extends z.ZodTypeAny = z.ZodTypeAny>(registry: Registry, options: {
    apiVersion: 'v2';
} & DefineModelOptions<CustomOptionsSchema>, runner: (request: GenerateRequest<CustomOptionsSchema>, options: ActionFnArg<GenerateResponseChunkData>) => Promise<GenerateResponseData>): ModelAction<CustomOptionsSchema>;
/**
 * Defines a new model and adds it to the registry.
 */
declare function defineModel<CustomOptionsSchema extends z.ZodTypeAny = z.ZodTypeAny>(registry: Registry, options: DefineModelOptions<CustomOptionsSchema>, runner: (request: GenerateRequest<CustomOptionsSchema>, streamingCallback?: StreamingCallback<GenerateResponseChunkData>) => Promise<GenerateResponseData>): ModelAction<CustomOptionsSchema>;
type DefineBackgroundModelOptions<CustomOptionsSchema extends z.ZodTypeAny = z.ZodTypeAny> = DefineModelOptions<CustomOptionsSchema> & {
    start: (request: GenerateRequest<CustomOptionsSchema>) => Promise<Operation<GenerateResponseData>>;
    check: (operation: Operation<GenerateResponseData>) => Promise<Operation<GenerateResponseData>>;
    cancel?: (operation: Operation<GenerateResponseData>) => Promise<Operation<GenerateResponseData>>;
};
/**
 * Defines a new model that runs in the background.
 */
declare function defineBackgroundModel<CustomOptionsSchema extends z.ZodTypeAny = z.ZodTypeAny>(registry: Registry, options: DefineBackgroundModelOptions<CustomOptionsSchema>): BackgroundModelAction<CustomOptionsSchema>;
/**
 * Defines a new model that runs in the background.
 */
declare function backgroundModel<CustomOptionsSchema extends z.ZodTypeAny = z.ZodTypeAny>(options: DefineBackgroundModelOptions<CustomOptionsSchema>): BackgroundModelAction<CustomOptionsSchema>;
interface ModelReference<CustomOptions extends z.ZodTypeAny> {
    name: string;
    configSchema?: CustomOptions;
    info?: ModelInfo;
    version?: string;
    config?: z.infer<CustomOptions>;
    withConfig(cfg: z.infer<CustomOptions>): ModelReference<CustomOptions>;
    withVersion(version: string): ModelReference<CustomOptions>;
}
/**
 * Packages model information into ActionMetadata object.
 */
declare function modelActionMetadata({ name, info, configSchema, background, }: {
    name: string;
    info?: ModelInfo;
    configSchema?: z.ZodTypeAny;
    background?: boolean;
}): ActionMetadata;
/** Cretes a model reference. */
declare function modelRef<CustomOptionsSchema extends z.ZodTypeAny = z.ZodTypeAny>(options: Omit<ModelReference<CustomOptionsSchema>, 'withConfig' | 'withVersion'> & {
    namespace?: string;
}): ModelReference<CustomOptionsSchema>;
/**
 * Calculates basic usage statistics from the given model inputs and outputs.
 */
declare function getBasicUsageStats(input: MessageData[], response: MessageData | CandidateData[]): GenerationUsage;
type ModelArgument<CustomOptions extends z.ZodTypeAny = z.ZodTypeAny> = ModelAction<CustomOptions> | ModelReference<CustomOptions> | string;
interface ResolvedModel<CustomOptions extends z.ZodTypeAny = z.ZodTypeAny> {
    modelAction: ModelAction;
    config?: z.infer<CustomOptions>;
    version?: string;
}
declare function resolveModel<C extends z.ZodTypeAny = z.ZodTypeAny>(registry: Registry, model: ModelArgument<C> | undefined, options?: {
    warnDeprecated?: boolean;
}): Promise<ResolvedModel<C>>;

export { type AugmentWithContextOptions as A, type BackgroundModelAction as B, CONTEXT_PREFACE as C, type DefineModelOptions as D, type GenerateAction as G, type ModelArgument as M, type ResolvedModel as R, type SimulatedConstrainedGenerationOptions as S, modelRef as a, type ModelReference as b, type ModelMiddleware as c, downloadRequestMedia as d, augmentWithContext as e, simulateConstrainedGeneration as f, defineGenerateAction as g, generateHelper as h, shouldInjectFormatInstructions as i, inferRoleFromParts as j, type ModelAction as k, model as l, modelActionMetadata as m, defineModel as n, type DefineBackgroundModelOptions as o, defineBackgroundModel as p, backgroundModel as q, getBasicUsageStats as r, simulateSystemPrompt as s, resolveModel as t, validateSupport as v };
