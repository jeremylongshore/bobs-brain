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
var tool_exports = {};
__export(tool_exports, {
  asTool: () => import_tool.asTool,
  dynamicTool: () => import_tool.dynamicTool,
  interrupt: () => import_tool.interrupt,
  toToolDefinition: () => import_tool.toToolDefinition,
  tool: () => import_tool.tool
});
module.exports = __toCommonJS(tool_exports);
var import_tool = require("@genkit-ai/ai/tool");
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  asTool,
  dynamicTool,
  interrupt,
  toToolDefinition,
  tool
});
//# sourceMappingURL=tool.js.map