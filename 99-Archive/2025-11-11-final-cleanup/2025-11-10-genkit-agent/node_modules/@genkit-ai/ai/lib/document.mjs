import { z } from "@genkit-ai/core";
const EmptyPartSchema = z.object({
  text: z.never().optional(),
  media: z.never().optional(),
  toolRequest: z.never().optional(),
  toolResponse: z.never().optional(),
  data: z.unknown().optional(),
  metadata: z.record(z.unknown()).optional(),
  custom: z.record(z.unknown()).optional(),
  reasoning: z.never().optional(),
  resource: z.never().optional()
});
const TextPartSchema = EmptyPartSchema.extend({
  /** The text of the message. */
  text: z.string()
});
const ReasoningPartSchema = EmptyPartSchema.extend({
  /** The reasoning text of the message. */
  reasoning: z.string()
});
const MediaSchema = z.object({
  /** The media content type. Inferred from data uri if not provided. */
  contentType: z.string().optional(),
  /** A `data:` or `https:` uri containing the media content.  */
  url: z.string()
});
const MediaPartSchema = EmptyPartSchema.extend({
  media: MediaSchema
});
const ToolRequestSchema = z.object({
  /** The call id or reference for a specific request. */
  ref: z.string().optional(),
  /** The name of the tool to call. */
  name: z.string(),
  /** The input parameters for the tool, usually a JSON object. */
  input: z.unknown().optional()
});
const ToolRequestPartSchema = EmptyPartSchema.extend({
  /** A request for a tool to be executed, usually provided by a model. */
  toolRequest: ToolRequestSchema
});
const ToolResponseSchema = z.object({
  /** The call id or reference for a specific request. */
  ref: z.string().optional(),
  /** The name of the tool. */
  name: z.string(),
  /** The output data returned from the tool, usually a JSON object. */
  output: z.unknown().optional()
});
const ToolResponsePartSchema = EmptyPartSchema.extend({
  /** A provided response to a tool call. */
  toolResponse: ToolResponseSchema
});
const DataPartSchema = EmptyPartSchema.extend({
  data: z.unknown()
});
const CustomPartSchema = EmptyPartSchema.extend({
  custom: z.record(z.any())
});
const ResourcePartSchema = EmptyPartSchema.extend({
  resource: z.object({
    uri: z.string()
  })
});
const PartSchema = z.union([TextPartSchema, MediaPartSchema]);
const DocumentDataSchema = z.object({
  content: z.array(PartSchema),
  metadata: z.record(z.string(), z.any()).optional()
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
export {
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
};
//# sourceMappingURL=document.mjs.map