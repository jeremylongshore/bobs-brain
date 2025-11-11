import { z } from '@genkit-ai/core';
import { e as GenerateOptions, E as ExecutablePrompt, f as GenerateStreamOptions, h as GenerateStreamResponse } from './generate-B-EKqoSX.mjs';
import { MessageData, GenerationCommonConfigSchema, Part } from './model-types.mjs';
import { Registry } from '@genkit-ai/core/registry';
import { GenerateResponse } from './generate/response.mjs';
import './document-SEV6zxye.mjs';
import './generate/chunk.mjs';
import './model-aQReSBZ2.mjs';
import './formats/types.mjs';
import './message.mjs';
import './resource.mjs';

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

type BaseGenerateOptions<O extends z.ZodTypeAny = z.ZodTypeAny, CustomOptions extends z.ZodTypeAny = z.ZodTypeAny> = Omit<GenerateOptions<O, CustomOptions>, 'prompt'>;
interface SessionOptions<S = any> {
    /** Session store implementation for persisting the session state. */
    store?: SessionStore<S>;
    /** Initial state of the session.  */
    initialState?: S;
    /** Custom session Id. */
    sessionId?: string;
}
/**
 * Session encapsulates a statful execution environment for chat.
 * Chat session executed within a session in this environment will have acesss to
 * session session convesation history.
 *
 * ```ts
 * const ai = genkit({...});
 * const chat = ai.chat(); // create a Session
 * let response = await chat.send('hi'); // session/history aware conversation
 * response = await chat.send('tell me a story');
 * ```
 */
declare class Session<S = any> {
    readonly registry: Registry;
    readonly id: string;
    private sessionData?;
    private store;
    constructor(registry: Registry, options?: {
        id?: string;
        stateSchema?: S;
        sessionData?: SessionData<S>;
        store?: SessionStore<S>;
    });
    get state(): S | undefined;
    /**
     * Update session state data.
     */
    updateState(data: S): Promise<void>;
    /**
     * Update messages for a given thread.
     */
    updateMessages(thread: string, messages: MessageData[]): Promise<void>;
    /**
     * Create a chat session with the provided options.
     *
     * ```ts
     * const session = ai.createSession({});
     * const chat = session.chat({
     *   system: 'talk like a pirate',
     * })
     * let response = await chat.send('tell me a joke');
     * response = await chat.send('another one');
     * ```
     */
    chat<I>(options?: ChatOptions<I, S>): Chat;
    /**
     * Create a chat session with the provided preamble.
     *
     * ```ts
     * const triageAgent = ai.definePrompt({
     *   system: 'help the user triage a problem',
     * })
     * const session = ai.createSession({});
     * const chat = session.chat(triageAgent);
     * const { text } = await chat.send('my phone feels hot');
     * ```
     */
    chat<I>(preamble: ExecutablePrompt<I>, options?: ChatOptions<I, S>): Chat;
    /**
     * Craete a separate chat conversation ("thread") within the given preamble.
     *
     * ```ts
     * const session = ai.createSession({});
     * const lawyerChat = session.chat('lawyerThread', {
     *   system: 'talk like a lawyer',
     * });
     * const pirateChat = session.chat('pirateThread', {
     *   system: 'talk like a pirate',
     * });
     * await lawyerChat.send('tell me a joke');
     * await pirateChat.send('tell me a joke');
     * ```
     */
    chat<I>(threadName: string, preamble: ExecutablePrompt<I>, options?: ChatOptions<I, S>): Chat;
    /**
     * Craete a separate chat conversation ("thread").
     *
     * ```ts
     * const session = ai.createSession({});
     * const lawyerChat = session.chat('lawyerThread', {
     *   system: 'talk like a lawyer',
     * });
     * const pirateChat = session.chat('pirateThread', {
     *   system: 'talk like a pirate',
     * });
     * await lawyerChat.send('tell me a joke');
     * await pirateChat.send('tell me a joke');
     * ```
     */
    chat<I>(threadName: string, options?: ChatOptions<I, S>): Chat;
    /**
     * Executes provided function within this session context allowing calling
     * `ai.currentSession().state`
     */
    run<O>(fn: () => O): O;
    toJSON(): SessionData<S> | undefined;
}
interface SessionData<S = any> {
    id: string;
    state?: S;
    threads?: Record<string, MessageData[]>;
}
/**
 * Executes provided function within the provided session state.
 */
declare function runWithSession<S = any, O = any>(registry: Registry, session: Session<S>, fn: () => O): O;
/** Returns the current session. */
declare function getCurrentSession<S = any>(registry: Registry): Session<S> | undefined;
/** Throw when session state errors occur, ex. missing state, etc. */
declare class SessionError extends Error {
    constructor(msg: string);
}
/** Session store persists session data such as state and chat messages. */
interface SessionStore<S = any> {
    get(sessionId: string): Promise<SessionData<S> | undefined>;
    save(sessionId: string, data: Omit<SessionData<S>, 'id'>): Promise<void>;
}
declare function inMemorySessionStore(): InMemorySessionStore<any>;
declare class InMemorySessionStore<S = any> implements SessionStore<S> {
    private data;
    get(sessionId: string): Promise<SessionData<S> | undefined>;
    save(sessionId: string, sessionData: SessionData<S>): Promise<void>;
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

declare const MAIN_THREAD = "main";
declare const SESSION_ID_ATTR: string;
declare const THREAD_NAME_ATTR: string;
type ChatGenerateOptions<O extends z.ZodTypeAny = z.ZodTypeAny, CustomOptions extends z.ZodTypeAny = z.ZodTypeAny> = GenerateOptions<O, CustomOptions>;
interface PromptRenderOptions<I> {
    input?: I;
}
type ChatOptions<I = undefined, S = any> = (PromptRenderOptions<I> | BaseGenerateOptions) & {
    store?: SessionStore<S>;
    sessionId?: string;
};
/**
 * Chat encapsulates a statful execution environment for chat.
 * Chat session executed within a session in this environment will have acesss to
 * session convesation history.
 *
 * ```ts
 * const ai = genkit({...});
 * const chat = ai.chat(); // create a Chat
 * let response = await chat.send('hi, my name is Genkit');
 * response = await chat.send('what is my name?'); // chat history aware conversation
 * ```
 */
declare class Chat {
    readonly session: Session;
    private requestBase?;
    readonly sessionId: string;
    private _messages?;
    private threadName;
    constructor(session: Session, requestBase: Promise<BaseGenerateOptions>, options: {
        id: string;
        thread: string;
        messages?: MessageData[];
    });
    send<O extends z.ZodTypeAny = z.ZodTypeAny, CustomOptions extends z.ZodTypeAny = typeof GenerationCommonConfigSchema>(options: string | Part[] | ChatGenerateOptions<O, CustomOptions>): Promise<GenerateResponse<z.infer<O>>>;
    sendStream<O extends z.ZodTypeAny = z.ZodTypeAny, CustomOptions extends z.ZodTypeAny = typeof GenerationCommonConfigSchema>(options: string | Part[] | GenerateStreamOptions<O, CustomOptions>): GenerateStreamResponse<z.infer<O>>;
    get messages(): MessageData[];
    private updateMessages;
}

export { type BaseGenerateOptions, type ChatGenerateOptions as C, MAIN_THREAD as M, type PromptRenderOptions as P, SESSION_ID_ATTR as S, Session, type SessionData, SessionError, type SessionOptions, type SessionStore, THREAD_NAME_ATTR as T, type ChatOptions as a, Chat as b, getCurrentSession, inMemorySessionStore, runWithSession };
