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
var document_exports = {};
__export(document_exports, {
  CustomPartSchema: () => CustomPartSchema,
  DataPartSchema: () => DataPartSchema,
  Document: () => Document,
  DocumentDataSchema: () => DocumentDataSchema,
  MediaPartSchema: () => MediaPartSchema,
  MediaSchema: () => MediaSchema,
  PartSchema: () => PartSchema,
  ReasoningPartSchema: () => ReasoningPartSchema,
  ResourcePartSchema: () => ResourcePartSchema,
  TextPartSchema: () => TextPartSchema,
  ToolRequestPartSchema: () => ToolRequestPartSchema,
  ToolRequestSchema: () => ToolRequestSchema,
  ToolResponsePartSchema: () => ToolResponsePartSchema,
  ToolResponseSchema: () => ToolResponseSchema,
  checkUniqueDocuments: () => checkUniqueDocuments
});
module.exports = __toCommonJS(document_exports);
var import_core = require("@genkit-ai/core");
const EmptyPartSchema = import_core.z.object({
  text: import_core.z.never().optional(),
  media: import_core.z.never().optional(),
  toolRequest: import_core.z.never().optional(),
  toolResponse: import_core.z.never().optional(),
  data: import_core.z.unknown().optional(),
  metadata: import_core.z.record(import_core.z.unknown()).optional(),
  custom: import_core.z.record(import_core.z.unknown()).optional(),
  reasoning: import_core.z.never().optional(),
  resource: import_core.z.never().optional()
});
const TextPartSchema = EmptyPartSchema.extend({
  /** The text of the message. */
  text: import_core.z.string()
});
const ReasoningPartSchema = EmptyPartSchema.extend({
  /** The reasoning text of the message. */
  reasoning: import_core.z.string()
});
const MediaSchema = import_core.z.object({
  /** The media content type. Inferred from data uri if not provided. */
  contentType: import_core.z.string().optional(),
  /** A `data:` or `https:` uri containing the media content.  */
  url: import_core.z.string()
});
const MediaPartSchema = EmptyPartSchema.extend({
  media: MediaSchema
});
const ToolRequestSchema = import_core.z.object({
  /** The call id or reference for a specific request. */
  ref: import_core.z.string().optional(),
  /** The name of the tool to call. */
  name: import_core.z.string(),
  /** The input parameters for the tool, usually a JSON object. */
  input: import_core.z.unknown().optional()
});
const ToolRequestPartSchema = EmptyPartSchema.extend({
  /** A request for a tool to be executed, usually provided by a model. */
  toolRequest: ToolRequestSchema
});
const ToolResponseSchema = import_core.z.object({
  /** The call id or reference for a specific request. */
  ref: import_core.z.string().optional(),
  /** The name of the tool. */
  name: import_core.z.string(),
  /** The output data returned from the tool, usually a JSON object. */
  output: import_core.z.unknown().optional()
});
const ToolResponsePartSchema = EmptyPartSchema.extend({
  /** A provided response to a tool call. */
  toolResponse: ToolResponseSchema
});
const DataPartSchema = EmptyPartSchema.extend({
  data: import_core.z.unknown()
});
const CustomPartSchema = EmptyPartSchema.extend({
  custom: import_core.z.record(import_core.z.any())
});
const ResourcePartSchema = EmptyPartSchema.extend({
  resource: import_core.z.object({
    uri: import_core.z.string()
  })
});
const PartSchema = import_core.z.union([TextPartSchema, MediaPartSchema]);
const DocumentDataSchema = import_core.z.object({
  content: import_core.z.array(PartSchema),
  metadata: import_core.z.record(import_core.z.string(), import_core.z.any()).optional()
});
function deepCopy(value) {
  if (value === void 0) {
    return value;
  }
  return JSON.parse(JSON.stringify(value));
}
class Document {
  content;
  metadata;
  constructor(data) {
    this.content = deepCopy(data.content);
    this.metadata = deepCopy(data.metadata);
  }
  static fromText(text, metadata) {
    return new Document({
      content: [{ text }],
      metadata
    });
  }
  // Construct a Document from a single media item
  static fromMedia(url, contentType, metadata) {
    return new Document({
      content: [
        {
          media: {
            contentType,
            url
          }
        }
      ],
      metadata
    });
  }
  // Construct a Document from content
  static fromData(data, dataType, metadata) {
    if (dataType === "text") {
      return this.fromText(data, metadata);
    }
    return this.fromMedia(data, dataType, metadata);
  }
  /**
   * Concatenates all `text` parts present in the document with no delimiter.
   * @returns A string of all concatenated text parts.
   */
  get text() {
    return this.content.map((part) => part.text || "").join("");
  }
  /**
   * Media array getter.
   * @returns the array of media parts.
   */
  get media() {
    return this.content.filter((part) => part.media && !part.text).map((part) => part.media);
  }
  /**
   * Gets the first item in the document. Either text or media url.
   */
  get data() {
    if (this.text) {
      return this.text;
    }
    if (this.media) {
      return this.media[0].url;
    }
    return "";
  }
  /**
   * Gets the contentType of the data that is returned by data()
   */
  get dataType() {
    if (this.text) {
      return "text";
    }
    if (this.media && this.media[0].contentType) {
      return this.media[0].contentType;
    }
    return void 0;
  }
  toJSON() {
    return {
      content: deepCopy(this.content),
      metadata: deepCopy(this.metadata)
    };
  }
  /**
   * Embedders may return multiple embeddings for a single document.
   * But storage still requires a 1:1 relationship. So we create an
   * array of Documents from a single document - one per embedding.
   * @param embeddings The embeddings to create the documents from.
   * @returns an array of documents based on this document and the embeddings.
   */
  getEmbeddingDocuments(embeddings) {
    const documents = [];
    for (const embedding of embeddings) {
      const jsonDoc = this.toJSON();
      if (embedding.metadata) {
        if (!jsonDoc.metadata) {
          jsonDoc.metadata = {};
        }
        jsonDoc.metadata.embedMetadata = embedding.metadata;
      }
      documents.push(new Document(jsonDoc));
    }
    checkUniqueDocuments(documents);
    return documents;
  }
}
function checkUniqueDocuments(documents) {
  const seen = /* @__PURE__ */ new Set();
  for (const doc of documents) {
    const serialized = JSON.stringify(doc);
    if (seen.has(serialized)) {
      console.warn(
        "Warning: embedding documents are not unique. Are you missing embed metadata?"
      );
      return false;
    }
    seen.add(serialized);
  }
  return true;
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  CustomPartSchema,
  DataPartSchema,
  Document,
  DocumentDataSchema,
  MediaPartSchema,
  MediaSchema,
  PartSchema,
  ReasoningPartSchema,
  ResourcePartSchema,
  TextPartSchema,
  ToolRequestPartSchema,
  ToolRequestSchema,
  ToolResponsePartSchema,
  ToolResponseSchema,
  checkUniqueDocuments
});
//# sourceMappingURL=document.js.map