import { defineAction } from "./action.js";
class SimpleCache {
  value;
  expiresAt;
  ttlMillis;
  dap;
  dapFn;
  fetchPromise = null;
  constructor(dap, config, dapFn) {
    this.dap = dap;
    this.dapFn = dapFn;
    this.ttlMillis = !config.cacheConfig?.ttlMillis ? 3 * 1e3 : config.cacheConfig?.ttlMillis;
  }
  async getOrFetch() {
    const isStale = !this.value || !this.expiresAt || this.ttlMillis < 0 || Date.now() > this.expiresAt;
    if (!isStale) {
      return this.value;
    }
    if (!this.fetchPromise) {
      this.fetchPromise = (async () => {
        try {
          this.value = await this.dapFn();
          this.expiresAt = Date.now() + this.ttlMillis;
          this.dap.run(this.value);
          return this.value;
        } catch (error) {
          console.error("Error fetching Dynamic Action Provider value:", error);
          this.invalidate();
          throw error;
        } finally {
          this.fetchPromise = null;
        }
      })();
    }
    return await this.fetchPromise;
  }
  invalidate() {
    this.value = void 0;
  }
}
function isDynamicActionProvider(obj) {
  return obj.__action?.metadata?.type == "dynamic-action-provider";
}
function transformDapValue(value) {
  const metadata = {};
  for (const key of Object.keys(value)) {
    metadata[key] = value[key].map((a) => {
      return a.__action;
    });
  }
  return metadata;
}
function defineDynamicActionProvider(registry, config, fn) {
  let cfg;
  if (typeof config == "string") {
    cfg = { name: config };
  } else {
    cfg = { ...config };
  }
  const a = defineAction(
    registry,
    {
      ...cfg,
      actionType: "dynamic-action-provider",
      metadata: { ...cfg.metadata || {}, type: "dynamic-action-provider" }
    },
    async (i, _options) => {
      return transformDapValue(i);
    }
  );
  implementDap(a, cfg, fn);
  return a;
}
function implementDap(dap, config, dapFn) {
  dap.__cache = new SimpleCache(dap, config, dapFn);
  dap.invalidateCache = () => {
    dap.__cache.invalidate();
  };
  dap.getAction = async (actionType, actionName) => {
    const result = await dap.__cache.getOrFetch();
    if (result[actionType]) {
      return result[actionType].find((t) => t.__action.name == actionName);
    }
    return void 0;
  };
  dap.listActionMetadata = async (actionType, actionName) => {
    const result = await dap.__cache.getOrFetch();
    if (!result[actionType]) {
      return [];
    }
    const metadata = result[actionType].map((a) => a.__action);
    if (actionName == "*") {
      return metadata;
    }
    if (actionName.endsWith("*")) {
      const prefix = actionName.slice(0, -1);
      return metadata.filter((m) => m.name.startsWith(prefix));
    }
    return metadata.filter((m) => m.name == actionName);
  };
}
export {
  defineDynamicActionProvider,
  isDynamicActionProvider
};
//# sourceMappingURL=dynamic-action-provider.mjs.map