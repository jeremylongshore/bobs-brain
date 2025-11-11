"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);
var plugin_exports = {};
__export(plugin_exports, {
  backgroundModel: () => import_model.backgroundModel,
  embedder: () => import_embedder.embedder,
  embedderActionMetadata: () => import_embedder.embedderActionMetadata,
  evaluator: () => import_evaluator.evaluator,
  genkitPlugin: () => genkitPlugin,
  genkitPluginV2: () => genkitPluginV2,
  indexer: () => import_retriever.indexer,
  isPluginV2: () => isPluginV2,
  model: () => import_model.model,
  modelActionMetadata: () => import_model.modelActionMetadata,
  reranker: () => import_reranker.reranker,
  retriever: () => import_retriever.retriever
});
module.exports = __toCommonJS(plugin_exports);
var import_embedder = require("@genkit-ai/ai/embedder");
var import_evaluator = require("@genkit-ai/ai/evaluator");
var import_model = require("@genkit-ai/ai/model");
var import_reranker = require("@genkit-ai/ai/reranker");
var import_retriever = require("@genkit-ai/ai/retriever");
function genkitPlugin(pluginName, initFn, resolveFn, listActionsFn) {
  return (genkit) => ({
    name: pluginName,
    initializer: async () => {
      await initFn(genkit);
    },
    resolver: async (action, target) => {
      if (resolveFn) {
        return await resolveFn(genkit, action, target);
      }
    },
    listActions: async () => {
      if (listActionsFn) {
        return await listActionsFn();
      }
      return [];
    }
  });
}
function genkitPluginV2(options) {
  return { ...options, version: "v2" };
}
function isPluginV2(plugin) {
  return plugin.version === "v2";
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  backgroundModel,
  embedder,
  embedderActionMetadata,
  evaluator,
  genkitPlugin,
  genkitPluginV2,
  indexer,
  isPluginV2,
  model,
  modelActionMetadata,
  reranker,
  retriever
});
//# sourceMappingURL=plugin.js.map