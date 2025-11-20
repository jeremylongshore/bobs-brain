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
var middleware_exports = {};
__export(middleware_exports, {
  CONTEXT_PREFACE: () => CONTEXT_PREFACE,
  augmentWithContext: () => augmentWithContext,
  downloadRequestMedia: () => downloadRequestMedia,
  simulateConstrainedGeneration: () => simulateConstrainedGeneration,
  simulateSystemPrompt: () => simulateSystemPrompt,
  validateSupport: () => validateSupport
});
module.exports = __toCommonJS(middleware_exports);
var import_document = require("../document.js");
var import_formats = require("../formats/index.js");
function downloadRequestMedia(options) {
  return async (req, next) => {
    const { default: fetch } = await import("node-fetch");
    const newReq = {
      ...req,
      messages: await Promise.all(
        req.messages.map(async (message) => {
          const content = await Promise.all(
            message.content.map(async (part) => {
              if (!part.media || !part.media.url.startsWith("http") || options?.filter && !options?.filter(part)) {
                return part;
              }
              const response = await fetch(part.media.url, {
                size: options?.maxBytes
              });
              if (response.status !== 200)
                throw new Error(
                  `HTTP error downloading media '${part.media.url}': ${await response.text()}`
                );
              const contentType = part.media.contentType || response.headers.get("content-type") || "";
              return {
                media: {
                  contentType,
                  url: `data:${contentType};base64,${Buffer.from(
                    await response.arrayBuffer()
                  ).toString("base64")}`
                }
              };
            })
          );
          return {
            ...message,
            content
          };
        })
      )
    };
    return next(newReq);
  };
}
function validateSupport(options) {
  const supports = options.supports || {};
  return async (req, next) => {
    function invalid(message) {
      throw new Error(
        `Model '${options.name}' does not support ${message}. Request: ${JSON.stringify(
          req,
          null,
          2
        )}`
      );
    }
    if (supports.media === false && req.messages.some((message) => message.content.some((part) => part.media)))
      invalid("media, but media was provided");
    if (supports.tools === false && req.tools?.length)
      invalid("tool use, but tools were provided");
    if (supports.multiturn === false && req.messages.length > 1)
      invalid(`multiple messages, but ${req.messages.length} were provided`);
    return next();
  };
}
function lastUserMessage(messages) {
  for (let i = messages.length - 1; i >= 0; i--) {
    if (messages[i].role === "user") {
      return messages[i];
    }
  }
  return void 0;
}
function simulateSystemPrompt(options) {
  const preface = options?.preface || "SYSTEM INSTRUCTIONS:\n";
  const acknowledgement = options?.acknowledgement || "Understood.";
  return (req, next) => {
    const messages = [...req.messages];
    for (let i = 0; i < messages.length; i++) {
      if (req.messages[i].role === "system") {
        const systemPrompt = messages[i].content;
        messages.splice(
          i,
          1,
          { role: "user", content: [{ text: preface }, ...systemPrompt] },
          { role: "model", content: [{ text: acknowledgement }] }
        );
        break;
      }
    }
    return next({ ...req, messages });
  };
}
const CONTEXT_PREFACE = "\n\nUse the following information to complete your task:\n\n";
const CONTEXT_ITEM_TEMPLATE = (d, index, options) => {
  let out = "- ";
  if (options?.citationKey) {
    out += `[${d.metadata[options.citationKey]}]: `;
  } else if (options?.citationKey === void 0) {
    out += `[${d.metadata?.["ref"] || d.metadata?.["id"] || index}]: `;
  }
  out += d.text + "\n";
  return out;
};
function augmentWithContext(options) {
  const preface = typeof options?.preface === "undefined" ? CONTEXT_PREFACE : options.preface;
  const itemTemplate = options?.itemTemplate || CONTEXT_ITEM_TEMPLATE;
  return (req, next) => {
    if (!req.docs?.length) return next(req);
    const userMessage = lastUserMessage(req.messages);
    if (!userMessage) return next(req);
    const contextPartIndex = userMessage?.content.findIndex(
      (p) => p.metadata?.purpose === "context"
    );
    const contextPart = contextPartIndex >= 0 && userMessage.content[contextPartIndex];
    if (contextPart && !contextPart.metadata?.pending) {
      return next(req);
    }
    let out = `${preface || ""}`;
    req.docs?.forEach((d, i) => {
      out += itemTemplate(new import_document.Document(d), i, options);
    });
    out += "\n";
    if (contextPartIndex >= 0) {
      userMessage.content[contextPartIndex] = {
        ...contextPart,
        text: out,
        metadata: { purpose: "context" }
      };
    } else {
      userMessage.content.push({ text: out, metadata: { purpose: "context" } });
    }
    return next(req);
  };
}
const DEFAULT_CONSTRAINED_GENERATION_INSTRUCTIONS = (schema) => `Output should be in JSON format and conform to the following schema:

\`\`\`
${JSON.stringify(schema)}
\`\`\`
`;
function simulateConstrainedGeneration(options) {
  return (req, next) => {
    let instructions;
    if (req.output?.constrained && req.output?.schema) {
      instructions = (options?.instructionsRenderer ?? DEFAULT_CONSTRAINED_GENERATION_INSTRUCTIONS)(req.output?.schema);
      req = {
        ...req,
        messages: (0, import_formats.injectInstructions)(req.messages, instructions),
        output: {
          ...req.output,
          // we're simulating it, so to the underlying model it's unconstrained.
          constrained: false,
          format: void 0,
          contentType: void 0,
          schema: void 0
        }
      };
    }
    return next(req);
  };
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  CONTEXT_PREFACE,
  augmentWithContext,
  downloadRequestMedia,
  simulateConstrainedGeneration,
  simulateSystemPrompt,
  validateSupport
});
//# sourceMappingURL=middleware.js.map