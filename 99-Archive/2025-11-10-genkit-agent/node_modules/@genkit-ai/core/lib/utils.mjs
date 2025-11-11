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
export {
  deleteUndefinedProps,
  featureMetadataPrefix,
  getCurrentEnv,
  isDevEnv,
  stripUndefinedProps
};
//# sourceMappingURL=utils.mjs.map