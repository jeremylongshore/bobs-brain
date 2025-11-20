import { embedder, embedderActionMetadata } from "@genkit-ai/ai/embedder";
import { evaluator } from "@genkit-ai/ai/evaluator";
import {
  backgroundModel,
  model,
  modelActionMetadata
} from "@genkit-ai/ai/model";
import { reranker } from "@genkit-ai/ai/reranker";
import { indexer, retriever } from "@genkit-ai/ai/retriever";
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
export {
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
};
//# sourceMappingURL=plugin.mjs.map