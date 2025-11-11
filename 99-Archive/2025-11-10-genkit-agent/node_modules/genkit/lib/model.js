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
var model_exports = {};
__export(model_exports, {
  CandidateErrorSchema: () => import_model.CandidateErrorSchema,
  CandidateSchema: () => import_model.CandidateSchema,
  CustomPartSchema: () => import_model.CustomPartSchema,
  DataPartSchema: () => import_model.DataPartSchema,
  GenerateRequestSchema: () => import_model.GenerateRequestSchema,
  GenerateResponseChunkSchema: () => import_model.GenerateResponseChunkSchema,
  GenerateResponseSchema: () => import_model.GenerateResponseSchema,
  GenerationCommonConfigDescriptions: () => import_model.GenerationCommonConfigDescriptions,
  GenerationCommonConfigSchema: () => import_model.GenerationCommonConfigSchema,
  GenerationUsageSchema: () => import_model.GenerationUsageSchema,
  MediaPartSchema: () => import_model.MediaPartSchema,
  MessageSchema: () => import_model.MessageSchema,
  ModelInfoSchema: () => import_model.ModelInfoSchema,
  ModelRequestSchema: () => import_model.ModelRequestSchema,
  ModelResponseSchema: () => import_model.ModelResponseSchema,
  PartSchema: () => import_model.PartSchema,
  RoleSchema: () => import_model.RoleSchema,
  TextPartSchema: () => import_model.TextPartSchema,
  ToolDefinitionSchema: () => import_model.ToolDefinitionSchema,
  ToolRequestPartSchema: () => import_model.ToolRequestPartSchema,
  ToolResponsePartSchema: () => import_model.ToolResponsePartSchema,
  getBasicUsageStats: () => import_model.getBasicUsageStats,
  modelRef: () => import_model.modelRef,
  simulateConstrainedGeneration: () => import_model.simulateConstrainedGeneration
});
module.exports = __toCommonJS(model_exports);
var import_model = require("@genkit-ai/ai/model");
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  CandidateErrorSchema,
  CandidateSchema,
  CustomPartSchema,
  DataPartSchema,
  GenerateRequestSchema,
  GenerateResponseChunkSchema,
  GenerateResponseSchema,
  GenerationCommonConfigDescriptions,
  GenerationCommonConfigSchema,
  GenerationUsageSchema,
  MediaPartSchema,
  MessageSchema,
  ModelInfoSchema,
  ModelRequestSchema,
  ModelResponseSchema,
  PartSchema,
  RoleSchema,
  TextPartSchema,
  ToolDefinitionSchema,
  ToolRequestPartSchema,
  ToolResponsePartSchema,
  getBasicUsageStats,
  modelRef,
  simulateConstrainedGeneration
});
//# sourceMappingURL=model.js.map