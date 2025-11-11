import { Channel } from "@genkit-ai/core/async";
const __flowStreamDelimiter = "\n\n";
function streamFlow({
  url,
  input,
  headers,
  abortSignal
}) {
  const channel = new Channel();
  const operationPromise = __flowRunEnvelope({
    url,
    input,
    sendChunk: (c) => channel.send(c),
    headers,
    abortSignal
  });
  operationPromise.then(
    () => channel.close(),
    (err) => channel.error(err)
  );
  return {
    output: operationPromise,
    stream: channel
  };
}
async function __flowRunEnvelope({
  url,
  input,
  sendChunk,
  headers,
  abortSignal
}) {
  const response = await fetch(url, {
    method: "POST",
    body: JSON.stringify({
      data: input
    }),
    headers: {
      Accept: "text/event-stream",
      "Content-Type": "application/json",
      ...headers
    },
    signal: abortSignal
  });
  if (response.status !== 200) {
    throw new Error(
      `Server returned: ${response.status}: ${await response.text()}`
    );
  }
  if (!response.body) {
    throw new Error("Response body is empty");
  }
  var reader = response.body.getReader();
  var decoder = new TextDecoder();
  let buffer = "";
  while (true) {
    const result = await reader.read();
    const decodedValue = decoder.decode(result.value);
    if (decodedValue) {
      buffer += decodedValue;
    }
    while (buffer.includes(__flowStreamDelimiter)) {
      const chunk = JSON.parse(
        buffer.substring(0, buffer.indexOf(__flowStreamDelimiter)).substring("data: ".length)
      );
      if (chunk.hasOwnProperty("message")) {
        sendChunk(chunk.message);
      } else if (chunk.hasOwnProperty("result")) {
        return chunk.result;
      } else if (chunk.hasOwnProperty("error")) {
        throw new Error(
          `${chunk.error.status}: ${chunk.error.message}
${chunk.error.details}`
        );
      } else {
        throw new Error("unknown chunk format: " + JSON.stringify(chunk));
      }
      buffer = buffer.substring(
        buffer.indexOf(__flowStreamDelimiter) + __flowStreamDelimiter.length
      );
    }
  }
  throw new Error("stream did not terminate correctly");
}
async function runFlow({
  url,
  input,
  headers,
  abortSignal
}) {
  const response = await fetch(url, {
    method: "POST",
    body: JSON.stringify({
      data: input
    }),
    headers: {
      "Content-Type": "application/json",
      ...headers
    },
    signal: abortSignal
  });
  if (response.status !== 200) {
    throw new Error(
      `Server returned: ${response.status}: ${await response.text()}`
    );
  }
  const wrappedResult = await response.json();
  if ("error" in wrappedResult) {
    if (typeof wrappedResult.error === "string") {
      throw new Error(wrappedResult.error);
    }
    throw new Error(JSON.stringify(wrappedResult.error));
  }
  return wrappedResult.result;
}
export {
  runFlow,
  streamFlow
};
//# sourceMappingURL=client.mjs.map