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
var middleware_exports = {};
__export(middleware_exports, {
  augmentWithContext: () => import_middleware.augmentWithContext,
  downloadRequestMedia: () => import_middleware.downloadRequestMedia,
  simulateSystemPrompt: () => import_middleware.simulateSystemPrompt,
  validateSupport: () => import_middleware.validateSupport
});
module.exports = __toCommonJS(middleware_exports);
var import_middleware = require("@genkit-ai/ai/model/middleware");
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  augmentWithContext,
  downloadRequestMedia,
  simulateSystemPrompt,
  validateSupport
});
//# sourceMappingURL=middleware.js.map