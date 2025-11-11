"use strict";
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
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
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);
var schema_exports = {};
__export(schema_exports, {
  ValidationError: () => ValidationError,
  defineJsonSchema: () => defineJsonSchema,
  defineSchema: () => defineSchema,
  parseSchema: () => parseSchema,
  toJsonSchema: () => toJsonSchema,
  validateSchema: () => validateSchema,
  z: () => import_zod.z
});
module.exports = __toCommonJS(schema_exports);
var import_ajv = __toESM(require("ajv"));
var import_ajv_formats = __toESM(require("ajv-formats"));
var import_zod = require("zod");
var import_zod_to_json_schema = __toESM(require("zod-to-json-schema"));
var import_error = require("./error.js");
const ajv = new import_ajv.default();
(0, import_ajv_formats.default)(ajv);
const jsonSchemas = /* @__PURE__ */ new WeakMap();
const validators = /* @__PURE__ */ new WeakMap();
class ValidationError extends import_error.GenkitError {
  constructor({
    data,
    errors,
    schema
  }) {
    super({
      status: "INVALID_ARGUMENT",
      message: `Schema validation failed. Parse Errors:

${errors.map((e) => `- ${e.path}: ${e.message}`).join("\n")}

Provided data:

${JSON.stringify(data, null, 2)}

Required JSON schema:

${JSON.stringify(schema, null, 2)}`,
      detail: { errors, schema }
    });
  }
}
function toJsonSchema({
  jsonSchema,
  schema
}) {
  if (!jsonSchema && !schema) return null;
  if (jsonSchema) return jsonSchema;
  if (jsonSchemas.has(schema)) return jsonSchemas.get(schema);
  const outSchema = (0, import_zod_to_json_schema.default)(schema, {
    $refStrategy: "none",
    removeAdditionalStrategy: "strict"
  });
  jsonSchemas.set(schema, outSchema);
  return outSchema;
}
function toErrorDetail(error) {
  return {
    path: error.instancePath.substring(1).replace(/\//g, ".") || "(root)",
    message: error.message
  };
}
function validateSchema(data, options) {
  const toValidate = toJsonSchema(options);
  if (!toValidate) {
    return { valid: true, schema: toValidate };
  }
  const validator = validators.get(toValidate) || ajv.compile(toValidate);
  const valid = validator(data);
  const errors = validator.errors?.map((e) => e);
  return { valid, errors: errors?.map(toErrorDetail), schema: toValidate };
}
function parseSchema(data, options) {
  const { valid, errors, schema } = validateSchema(data, options);
  if (!valid) {
    throw new ValidationError({ data, errors, schema });
  }
  return data;
}
function defineSchema(registry, name, schema) {
  registry.registerSchema(name, { schema });
  return schema;
}
function defineJsonSchema(registry, name, jsonSchema) {
  registry.registerSchema(name, { jsonSchema });
  return jsonSchema;
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  ValidationError,
  defineJsonSchema,
  defineSchema,
  parseSchema,
  toJsonSchema,
  validateSchema,
  z
});
//# sourceMappingURL=schema.js.map