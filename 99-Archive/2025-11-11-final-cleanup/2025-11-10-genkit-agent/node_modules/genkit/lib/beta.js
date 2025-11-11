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
var __reExport = (target, mod, secondTarget) => (__copyProps(target, mod, "default"), secondTarget && __copyProps(secondTarget, mod, "default"));
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);
var beta_exports = {};
__export(beta_exports, {
  GenkitBeta: () => import_genkit_beta.GenkitBeta,
  genkit: () => import_genkit_beta.genkit
});
module.exports = __toCommonJS(beta_exports);
__reExport(beta_exports, require("./common.js"), module.exports);
var import_genkit_beta = require("./genkit-beta.js");
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  GenkitBeta,
  genkit,
  ...require("./common.js")
});
//# sourceMappingURL=beta.js.map