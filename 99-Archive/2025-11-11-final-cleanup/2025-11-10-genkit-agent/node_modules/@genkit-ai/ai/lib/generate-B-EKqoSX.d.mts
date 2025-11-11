import { z, JSONSchema7, ActionContext, Action, ActionRunOptions, StreamingCallback, GenkitError, Operation } from '@genkit-ai/core';
import { Registry } from '@genkit-ai/core/registry';
import { b as DocumentData, l as ToolRequestPart, m as ToolResponsePart } from './document-SEV6zxye.mjs';
import { GenerateResponseChunk } from './generate/chunk.mjs';
import { GenerateResponse } from './generate/response.mjs';
import { M as ModelArgument, c as ModelMiddleware } from './model-aQReSBZ2.mjs';
import { ResourceArgument } from './resource.mjs';
import { Part, MessageData, GenerateRequestSchema, GenerateResponseSchema, GenerateResponseChunkSchema, ToolDefinition, GenerationCommonConfigSchema, GenerateRequest, GenerateResponseData, GenerateActionOptions } from './model-types.mjs';

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
 * Prompt action.
 */
type PromptAction<I extends z.ZodTypeAny = z.ZodTypeAny> = Action<I, typeof GenerateRequestSchema, z.ZodNever> & {
    __action: {
        metadata: {
            type: 'prompt';
        };
    };
    __executablePrompt: ExecutablePrompt<I>;
};
declare function isPromptAction(action: Action): action is PromptAction;
/**
 * Prompt action.
 */
type ExecutablePromptAction<I extends z.ZodTypeAny = z.ZodTypeAny> = Action<I, typeof GenerateResponseSchema, typeof GenerateResponseChunkSchema> & {
    __action: {
        metadata: {
            type: 'executablePrompt';
        };
    };
    __executablePrompt: ExecutablePrompt<I>;
};
/**
 * Configuration for a prompt action.
 */
interface PromptConfig<I extends z.ZodTypeAny = z.ZodTypeAny, O extends z.ZodTypeAny = z.ZodTypeAny, CustomOptions extends z.ZodTypeAny = z.ZodTypeAny> {
    name: string;
    variant?: string;
    model?: ModelArgument<CustomOptions>;
    config?: z.infer<CustomOptions>;
    description?: string;
    input?: {
        schema?: I;
        jsonSchema?: JSONSchema7;
    };
    system?: string | Part | Part[] | PartsResolver<z.infer<I>>;
    prompt?: string | Part | Part[] | PartsResolver<z.infer<I>>;
    messages?: string | MessageData[] | MessagesResolver<z.infer<I>>;
    docs?: DocumentData[] | DocsResolver<z.infer<I>>;
    output?: OutputOptions<O>;
    maxTurns?: number;
    returnToolRequests?: boolean;
    metadata?: Record<string, any>;
    tools?: ToolArgument[];
    toolChoice?: ToolChoice;
    use?: ModelMiddleware[];
    context?: ActionContext;
}
/**
 * Generate options of a prompt.
 */
type PromptGenerateOptions<O extends z.ZodTypeAny = z.ZodTypeAny, CustomOptions extends z.ZodTypeAny = z.ZodTypeAny> = Omit<GenerateOptions<O, CustomOptions>, 'prompt' | 'system'>;
/**
 * A prompt that can be executed as a function.
 */
interface ExecutablePrompt<I = undefined, O extends z.ZodTypeAny = z.ZodTypeAny, CustomOptions extends z.ZodTypeAny = z.ZodTypeAny> {
    /** Prompt reference. */
    ref: {
        name: string;
        metadata?: Record<string, any>;
    };
    /**
     * Generates a response by rendering the prompt template with given user input and then calling the model.
     *
     * @param input Prompt inputs.
     * @param opt Options for the prompt template, including user input variables and custom model configuration options.
     * @returns the model response as a promise of `GenerateStreamResponse`.
     */
    (input?: I, opts?: PromptGenerateOptions<O, CustomOptions>): Promise<GenerateResponse<z.infer<O>>>;
    /**
     * Generates a response by rendering the prompt template with given user input and then calling the model.
     * @param input Prompt inputs.
     * @param opt Options for the prompt template, including user input variables and custom model configuration options.
     * @returns the model response as a promise of `GenerateStreamResponse`.
     */
    stream(input?: I, opts?: PromptGenerateOptions<O, CustomOptions>): GenerateStreamResponse<z.infer<O>>;
    /**
     * Renders the prompt template based on user input.
     *
     * @param opt Options for the prompt template, including user input variables and custom model configuration options.
     * @returns a `GenerateOptions` object to be used with the `generate()` function from @genkit-ai/ai.
     */
    render(input?: I, opts?: PromptGenerateOptions<O, CustomOptions>): Promise<GenerateOptions<O, CustomOptions>>;
    /**
     * Returns the prompt usable as a tool.
     */
    asTool(): Promise<ToolAction>;
}
type PartsResolver<I, S = any> = (input: I, options: {
    state?: S;
    context: ActionContext;
}) => Part[] | Promise<string | Part | Part[]>;
type MessagesResolver<I, S = any> = (input: I, options: {
    history?: MessageData[];
    state?: S;
    context: ActionContext;
}) => MessageData[] | Promise<MessageData[]>;
type DocsResolver<I, S = any> = (input: I, options: {
    context: ActionContext;
    state?: S;
}) => DocumentData[] | Promise<DocumentData[]>;
/**
 * Defines a prompt which can be used to generate content or render a request.
 *
 * @returns The new `ExecutablePrompt`.
 */
declare function definePrompt<I extends z.ZodTypeAny = z.ZodTypeAny, O extends z.ZodTypeAny = z.ZodTypeAny, CustomOptions extends z.ZodTypeAny = z.ZodTypeAny>(registry: Registry, options: PromptConfig<I, O, CustomOptions>): ExecutablePrompt<z.infer<I>, O, CustomOptions>;
/**
 * Checks whether the provided object is an executable prompt.
 */
declare function isExecutablePrompt(obj: any): obj is ExecutablePrompt;
declare function loadPromptFolder(registry: Registry, dir: string | undefined, ns: string): void;
declare function loadPromptFolderRecursively(registry: Registry, dir: string, ns: string, subDir: string): void;
declare function definePartial(registry: Registry, name: string, source: string): void;
declare function defineHelper(registry: Registry, name: string, fn: Handlebars.HelperDelegate): void;
declare function prompt<I = undefined, O extends z.ZodTypeAny = z.ZodTypeAny, CustomOptions extends z.ZodTypeAny = z.ZodTypeAny>(registry: Registry, name: string, options?: {
    variant?: string;
    dir?: string;
}): Promise<ExecutablePrompt<I, O, CustomOptions>>;

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

interface Resumable<I extends z.ZodTypeAny = z.ZodTypeAny, O extends z.ZodTypeAny = z.ZodTypeAny> {
    /**
     * respond constructs a tool response corresponding to the provided interrupt tool request
     * using the provided reply data, validating it against the output schema of the tool if
     * it exists.
     *
     * @beta
     */
    respond(
    /** The interrupt tool request to which you want to respond. */
    interrupt: ToolRequestPart, 
    /**
     * The data with which you want to respond. Must conform to a tool's output schema or an
     * interrupt's input schema.
     **/
    outputData: z.infer<O>, options?: {
        metadata?: Record<string, any>;
    }): ToolResponsePart;
    /**
     * restart constructs a tool request corresponding to the provided interrupt tool request
     * that will then re-trigger the tool after e.g. a user confirms. The `resumedMetadata`
     * supplied to this method will be passed to the tool to allow for custom handling of
     * restart logic.
     *
     * @param interrupt The interrupt tool request you want to restart.
     * @param resumedMetadata The metadata you want to provide to the tool to aide in reprocessing. Defaults to `true` if none is supplied.
     * @param options Additional options for restarting the tool.
     *
     * @beta
     */
    restart(interrupt: ToolRequestPart, resumedMetadata?: any, options?: {
        /**
         * Replace the existing input arguments to the tool with different ones, for example
         * if the user revised an action before confirming. When input is replaced, the existing
         * tool request will be amended in the message history.
         **/
        replaceInput?: z.infer<I>;
    }): ToolRequestPart;
}
/**
 * An action with a `tool` type.
 */
type ToolAction<I extends z.ZodTypeAny = z.ZodTypeAny, O extends z.ZodTypeAny = z.ZodTypeAny> = Action<I, O, z.ZodTypeAny, ToolRunOptions> & Resumable<I, O> & {
    __action: {
        metadata: {
            type: 'tool';
        };
    };
};
/**
 * A dynamic action with a `tool` type. Dynamic tools are detached actions -- not associated with any registry.
 */
type DynamicToolAction<I extends z.ZodTypeAny = z.ZodTypeAny, O extends z.ZodTypeAny = z.ZodTypeAny> = Action<I, O, z.ZodTypeAny, ToolRunOptions> & {
    /** @deprecated no-op, for backwards compatibility only. */
    attach(registry: Registry): ToolAction<I, O>;
} & Resumable<I, O> & {
    __action: {
        metadata: {
            type: 'tool';
        };
    };
};
interface ToolRunOptions extends ActionRunOptions<z.ZodTypeAny> {
    /**
     * If resumed is supplied to a tool at runtime, that means that it was previously interrupted and this is a second
     * @beta
     **/
    resumed?: boolean | Record<string, any>;
    /** The metadata from the tool request that triggered this run. */
    metadata?: Record<string, any>;
}
/**
 * Configuration for a tool.
 */
interface ToolConfig<I extends z.ZodTypeAny, O extends z.ZodTypeAny> {
    /** Unique name of the tool to use as a key in the registry. */
    name: string;
    /** Description of the tool. This is passed to the model to help understand what the tool is used for. */
    description: string;
    /** Input Zod schema. Mutually exclusive with `inputJsonSchema`. */
    inputSchema?: I;
    /** Input JSON schema. Mutually exclusive with `inputSchema`. */
    inputJsonSchema?: JSONSchema7;
    /** Output Zod schema. Mutually exclusive with `outputJsonSchema`. */
    outputSchema?: O;
    /** Output JSON schema. Mutually exclusive with `outputSchema`. */
    outputJsonSchema?: JSONSchema7;
    /** Metadata to be passed to the tool. */
    metadata?: Record<string, any>;
}
/**
 * A reference to a tool in the form of a name, definition, or the action itself.
 */
type ToolArgument<I extends z.ZodTypeAny = z.ZodTypeAny, O extends z.ZodTypeAny = z.ZodTypeAny> = string | ToolAction<I, O> | Action<I, O> | ExecutablePrompt<any, any, any>;
/**
 * Converts an action to a tool action by setting the appropriate metadata.
 */
declare function asTool<I extends z.ZodTypeAny, O extends z.ZodTypeAny>(registry: Registry, action: Action<I, O>): ToolAction<I, O>;
/**
 * Resolves a mix of various formats of tool references to a list of tool actions by looking them up in the registry.
 */
declare function resolveTools<O extends z.ZodTypeAny = z.ZodTypeAny, CustomOptions extends z.ZodTypeAny = z.ZodTypeAny>(registry: Registry, tools?: (ToolArgument | ToolDefinition)[]): Promise<ToolAction[]>;
declare function lookupToolByName(registry: Registry, name: string): Promise<ToolAction>;
/**
 * Converts a tool action to a definition of the tool to be passed to a model.
 */
declare function toToolDefinition(tool: Action<z.ZodTypeAny, z.ZodTypeAny>): ToolDefinition;
interface ToolFnOptions {
    /**
     * A function that can be called during tool execution that will result in the tool
     * getting interrupted (immediately) and tool request returned to the upstream caller.
     */
    interrupt: (metadata?: Record<string, any>) => never;
    context: ActionContext;
}
type ToolFn<I extends z.ZodTypeAny, O extends z.ZodTypeAny> = (input: z.infer<I>, ctx: ToolFnOptions & ToolRunOptions) => Promise<z.infer<O>>;
/**
 * Defines a tool.
 *
 * A tool is an action that can be passed to a model to be called automatically if it so chooses.
 */
declare function defineTool<I extends z.ZodTypeAny, O extends z.ZodTypeAny>(registry: Registry, config: ToolConfig<I, O>, fn: ToolFn<I, O>): ToolAction<I, O>;
/** InterruptConfig defines the options for configuring an interrupt. */
type InterruptConfig<I extends z.ZodTypeAny = z.ZodTypeAny, R extends z.ZodTypeAny = z.ZodTypeAny> = ToolConfig<I, R> & {
    /** requestMetadata adds additional `interrupt` metadata to the `toolRequest` generated by the interrupt */
    requestMetadata?: Record<string, any> | ((input: z.infer<I>) => Record<string, any> | Promise<Record<string, any>>);
};
declare function isToolRequest(part: Part): part is ToolRequestPart;
declare function isToolResponse(part: Part): part is ToolResponsePart;
declare function isDynamicTool(t: unknown): t is ToolAction;
declare function interrupt<I extends z.ZodTypeAny, O extends z.ZodTypeAny>(config: InterruptConfig<I, O>): ToolAction<I, O>;
declare function defineInterrupt<I extends z.ZodTypeAny, O extends z.ZodTypeAny>(registry: Registry, config: InterruptConfig<I, O>): ToolAction<I, O>;
/**
 * Thrown when tools execution is interrupted. It's meant to be caugh by the framework, not public API.
 */
declare class ToolInterruptError extends Error {
    readonly metadata?: Record<string, any> | undefined;
    constructor(metadata?: Record<string, any> | undefined);
}
/**
 * Defines a dynamic tool. Dynamic tools are just like regular tools but will not be registered in the
 * Genkit registry and can be defined dynamically at runtime.
 */
declare function tool<I extends z.ZodTypeAny, O extends z.ZodTypeAny>(config: ToolConfig<I, O>, fn?: ToolFn<I, O>): ToolAction<I, O>;
/**
 * Defines a dynamic tool. Dynamic tools are just like regular tools but will not be registered in the
 * Genkit registry and can be defined dynamically at runtime.
 *
 * @deprecated renamed to {@link tool}.
 */
declare function dynamicTool<I extends z.ZodTypeAny, O extends z.ZodTypeAny>(config: ToolConfig<I, O>, fn?: ToolFn<I, O>): DynamicToolAction<I, O>;

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

/** Specifies how tools should be called by the model. */
type ToolChoice = 'auto' | 'required' | 'none';
interface OutputOptions<O extends z.ZodTypeAny = z.ZodTypeAny> {
    format?: string;
    contentType?: string;
    instructions?: boolean | string;
    schema?: O;
    jsonSchema?: any;
    constrained?: boolean;
}
/** ResumeOptions configure how to resume generation after an interrupt. */
interface ResumeOptions {
    /**
     * respond should contain a single or list of `toolResponse` parts corresponding
     * to interrupt `toolRequest` parts from the most recent model message. Each
     * entry must have a matching `name` and `ref` (if supplied) for its `toolRequest`
     * counterpart.
     *
     * Tools have a `.respond` helper method to construct a reply ToolResponse and validate
     * the data against its schema. Call `myTool.respond(interruptToolRequest, yourReplyData)`.
     */
    respond?: ToolResponsePart | ToolResponsePart[];
    /**
     * restart will run a tool again with additionally supplied metadata passed through as
     * a `resumed` option in the second argument. This allows for scenarios like conditionally
     * requesting confirmation of an LLM's tool request.
     *
     * Tools have a `.restart` helper method to construct a restart ToolRequest. Call
     * `myTool.restart(interruptToolRequest, resumeMetadata)`.
     *
     */
    restart?: ToolRequestPart | ToolRequestPart[];
    /** Additional metadata to annotate the created tool message with in the "resume" key. */
    metadata?: Record<string, any>;
}
interface GenerateOptions<O extends z.ZodTypeAny = z.ZodTypeAny, CustomOptions extends z.ZodTypeAny = z.ZodTypeAny> {
    /** A model name (e.g. `vertexai/gemini-1.0-pro`) or reference. */
    model?: ModelArgument<CustomOptions>;
    /** The system prompt to be included in the generate request. Can be a string for a simple text prompt or one or more parts for multi-modal prompts (subject to model support). */
    system?: string | Part | Part[];
    /** The prompt for which to generate a response. Can be a string for a simple text prompt or one or more parts for multi-modal prompts. */
    prompt?: string | Part | Part[];
    /** Retrieved documents to be used as context for this generation. */
    docs?: DocumentData[];
    /** Conversation messages (history) for multi-turn prompting when supported by the underlying model. */
    messages?: (MessageData & {
        content: Part[] | string | (string | Part)[];
    })[];
    /** List of registered tool names or actions to treat as a tool for this generation if supported by the underlying model. */
    tools?: ToolArgument[];
    /** List of dynamic resources to be made available to this generate request. */
    resources?: ResourceArgument[];
    /** Specifies how tools should be called by the model.  */
    toolChoice?: ToolChoice;
    /** Configuration for the generation request. */
    config?: z.infer<CustomOptions>;
    /** Configuration for the desired output of the request. Defaults to the model's default output if unspecified. */
    output?: OutputOptions<O>;
    /**
     * resume provides convenient capabilities for continuing generation
     * after an interrupt is triggered. Example:
     *
     * ```ts
     * const myInterrupt = ai.defineInterrupt({...});
     *
     * const response = await ai.generate({
     *   tools: [myInterrupt],
     *   prompt: "Call myInterrupt",
     * });
     *
     * const interrupt = response.interrupts[0];
     *
     * const resumedResponse = await ai.generate({
     *   messages: response.messages,
     *   resume: myInterrupt.respond(interrupt, {note: "this is the reply data"}),
     * });
     * ```
     *
     * @beta
     */
    resume?: ResumeOptions;
    /** When true, return tool calls for manual processing instead of automatically resolving them. */
    returnToolRequests?: boolean;
    /** Maximum number of tool call iterations that can be performed in a single generate call (default 5). */
    maxTurns?: number;
    /** When provided, models supporting streaming will call the provided callback with chunks as generation progresses. */
    onChunk?: StreamingCallback<GenerateResponseChunk>;
    /**
     * When provided, models supporting streaming will call the provided callback with chunks as generation progresses.
     *
     * @deprecated use {@link onChunk} instead.
     */
    streamingCallback?: StreamingCallback<GenerateResponseChunk>;
    /** Middleware to be used with this model call. */
    use?: ModelMiddleware[];
    /** Additional context (data, like e.g. auth) to be passed down to tools, prompts and other sub actions. */
    context?: ActionContext;
    /** Abort signal for the generate request. */
    abortSignal?: AbortSignal;
    /** Custom step name for this generate call to display in trace views. Defaults to "generate". */
    stepName?: string;
    /**
     * Additional metadata describing the GenerateOptions, used by tooling. If
     * this is an instance of a rendered dotprompt, will contain any prompt
     * metadata contained in the original frontmatter.
     **/
    metadata?: Record<string, any>;
}
declare function toGenerateRequest(registry: Registry, options: GenerateOptions): Promise<GenerateRequest>;
declare class GenerationResponseError extends GenkitError {
    detail: {
        response: GenerateResponse;
        [otherDetails: string]: any;
    };
    constructor(response: GenerateResponse<any>, message: string, status?: GenkitError['status'], detail?: Record<string, any>);
}
/** A GenerationBlockedError is thrown when a generation is blocked. */
declare class GenerationBlockedError extends GenerationResponseError {
}
/**
 * Generate calls a generative model based on the provided prompt and configuration. If
 * `history` is provided, the generation will include a conversation history in its
 * request. If `tools` are provided, the generate method will automatically resolve
 * tool calls returned from the model unless `returnToolRequests` is set to `true`.
 *
 * See `GenerateOptions` for detailed information about available options.
 *
 * @param options The options for this generation request.
 * @returns The generated response based on the provided parameters.
 */
declare function generate<O extends z.ZodTypeAny = z.ZodTypeAny, CustomOptions extends z.ZodTypeAny = typeof GenerationCommonConfigSchema>(registry: Registry, options: GenerateOptions<O, CustomOptions> | PromiseLike<GenerateOptions<O, CustomOptions>>): Promise<GenerateResponse<z.infer<O>>>;
declare function generateOperation<O extends z.ZodTypeAny = z.ZodTypeAny, CustomOptions extends z.ZodTypeAny = typeof GenerationCommonConfigSchema>(registry: Registry, options: GenerateOptions<O, CustomOptions> | PromiseLike<GenerateOptions<O, CustomOptions>>): Promise<Operation<GenerateResponseData>>;
declare function toGenerateActionOptions<O extends z.ZodTypeAny = z.ZodTypeAny, CustomOptions extends z.ZodTypeAny = typeof GenerationCommonConfigSchema>(registry: Registry, options: GenerateOptions<O, CustomOptions>): Promise<GenerateActionOptions>;
type GenerateStreamOptions<O extends z.ZodTypeAny = z.ZodTypeAny, CustomOptions extends z.ZodTypeAny = typeof GenerationCommonConfigSchema> = Omit<GenerateOptions<O, CustomOptions>, 'streamingCallback'>;
interface GenerateStreamResponse<O extends z.ZodTypeAny = z.ZodTypeAny> {
    get stream(): AsyncIterable<GenerateResponseChunk>;
    get response(): Promise<GenerateResponse<O>>;
}
declare function generateStream<O extends z.ZodTypeAny = z.ZodTypeAny, CustomOptions extends z.ZodTypeAny = typeof GenerationCommonConfigSchema>(registry: Registry, options: GenerateOptions<O, CustomOptions> | PromiseLike<GenerateOptions<O, CustomOptions>>): GenerateStreamResponse<O>;
declare function tagAsPreamble(msgs?: MessageData[]): MessageData[] | undefined;

export { isPromptAction as A, type ExecutablePromptAction as B, type PartsResolver as C, type DocsResolver as D, type ExecutablePrompt as E, loadPromptFolderRecursively as F, GenerationBlockedError as G, type Resumable as H, type InterruptConfig as I, type DynamicToolAction as J, resolveTools as K, lookupToolByName as L, type MessagesResolver as M, toToolDefinition as N, type OutputOptions as O, type PromptAction as P, type ToolFnOptions as Q, type ResumeOptions as R, type ToolFn as S, type ToolChoice as T, isToolRequest as U, isToolResponse as V, isDynamicTool as W, tool as X, dynamicTool as Y, toGenerateActionOptions as Z, GenerationResponseError as a, generateOperation as b, generateStream as c, toGenerateRequest as d, type GenerateOptions as e, type GenerateStreamOptions as f, generate as g, type GenerateStreamResponse as h, defineHelper as i, definePartial as j, definePrompt as k, isExecutablePrompt as l, loadPromptFolder as m, type PromptConfig as n, type PromptGenerateOptions as o, prompt as p, ToolInterruptError as q, asTool as r, defineInterrupt as s, tagAsPreamble as t, defineTool as u, interrupt as v, type ToolAction as w, type ToolArgument as x, type ToolConfig as y, type ToolRunOptions as z };
