import { Dotprompt } from "dotprompt";
import {
  runOutsideActionRuntimeContext
} from "./action.js";
import {
  lookupBackgroundAction
} from "./background-action.js";
import { isDynamicActionProvider } from "./dynamic-action-provider.js";
import { GenkitError } from "./error.js";
import { logger } from "./logging.js";
import { toJsonSchema } from "./schema.js";
const ACTION_TYPES = [
  "custom",
  "dynamic-action-provider",
  "embedder",
  "evaluator",
  "executable-prompt",
  "flow",
  "indexer",
  "model",
  "background-model",
  "check-operation",
  "cancel-operation",
  "prompt",
  "reranker",
  "retriever",
  "tool",
  "util",
  "resource"
];
function isActionType(value) {
  return ACTION_TYPES.includes(value);
}
function parsePluginName(registryKey) {
  const tokens = registryKey.split("/");
  if (tokens.length >= 4) {
    return tokens[2];
  }
  return void 0;
}
function parseRegistryKey(registryKey) {
  if (registryKey.startsWith("/dynamic-action-provider")) {
    const keyTokens = registryKey.split(":");
    const hostTokens = keyTokens[0].split("/");
    if (hostTokens.length < 3) {
      return void 0;
    }
    if (keyTokens.length < 2) {
      return {
        actionType: "dynamic-action-provider",
        actionName: hostTokens[2]
      };
    }
    const tokens2 = keyTokens[1].split("/");
    if (tokens2.length < 2 || !isActionType(tokens2[0])) {
      return void 0;
    }
    return {
      dynamicActionHost: hostTokens[2],
      actionType: tokens2[0],
      actionName: tokens2.slice(1).join("/")
    };
  }
  const tokens = registryKey.split("/");
  if (tokens.length < 3) {
    return void 0;
  }
  if (tokens.length >= 4) {
    return {
      actionType: tokens[1],
      pluginName: tokens[2],
      actionName: tokens.slice(3).join("/")
    };
  }
  return {
    actionType: tokens[1],
    actionName: tokens[2]
  };
}
class Registry {
  actionsById = {};
  pluginsByName = {};
  schemasByName = {};
  valueByTypeAndName = {};
  allPluginsInitialized = false;
  apiStability = "stable";
  dotprompt;
  parent;
  /** Additional runtime context data for flows and tools. */
  context;
  constructor(parent) {
    if (parent) {
      this.parent = parent;
      this.apiStability = parent?.apiStability;
      this.dotprompt = parent.dotprompt;
    } else {
      this.dotprompt = new Dotprompt({
        schemaResolver: async (name) => {
          const resolvedSchema = await this.lookupSchema(name);
          if (!resolvedSchema) {
            throw new GenkitError({
              message: `Schema '${name}' not found`,
              status: "NOT_FOUND"
            });
          }
          return toJsonSchema(resolvedSchema);
        }
      });
    }
  }
  /**
   * Creates a new registry overlaid onto the provided registry.
   * @param parent The parent registry.
   * @returns The new overlaid registry.
   */
  static withParent(parent) {
    return new Registry(parent);
  }
  async resolveActionNames(key) {
    const parsedKey = parseRegistryKey(key);
    if (parsedKey?.dynamicActionHost) {
      const hostId = `/dynamic-action-provider/${parsedKey.dynamicActionHost}`;
      const dap = await this.actionsById[hostId];
      if (!dap || !isDynamicActionProvider(dap)) {
        return [];
      }
      return (await dap.listActionMetadata(parsedKey.actionType, parsedKey.actionName)).map((m) => `${hostId}:${parsedKey.actionType}/${m.name}`);
    }
    if (await this.lookupAction(key)) {
      return [key];
    }
    return [];
  }
  /**
   * Looks up an action in the registry.
   * @param key The key of the action to lookup.
   * @returns The action.
   */
  async lookupAction(key) {
    const parsedKey = parseRegistryKey(key);
    if (parsedKey?.dynamicActionHost && this.actionsById[`/dynamic-action-provider/${parsedKey.dynamicActionHost}`]) {
      const action = await this.getDynamicAction(parsedKey);
      if (action) {
        return action;
      }
    }
    if (parsedKey?.pluginName && this.pluginsByName[parsedKey.pluginName]) {
      await this.initializePlugin(parsedKey.pluginName);
      if (!this.actionsById[key]) {
        await this.resolvePluginAction(
          parsedKey.pluginName,
          parsedKey.actionType,
          parsedKey.actionName
        );
      }
    }
    return await this.actionsById[key] || this.parent?.lookupAction(key);
  }
  /**
   * Looks up a background action from the registry.
   * @param key The key of the action to lookup.
   * @returns The action.
   */
  async lookupBackgroundAction(key) {
    return lookupBackgroundAction(this, key);
  }
  /**
   * Registers an action in the registry.
   * @param type The type of the action to register.
   * @param action The action to register.
   */
  registerAction(type, action, opts) {
    if (type !== action.__action.actionType) {
      throw new GenkitError({
        status: "INVALID_ARGUMENT",
        message: `action type (${type}) does not match type on action (${action.__action.actionType})`
      });
    }
    if (opts?.namespace && !action.__action.name.startsWith(`${opts.namespace}/`)) {
      action.__action.name = `${opts.namespace}/${action.__action.name}`;
    }
    const key = `/${type}/${action.__action.name}`;
    logger.debug(`registering ${key}`);
    if (this.actionsById.hasOwnProperty(key)) {
      logger.warn(
        `WARNING: ${key} already has an entry in the registry. Overwriting.`
      );
    }
    this.actionsById[key] = action;
    if (action.__registry) {
      logger.error(`ERROR: ${key} already registered.`);
    }
    action.__registry = this;
  }
  /**
   * Registers an action promise in the registry.
   */
  registerActionAsync(type, name, action, opts) {
    if (opts?.namespace && !name.startsWith(`${opts.namespace}/`)) {
      name = `${opts.namespace}/${name}`;
    }
    const key = `/${type}/${name}`;
    logger.debug(`registering ${key} (async)`);
    if (this.actionsById.hasOwnProperty(key)) {
      logger.warn(
        `WARNING: ${key} already has an entry in the registry. Overwriting.`
      );
    }
    this.actionsById[key] = action;
  }
  /**
   * Returns all actions that have been registered in the registry.
   * @returns All actions in the registry as a map of <key, action>.
   */
  async listActions() {
    await this.initializeAllPlugins();
    const actions = {};
    await Promise.all(
      Object.entries(this.actionsById).map(async ([key, action]) => {
        actions[key] = await action;
      })
    );
    return {
      ...await this.parent?.listActions(),
      ...actions
    };
  }
  /**
   * Returns all actions that are resolvable by plugins as well as those that are already
   * in the registry.
   *
   * NOTE: this method should not be used in latency sensitive code paths.
   * It may rely on "admin" API calls such as "list models", which may cause increased cold start latency.
   *
   * @returns All resolvable action metadata as a map of <key, action metadata>.
   */
  async listResolvableActions() {
    const resolvableActions = {};
    await Promise.all(
      Object.entries(this.pluginsByName).map(async ([pluginName, plugin]) => {
        if (plugin.listActions) {
          try {
            (await plugin.listActions()).forEach((meta) => {
              if (!meta.name) {
                throw new GenkitError({
                  status: "INVALID_ARGUMENT",
                  message: `Invalid metadata when listing actions from ${pluginName} - name required`
                });
              }
              if (!meta.actionType) {
                throw new GenkitError({
                  status: "INVALID_ARGUMENT",
                  message: `Invalid metadata when listing actions from ${pluginName} - actionType required`
                });
              }
              resolvableActions[`/${meta.actionType}/${meta.name}`] = meta;
            });
          } catch (e) {
            logger.error(`Error listing actions for ${pluginName}
`, e);
          }
        }
      })
    );
    for (const [key, action] of Object.entries(await this.listActions())) {
      resolvableActions[key] = action.__action;
    }
    return {
      ...await this.parent?.listResolvableActions(),
      ...resolvableActions
    };
  }
  /**
   * Initializes all plugins in the registry.
   */
  async initializeAllPlugins() {
    if (this.allPluginsInitialized) {
      return;
    }
    for (const pluginName of Object.keys(this.pluginsByName)) {
      await this.initializePlugin(pluginName);
    }
    this.allPluginsInitialized = true;
  }
  /**
   * Registers a plugin provider. This plugin must be initialized before it can be used by calling {@link initializePlugin} or {@link initializeAllPlugins}.
   * @param name The name of the plugin to register.
   * @param provider The plugin provider.
   */
  registerPluginProvider(name, provider) {
    if (this.pluginsByName[name]) {
      throw new Error(`Plugin ${name} already registered`);
    }
    this.allPluginsInitialized = false;
    let cached;
    let isInitialized = false;
    this.pluginsByName[name] = {
      name: provider.name,
      initializer: () => {
        if (!isInitialized) {
          cached = provider.initializer();
          isInitialized = true;
        }
        return cached;
      },
      resolver: async (actionType, actionName) => {
        if (provider.resolver) {
          await provider.resolver(actionType, actionName);
        }
      },
      listActions: async () => {
        if (provider.listActions) {
          return await provider.listActions();
        }
        return [];
      }
    };
  }
  /**
   * Looks up a plugin.
   * @param name The name of the plugin to lookup.
   * @returns The plugin provider.
   */
  lookupPlugin(name) {
    return this.pluginsByName[name] || this.parent?.lookupPlugin(name);
  }
  /**
   * Resolves a new Action dynamically by registering it.
   * @param pluginName The name of the plugin
   * @param actionType The type of the action
   * @param actionName The name of the action
   * @returns
   */
  async resolvePluginAction(pluginName, actionType, actionName) {
    const plugin = this.pluginsByName[pluginName];
    if (plugin) {
      return await runOutsideActionRuntimeContext(async () => {
        if (plugin.resolver) {
          await plugin.resolver(actionType, actionName);
        }
      });
    }
  }
  async getDynamicAction(key) {
    if (key.actionName.includes("*")) {
      return void 0;
    }
    const actionId = `/dynamic-action-provider/${key.dynamicActionHost}`;
    const dap = await this.actionsById[actionId];
    if (!dap || !isDynamicActionProvider(dap)) {
      return void 0;
    }
    return await dap.getAction(key.actionType, key.actionName);
  }
  /**
   * Initializes a plugin already registered with {@link registerPluginProvider}.
   * @param name The name of the plugin to initialize.
   * @returns The plugin.
   */
  async initializePlugin(name) {
    if (this.pluginsByName[name]) {
      return await runOutsideActionRuntimeContext(
        () => this.pluginsByName[name].initializer()
      );
    }
  }
  /**
   * Registers a schema.
   * @param name The name of the schema to register.
   * @param data The schema to register (either a Zod schema or a JSON schema).
   */
  registerSchema(name, data) {
    if (this.schemasByName[name]) {
      throw new Error(`Schema ${name} already registered`);
    }
    this.schemasByName[name] = data;
  }
  registerValue(type, name, value) {
    if (!this.valueByTypeAndName[type]) {
      this.valueByTypeAndName[type] = {};
    }
    this.valueByTypeAndName[type][name] = value;
  }
  async lookupValue(type, key) {
    const pluginName = parsePluginName(key);
    if (!this.valueByTypeAndName[type]?.[key] && pluginName) {
      await this.initializePlugin(pluginName);
    }
    return this.valueByTypeAndName[type]?.[key] || this.parent?.lookupValue(type, key);
  }
  async listValues(type) {
    await this.initializeAllPlugins();
    return {
      ...await this.parent?.listValues(type) || {},
      ...this.valueByTypeAndName[type] || {}
    };
  }
  /**
   * Looks up a schema.
   * @param name The name of the schema to lookup.
   * @returns The schema.
   */
  lookupSchema(name) {
    return this.schemasByName[name] || this.parent?.lookupSchema(name);
  }
}
export {
  Registry,
  isActionType,
  parseRegistryKey
};
//# sourceMappingURL=registry.mjs.map