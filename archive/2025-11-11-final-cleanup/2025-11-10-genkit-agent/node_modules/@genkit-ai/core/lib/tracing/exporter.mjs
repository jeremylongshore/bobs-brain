import { SpanKind } from "@opentelemetry/api";
import {
  ExportResultCode,
  hrTimeToMilliseconds
} from "@opentelemetry/core";
import { logger } from "../logging.js";
import { deleteUndefinedProps } from "../utils.js";
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
      spanKind: SpanKind[span.kind],
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
    deleteUndefinedProps(spanData);
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
        logger.error(`Failed to save trace ${traceId}`, e);
      }
      if (done) {
        return done({
          code: error ? ExportResultCode.FAILED : ExportResultCode.SUCCESS
        });
      }
    }
  }
  async save(traceId, spans) {
    if (!telemetryServerUrl) {
      logger.debug(
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
  return hrTimeToMilliseconds(time);
}
export {
  TraceServerExporter,
  setTelemetryServerUrl,
  telemetryServerUrl
};
//# sourceMappingURL=exporter.mjs.map