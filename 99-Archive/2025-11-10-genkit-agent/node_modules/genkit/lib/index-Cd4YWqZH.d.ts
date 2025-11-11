import { ModelArgument, ToolConfig, ToolAction, GenerateRequest, GenerateResponseData, ExecutablePrompt, PromptConfig, RetrieverInfo, RetrieverAction, Document, EmbedderInfo, BaseDataPointSchema, EmbedderParams, Embedding, EvaluatorParams, EvalResponses, RerankerParams, RankedDocument, IndexerParams, RetrieverParams, GenerateResponse, Part, GenerationCommonConfigSchema, GenerateOptions, GenerateStreamResponse } from '@genkit-ai/ai';
import '@genkit-ai/ai/chat';
import '@genkit-ai/ai/session';
import { ToolFn } from '@genkit-ai/ai/tool';
import { ActionMetadata, Action, BackgroundAction, ActionContext, z, FlowConfig, FlowFn, DapConfig, DapFn, DynamicActionProviderAction, JSONSchema, ActionFnArg, StreamingCallback, Operation } from '@genkit-ai/core';
import * as _genkit_ai_ai_reranker from '@genkit-ai/ai/reranker';
import { RerankerInfo, RerankerFn } from '@genkit-ai/ai/reranker';
import { EmbedderFn, EmbedderAction, EmbedderArgument, EmbeddingBatch } from '@genkit-ai/ai/embedder';
import { BaseEvalDataPointSchema, EvaluatorFn, EvaluatorAction } from '@genkit-ai/ai/evaluator';
import { DefineModelOptions, GenerateResponseChunkData, ModelAction, DefineBackgroundModelOptions, BackgroundModelAction } from '@genkit-ai/ai/model';
import { RetrieverFn, SimpleRetrieverOptions, IndexerFn, IndexerAction, DocumentData } from '@genkit-ai/ai/retriever';
import { ActionType, HasRegistry, Registry } from '@genkit-ai/core/registry';

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

interface PluginProvider {
    name: string;
    initializer: () => void | Promise<void>;
    resolver?: (action: ActionType, target: string) => Promise<void>;
    listActions?: () => Promise<ActionMetadata[]>;
}
type ResolvableAction = Action | BackgroundAction;
interface GenkitPluginV2 {
    version: 'v2';
    name: string;
    init?: () => ResolvableAction[] | Promise<ResolvableAction[]>;
    resolve?: (actionType: ActionType, name: string) => ResolvableAction | undefined | Promise<ResolvableAction | undefined>;
    list?: () => ActionMetadata[] | Promise<ActionMetadata[]>;
}
type GenkitPlugin = (genkit: Genkit) => PluginProvider;
type PluginInit = (genkit: Genkit) => void | Promise<void>;
type PluginActionResolver = (genkit: Genkit, action: ActionType, target: string) => Promise<void>;
/**
 * Defines a Genkit plugin.
 */
declare function genkitPlugin<T extends PluginInit>(pluginName: string, initFn: T, resolveFn?: PluginActionResolver, listActionsFn?: () => Promise<ActionMetadata[]>): GenkitPlugin;
declare function genkitPluginV2(options: Omit<GenkitPluginV2, 'version'>): GenkitPluginV2;
declare function isPluginV2(plugin: unknown): plugin is GenkitPluginV2;

/**
 * @deprecated use `ai.definePrompt({messages: fn})`
 */
type PromptFn<I extends z.ZodTypeAny = z.ZodTypeAny, CustomOptionsSchema extends z.ZodTypeAny = z.ZodTypeAny> = (input: z.infer<I>) => Promise<GenerateRequest<CustomOptionsSchema>>;
/**
 * Options for initializing Genkit.
 */
interface GenkitOptions {
    /** List of plugins to load. */
    plugins?: (GenkitPlugin | GenkitPluginV2)[];
    /** Directory where dotprompts are stored. */
    promptDir?: string;
    /** Default model to use if no model is specified. */
    model?: ModelArgument<any>;
    /** Additional runtime context data for flows and tools. */
    context?: ActionContext;
    /** Display name that will be shown in developer tooling. */
    name?: string;
    /** Additional attribution information to include in the x-goog-api-client header. */
    clientHeader?: string;
}
/**
 * `Genkit` encapsulates a single Genkit instance including the {@link Registry}, {@link ReflectionServer}, {@link FlowServer}, and configuration.
 *
 * Do not instantiate this class directly. Use {@link genkit}.
 *
 * Registry keeps track of actions, flows, tools, and many other components. Reflection server exposes an API to inspect the registry and trigger executions of actions in the registry. Flow server exposes flows as HTTP endpoints for production use.
 *
 * There may be multiple Genkit instances in a single codebase.
 */
declare class Genkit implements HasRegistry {
    /** Developer-configured options. */
    readonly options: GenkitOptions;
    /** Registry instance that is exclusively modified by this Genkit instance. */
    readonly registry: Registry;
    /** Reflection server for this registry. May be null if not started. */
    private reflectionServer;
    /** List of flows that have been registered in this instance. */
    readonly flows: Action<any, any, any>[];
    get apiStability(): "stable" | "beta";
    constructor(options?: GenkitOptions);
    /**
     * Defines and registers a flow function.
     */
    defineFlow<I extends z.ZodTypeAny = z.ZodTypeAny, O extends z.ZodTypeAny = z.ZodTypeAny, S extends z.ZodTypeAny = z.ZodTypeAny>(config: FlowConfig<I, O, S> | string, fn: FlowFn<I, O, S>): Action<I, O, S>;
    /**
     * Defines and registers a tool.
     *
     * Tools can be passed to models by name or value during `generate` calls to be called automatically based on the prompt and situation.
     */
    defineTool<I extends z.ZodTypeAny, O extends z.ZodTypeAny>(config: ToolConfig<I, O>, fn: ToolFn<I, O>): ToolAction<I, O>;
    /**
     * Defines a dynamic tool. Dynamic tools are just like regular tools ({@link Genkit.defineTool}) but will not be registered in the
     * Genkit registry and can be defined dynamically at runtime.
     */
    dynamicTool<I extends z.ZodTypeAny, O extends z.ZodTypeAny>(config: ToolConfig<I, O>, fn?: ToolFn<I, O>): ToolAction<I, O>;
    /**
     * Defines and registers a dynamic action provider (e.g. mcp host)
     */
    defineDynamicActionProvider(config: DapConfig | string, fn: DapFn): DynamicActionProviderAction;
    /**
     * Defines and registers a schema from a Zod schema.
     *
     * Defined schemas can be referenced by `name` in prompts in place of inline schemas.
     */
    defineSchema<T extends z.ZodTypeAny>(name: string, schema: T): T;
    /**
     * Defines and registers a schema from a JSON schema.
     *
     * Defined schemas can be referenced by `name` in prompts in place of inline schemas.
     */
    defineJsonSchema(name: string, jsonSchema: JSONSchema): any;
    /**
     * Defines a new model and adds it to the registry.
     */
    defineModel<CustomOptionsSchema extends z.ZodTypeAny = z.ZodTypeAny>(options: {
        apiVersion: 'v2';
    } & DefineModelOptions<CustomOptionsSchema>, runner: (request: GenerateRequest<CustomOptionsSchema>, options: ActionFnArg<GenerateResponseChunkData>) => Promise<GenerateResponseData>): ModelAction<CustomOptionsSchema>;
    /**
     * Defines a new model and adds it to the registry.
     */
    defineModel<CustomOptionsSchema extends z.ZodTypeAny = z.ZodTypeAny>(options: DefineModelOptions<CustomOptionsSchema>, runner: (request: GenerateRequest<CustomOptionsSchema>, streamingCallback?: StreamingCallback<GenerateResponseChunkData>) => Promise<GenerateResponseData>): ModelAction<CustomOptionsSchema>;
    /**
     * Defines a new background model and adds it to the registry.
     */
    defineBackgroundModel<CustomOptionsSchema extends z.ZodTypeAny = z.ZodTypeAny>(options: DefineBackgroundModelOptions<CustomOptionsSchema>): BackgroundModelAction<CustomOptionsSchema>;
    /**
     * Looks up a prompt by `name` (and optionally `variant`). Can be used to lookup
     * .prompt files or prompts previously defined with {@link Genkit.definePrompt}
     */
    prompt<I extends z.ZodTypeAny = z.ZodTypeAny, O extends z.ZodTypeAny = z.ZodTypeAny, CustomOptions extends z.ZodTypeAny = z.ZodTypeAny>(name: string, options?: {
        variant?: string;
    }): ExecutablePrompt<z.infer<I>, O, CustomOptions>;
    private wrapExecutablePromptPromise;
    /**
     * Defines and registers a prompt based on a function.
     *
     * This is an alternative to defining and importing a .prompt file, providing
     * the most advanced control over how the final request to the model is made.
     *
     * @param options - Prompt metadata including model, model params,
     * input/output schemas, etc
     * @param fn - A function that returns a {@link GenerateRequest}. Any config
     * parameters specified by the {@link GenerateRequest} will take precedence
     * over any parameters specified by `options`.
     *
     * ```ts
     * const hi = ai.definePrompt(
     *   {
     *     name: 'hi',
     *     input: {
     *       schema: z.object({
     *         name: z.string(),
     *       }),
     *     },
     *     config: {
     *       temperature: 1,
     *     },
     *   },
     *   async (input) => {
     *     return {
     *       messages: [ { role: 'user', content: [{ text: `hi ${input.name}` }] } ],
     *     };
     *   }
     * );
     * const { text } = await hi({ name: 'Genkit' });
     * ```
     */
    definePrompt<I extends z.ZodTypeAny = z.ZodTypeAny, O extends z.ZodTypeAny = z.ZodTypeAny, CustomOptions extends z.ZodTypeAny = z.ZodTypeAny>(options: PromptConfig<I, O, CustomOptions>, 
    /** @deprecated use `options.messages` with a template string instead. */
    templateOrFn?: string | PromptFn<I>): ExecutablePrompt<z.infer<I>, O, CustomOptions>;
    /**
     * Creates a retriever action for the provided {@link RetrieverFn} implementation.
     */
    defineRetriever<OptionsType extends z.ZodTypeAny = z.ZodTypeAny>(options: {
        name: string;
        configSchema?: OptionsType;
        info?: RetrieverInfo;
    }, runner: RetrieverFn<OptionsType>): RetrieverAction<OptionsType>;
    /**
     * defineSimpleRetriever makes it easy to map existing data into documents that
     * can be used for prompt augmentation.
     *
     * @param options Configuration options for the retriever.
     * @param handler A function that queries a datastore and returns items from which to extract documents.
     * @returns A Genkit retriever.
     */
    defineSimpleRetriever<C extends z.ZodTypeAny = z.ZodTypeAny, R = any>(options: SimpleRetrieverOptions<C, R>, handler: (query: Document, config: z.infer<C>) => Promise<R[]>): RetrieverAction<C>;
    /**
     * Creates an indexer action for the provided {@link IndexerFn} implementation.
     */
    defineIndexer<IndexerOptions extends z.ZodTypeAny>(options: {
        name: string;
        embedderInfo?: EmbedderInfo;
        configSchema?: IndexerOptions;
    }, runner: IndexerFn<IndexerOptions>): IndexerAction<IndexerOptions>;
    /**
     * Creates evaluator action for the provided {@link EvaluatorFn} implementation.
     */
    defineEvaluator<DataPoint extends typeof BaseDataPointSchema = typeof BaseDataPointSchema, EvalDataPoint extends typeof BaseEvalDataPointSchema = typeof BaseEvalDataPointSchema, EvaluatorOptions extends z.ZodTypeAny = z.ZodTypeAny>(options: {
        name: string;
        displayName: string;
        definition: string;
        dataPointType?: DataPoint;
        configSchema?: EvaluatorOptions;
        isBilled?: boolean;
    }, runner: EvaluatorFn<EvalDataPoint, EvaluatorOptions>): EvaluatorAction;
    /**
     * Creates embedder model for the provided {@link EmbedderFn} model implementation.
     */
    defineEmbedder<ConfigSchema extends z.ZodTypeAny = z.ZodTypeAny>(options: {
        name: string;
        configSchema?: ConfigSchema;
        info?: EmbedderInfo;
    }, runner: EmbedderFn<ConfigSchema>): EmbedderAction<ConfigSchema>;
    /**
     * create a handlebars helper (https://handlebarsjs.com/guide/block-helpers.html) to be used in dotprompt templates.
     */
    defineHelper(name: string, fn: Handlebars.HelperDelegate): void;
    /**
     * Creates a handlebars partial (https://handlebarsjs.com/guide/partials.html) to be used in dotprompt templates.
     */
    definePartial(name: string, source: string): void;
    /**
     *  Creates a reranker action for the provided {@link RerankerFn} implementation.
     */
    defineReranker<OptionsType extends z.ZodTypeAny = z.ZodTypeAny>(options: {
        name: string;
        configSchema?: OptionsType;
        info?: RerankerInfo;
    }, runner: RerankerFn<OptionsType>): _genkit_ai_ai_reranker.RerankerAction<OptionsType>;
    /**
     * Embeds the given `content` using the specified `embedder`.
     */
    embed<CustomOptions extends z.ZodTypeAny>(params: EmbedderParams<CustomOptions>): Promise<Embedding[]>;
    /**
     * A veneer for interacting with embedder models in bulk.
     */
    embedMany<ConfigSchema extends z.ZodTypeAny = z.ZodTypeAny>(params: {
        embedder: EmbedderArgument<ConfigSchema>;
        content: string[] | DocumentData[];
        metadata?: Record<string, unknown>;
        options?: z.infer<ConfigSchema>;
    }): Promise<EmbeddingBatch>;
    /**
     * Evaluates the given `dataset` using the specified `evaluator`.
     */
    evaluate<DataPoint extends typeof BaseDataPointSchema = typeof BaseDataPointSchema, CustomOptions extends z.ZodTypeAny = z.ZodTypeAny>(params: EvaluatorParams<DataPoint, CustomOptions>): Promise<EvalResponses>;
    /**
     * Reranks documents from a {@link RerankerArgument} based on the provided query.
     */
    rerank<CustomOptions extends z.ZodTypeAny>(params: RerankerParams<CustomOptions>): Promise<Array<RankedDocument>>;
    /**
     * Indexes `documents` using the provided `indexer`.
     */
    index<CustomOptions extends z.ZodTypeAny>(params: IndexerParams<CustomOptions>): Promise<void>;
    /**
     * Retrieves documents from the `retriever` based on the provided `query`.
     */
    retrieve<CustomOptions extends z.ZodTypeAny>(params: RetrieverParams<CustomOptions>): Promise<Array<Document>>;
    /**
     * Make a generate call to the default model with a simple text prompt.
     *
     * ```ts
     * const ai = genkit({
     *   plugins: [googleAI()],
     *   model: gemini15Flash, // default model
     * })
     *
     * const { text } = await ai.generate('hi');
     * ```
     */
    generate<O extends z.ZodTypeAny = z.ZodTypeAny>(strPrompt: string): Promise<GenerateResponse<z.infer<O>>>;
    /**
     * Make a generate call to the default model with a multipart request.
     *
     * ```ts
     * const ai = genkit({
     *   plugins: [googleAI()],
     *   model: gemini15Flash, // default model
     * })
     *
     * const { text } = await ai.generate([
     *   { media: {url: 'http://....'} },
     *   { text: 'describe this image' }
     * ]);
     * ```
     */
    generate<O extends z.ZodTypeAny = z.ZodTypeAny>(parts: Part[]): Promise<GenerateResponse<z.infer<O>>>;
    /**
     * Generate calls a generative model based on the provided prompt and configuration. If
     * `messages` is provided, the generation will include a conversation history in its
     * request. If `tools` are provided, the generate method will automatically resolve
     * tool calls returned from the model unless `returnToolRequests` is set to `true`.
     *
     * See {@link GenerateOptions} for detailed information about available options.
     *
     * ```ts
     * const ai = genkit({
     *   plugins: [googleAI()],
     * })
     *
     * const { text } = await ai.generate({
     *   system: 'talk like a pirate',
     *   prompt: [
     *     { media: { url: 'http://....' } },
     *     { text: 'describe this image' }
     *   ],
     *   messages: conversationHistory,
     *   tools: [ userInfoLookup ],
     *   model: gemini15Flash,
     * });
     * ```
     */
    generate<O extends z.ZodTypeAny = z.ZodTypeAny, CustomOptions extends z.ZodTypeAny = typeof GenerationCommonConfigSchema>(opts: GenerateOptions<O, CustomOptions> | PromiseLike<GenerateOptions<O, CustomOptions>>): Promise<GenerateResponse<z.infer<O>>>;
    /**
     * Make a streaming generate call to the default model with a simple text prompt.
     *
     * ```ts
     * const ai = genkit({
     *   plugins: [googleAI()],
     *   model: gemini15Flash, // default model
     * })
     *
     * const { response, stream } = ai.generateStream('hi');
     * for await (const chunk of stream) {
     *   console.log(chunk.text);
     * }
     * console.log((await response).text);
     * ```
     */
    generateStream<O extends z.ZodTypeAny = z.ZodTypeAny>(strPrompt: string): GenerateStreamResponse<z.infer<O>>;
    /**
     * Make a streaming generate call to the default model with a multipart request.
     *
     * ```ts
     * const ai = genkit({
     *   plugins: [googleAI()],
     *   model: gemini15Flash, // default model
     * })
     *
     * const { response, stream } = ai.generateStream([
     *   { media: {url: 'http://....'} },
     *   { text: 'describe this image' }
     * ]);
     * for await (const chunk of stream) {
     *   console.log(chunk.text);
     * }
     * console.log((await response).text);
     * ```
     */
    generateStream<O extends z.ZodTypeAny = z.ZodTypeAny>(parts: Part[]): GenerateStreamResponse<z.infer<O>>;
    /**
     * Streaming generate calls a generative model based on the provided prompt and configuration. If
     * `messages` is provided, the generation will include a conversation history in its
     * request. If `tools` are provided, the generate method will automatically resolve
     * tool calls returned from the model unless `returnToolRequests` is set to `true`.
     *
     * See {@link GenerateOptions} for detailed information about available options.
     *
     * ```ts
     * const ai = genkit({
     *   plugins: [googleAI()],
     * })
     *
     * const { response, stream } = ai.generateStream({
     *   system: 'talk like a pirate',
     *   prompt: [
     *     { media: { url: 'http://....' } },
     *     { text: 'describe this image' }
     *   ],
     *   messages: conversationHistory,
     *   tools: [ userInfoLookup ],
     *   model: gemini15Flash,
     * });
     * for await (const chunk of stream) {
     *   console.log(chunk.text);
     * }
     * console.log((await response).text);
     * ```
     */
    generateStream<O extends z.ZodTypeAny = z.ZodTypeAny, CustomOptions extends z.ZodTypeAny = typeof GenerationCommonConfigSchema>(parts: GenerateOptions<O, CustomOptions> | PromiseLike<GenerateOptions<O, CustomOptions>>): GenerateStreamResponse<z.infer<O>>;
    /**
     * Checks the status of of a given operation. Returns a new operation which will contain the updated status.
     *
     * ```ts
     * let operation = await ai.generateOperation({
     *   model: googleAI.model('veo-2.0-generate-001'),
     *   prompt: 'A banana riding a bicycle.',
     * });
     *
     * while (!operation.done) {
     *   operation = await ai.checkOperation(operation!);
     *   await new Promise((resolve) => setTimeout(resolve, 5000));
     * }
     * ```
     *
     * @param operation
     * @returns
     */
    checkOperation<T>(operation: Operation<T>): Promise<Operation<T>>;
    /**
     * A flow step that executes the provided function. Each run step is recorded separately in the trace.
     *
     * ```ts
     * ai.defineFlow('hello', async() => {
     *   await ai.run('step1', async () => {
     *     // ... step 1
     *   });
     *   await ai.run('step2', async () => {
     *     // ... step 2
     *   });
     *   return result;
     * })
     * ```
     */
    run<T>(name: string, func: () => Promise<T>): Promise<T>;
    /**
     * A flow step that executes the provided function. Each run step is recorded separately in the trace.
     *
     * ```ts
     * ai.defineFlow('hello', async() => {
     *   await ai.run('step1', async () => {
     *     // ... step 1
     *   });
     *   await ai.run('step2', async () => {
     *     // ... step 2
     *   });
     *   return result;
     * })
     */
    run<T>(name: string, input: any, func: (input?: any) => Promise<T>): Promise<T>;
    /**
     * Returns current action (or flow) invocation context. Can be used to access things like auth
     * data set by HTTP server frameworks. If invoked outside of an action (e.g. flow or tool) will
     * return `undefined`.
     */
    currentContext(): ActionContext | undefined;
    /**
     * Configures the Genkit instance.
     */
    private configure;
    /**
     * Stops all servers.
     */
    stopServers(): Promise<void>;
}
/**
 * Initializes Genkit with a set of options.
 *
 * This will create a new Genkit registry, register the provided plugins, stores, and other configuration. This
 * should be called before any flows are registered.
 */
declare function genkit(options: GenkitOptions): Genkit;
declare function __disableReflectionApi(): void;

export { Genkit as G, type PluginProvider as P, type ResolvableAction as R, __disableReflectionApi as _, type GenkitOptions as a, type GenkitPluginV2 as b, type GenkitPlugin as c, type PluginInit as d, type PluginActionResolver as e, genkitPluginV2 as f, genkitPlugin as g, type PromptFn as h, isPluginV2 as i, genkit as j };
