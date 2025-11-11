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
var exporter_exports = {};
__export(exporter_exports, {
  TraceServerExporter: () => TraceServerExporter,
  setTelemetryServerUrl: () => setTelemetryServerUrl,
  telemetryServerUrl: () => telemetryServerUrl
});
module.exports = __toCommonJS(exporter_exports);
var import_api = require("@opentelemetry/api");
var import_core = require("@opentelemetry/core");
var import_logging = require("../logging.js");
var import_utils = require("../utils.js");
let telemetryServerUrl;
function setTelemetryServerUrl(url) {
  telemetryServerUrl = url;
}
class TraceServerExporter {
  /**
   * Export spans.
   * @param spans
   * @param resultCallback
   */
  export(spans, resultCallback) {
    this._sendSpans(spans, resultCallback);
  }
  /**
   * Shutdown the exporter.
   */
  shutdown() {
    this._sendSpans([]);
    return this.forceFlush();
  }
  /**
   * Converts span info into trace store format.
   * @param span
   */
  _exportInfo(span) {
    const spanData = {
      spanId: span.spanContext().spanId,
      traceId: span.spanContext().traceId,
      startTime: transformTime(span.startTime),
      endTime: transformTime(span.endTime),
      attributes: { ...span.attributes },
      displayName: span.name,
      links: span.links,
      spanKind: import_api.SpanKind[span.kind],
      parentSpanId: span.parentSpanId,
      sameProcessAsParentSpan: { value: !span.spanContext().isRemote },
      status: span.status,
      timeEvents: {
        timeEvent: span.events.map((e) => ({
          time: transformTime(e.time),
          annotation: {
            attributes: e.attributes ?? {},
            description: e.name
          }
        }))
      }
    };
    if (span.instrumentationLibrary !== void 0) {
      spanData.instrumentationLibrary = {
        name: span.instrumentationLibrary.name
      };
      if (span.instrumentationLibrary.schemaUrl !== void 0) {
        spanData.instrumentationLibrary.schemaUrl = span.instrumentationLibrary.schemaUrl;
      }
      if (span.instrumentationLibrary.version !== void 0) {
        spanData.instrumentationLibrary.version = span.instrumentationLibrary.version;
      }
    }
    (0, import_utils.deleteUndefinedProps)(spanData);
    return spanData;
  }
  /**
   * Exports any pending spans in exporter
   */
  forceFlush() {
    return Promise.resolve();
  }
  async _sendSpans(spans, done) {
    const traces = {};
    for (const span of spans) {
      if (!traces[span.spanContext().traceId]) {
        traces[span.spanContext().traceId] = [];
      }
      traces[span.spanContext().traceId].push(span);
    }
    let error = false;
    for (const traceId of Object.keys(traces)) {
      try {
        await this.save(traceId, traces[traceId]);
      } catch (e) {
        error = true;
        import_logging.logger.error(`Failed to save trace ${traceId}`, e);
      }
      if (done) {
        return done({
          code: error ? import_core.ExportResultCode.FAILED : import_core.ExportResultCode.SUCCESS
        });
      }
    }
  }
  async save(traceId, spans) {
    if (!telemetryServerUrl) {
      import_logging.logger.debug(
        `Telemetry server is not configured, trace ${traceId} not saved!`
      );
      return;
    }
    const data = {
      traceId,
      spans: {}
    };
    for (const span of spans) {
      const convertedSpan = this._exportInfo(span);
      data.spans[convertedSpan.spanId] = convertedSpan;
      if (!convertedSpan.parentSpanId) {
        data.displayName = convertedSpan.displayName;
        data.startTime = convertedSpan.startTime;
        data.endTime = convertedSpan.endTime;
      }
    }
    await fetch(`${telemetryServerUrl}/api/traces`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });
  }
}
function transformTime(time) {
  return (0, import_core.hrTimeToMilliseconds)(time);
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  TraceServerExporter,
  setTelemetryServerUrl,
  telemetryServerUrl
});
//# sourceMappingURL=exporter.js.map