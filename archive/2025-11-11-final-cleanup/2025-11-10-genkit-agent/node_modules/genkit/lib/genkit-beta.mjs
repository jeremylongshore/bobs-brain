import {
  defineInterrupt,
  defineResource,
  generateOperation,
  isExecutablePrompt
} from "@genkit-ai/ai";
import { defineFormat } from "@genkit-ai/ai/formats";
import {
  getCurrentSession,
  Session,
  SessionError
} from "@genkit-ai/ai/session";
import { v4 as uuidv4 } from "uuid";
import { Genkit } from "./genkit";
function genkit(options) {
  return new GenkitBeta(options);
}
class GenkitBeta extends Genkit {
  constructor(options) {
    super(options);
    this.registry.apiStability = "beta";
  }
  /**
   * Create a chat session with the provided options.
   *
   * ```ts
   * const chat = ai.chat({
   *   system: 'talk like a pirate',
   * })
   * let response = await chat.send('tell me a joke')
   * response = await chat.send('another one')
   * ```
   *
   * @beta
   */
  chat(preambleOrOptions, maybeOptions) {
    let options;
    let preamble;
    if (maybeOptions) {
      options = maybeOptions;
    }
    if (preambleOrOptions) {
      if (isExecutablePrompt(preambleOrOptions)) {
        preamble = preambleOrOptions;
      } else {
        options = preambleOrOptions;
      }
    }
    const session = this.createSession();
    if (preamble) {
      return session.chat(preamble, options);
    }
    return session.chat(options);
  }
  /**
   * Create a session for this environment.
   */
  createSession(options) {
    const sessionId = options?.sessionId?.trim() || uuidv4();
    const sessionData = {
      id: sessionId,
      state: options?.initialState
    };
    return new Session(this.registry, {
      id: sessionId,
      sessionData,
      store: options?.store
    });
  }
  /**
   * Loads a session from the store.
   *
   * @beta
   */
  async loadSession(sessionId, options) {
    if (!options.store) {
      throw new Error("options.store is required");
    }
    const sessionData = await options.store.get(sessionId);
    return new Session(this.registry, {
      id: sessionId,
      sessionData,
      store: options.store
    });
  }
  /**
   * Gets the current session from async local storage.
   *
   * @beta
   */
  currentSession() {
    const currentSession = getCurrentSession(this.registry);
    if (!currentSession) {
      throw new SessionError("not running within a session");
    }
    return currentSession;
  }
  /**
   * Defines and registers a custom model output formatter.
   *
   * Here's an example of a custom JSON output formatter:
   *
   * ```ts
   * import { extractJson } from 'genkit/extract';
   *
   * ai.defineFormat(
   *   { name: 'customJson' },
   *   (schema) => {
   *     let instructions: string | undefined;
   *     if (schema) {
   *       instructions = `Output should be in JSON format and conform to the following schema:
   * \`\`\`
   * ${JSON.stringify(schema)}
   * \`\`\`
   * `;
   *     }
   *     return {
   *       parseChunk: (chunk) => extractJson(chunk.accumulatedText),
   *       parseMessage: (message) => extractJson(message.text),
   *       instructions,
   *     };
   *   }
   * );
   *
   * const { output } = await ai.generate({
   *   prompt: 'Invent a menu item for a pirate themed restaurant.',
   *   output: { format: 'customJson', schema: MenuItemSchema },
   * });
   * ```
   *
   * @beta
   */
  defineFormat(options, handler) {
    return defineFormat(this.registry, options, handler);
  }
  /**
   * Defines and registers an interrupt.
   *
   * Interrupts are special tools that halt model processing and return control back to the caller. Interrupts make it simpler to implement
   * "human-in-the-loop" and out-of-band processing patterns that require waiting on external actions to complete.
   *
   * @beta
   */
  defineInterrupt(config) {
    return defineInterrupt(this.registry, config);
  }
  /**
   * Starts a generate operation for long running generation models, typically for
   * video and complex audio generation.
   *
   * See {@link GenerateOptions} for detailed information about available options.
   *
   * ```ts
   * const operation = await ai.generateOperation({
   *   model: googleAI.model('veo-2.0-generate-001'),
   *   prompt: 'A banana riding a bicycle.',
   * });
   * ```
   *
   * The status of the operation and final result can be obtained using {@link Genkit.checkOperation}.
   */
  generateOperation(opts) {
    return generateOperation(this.registry, opts);
  }
  /**
   * Defines a resource. Resources can then be accessed from a generate call.
   *
   * ```ts
   * ai.defineResource({
   *   uri: 'my://resource/{param}',
   *   description: 'provides my resource',
   * }, async ({param}) => {
   *   return [{ text: `resource ${param}` }]
   * });
   *
   * await ai.generate({
   *   prompt: [{ resource: 'my://resource/value' }]
   * })
   */
  defineResource(opts, fn) {
    return defineResource(this.registry, opts, fn);
  }
}
export {
  GenkitBeta,
  genkit
};
//# sourceMappingURL=genkit-beta.mjs.map