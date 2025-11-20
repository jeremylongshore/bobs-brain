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
var utils_exports = {};
__export(utils_exports, {
  deleteUndefinedProps: () => deleteUndefinedProps,
  featureMetadataPrefix: () => featureMetadataPrefix,
  getCurrentEnv: () => getCurrentEnv,
  isDevEnv: () => isDevEnv,
  stripUndefinedProps: () => stripUndefinedProps
});
module.exports = __toCommonJS(utils_exports);
function deleteUndefinedProps(obj) {
  for (const prop in obj) {
    if (obj[prop] === void 0) {
      delete obj[prop];
    } else {
      if (typeof obj[prop] === "object") {
        deleteUndefinedProps(obj[prop]);
      }
    }
  }
}
function stripUndefinedProps(input) {
  if (input === void 0 || input === null || Array.isArray(input) || typeof input !== "object") {
    return input;
  }
  const out = {};
  for (const key in input) {
    if (input[key] !== void 0) {
      out[key] = stripUndefinedProps(input[key]);
    }
  }
  return out;
}
function getCurrentEnv() {
  return process.env.GENKIT_ENV || "prod";
}
function isDevEnv() {
  return getCurrentEnv() === "dev";
}
function featureMetadataPrefix(name) {
  return `feature:${name}`;
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  deleteUndefinedProps,
  featureMetadataPrefix,
  getCurrentEnv,
  isDevEnv,
  stripUndefinedProps
});
//# sourceMappingURL=utils.js.map