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
var async_exports = {};
__export(async_exports, {
  Channel: () => Channel,
  LazyPromise: () => LazyPromise,
  lazy: () => lazy
});
module.exports = __toCommonJS(async_exports);
function createTask() {
  let resolve, reject;
  const promise = new Promise(
    (res, rej) => [resolve, reject] = [res, rej]
  );
  return {
    resolve,
    reject,
    promise
  };
}
class Channel {
  ready = createTask();
  buffer = [];
  err = null;
  send(value) {
    this.buffer.push(value);
    this.ready.resolve();
  }
  close() {
    this.buffer.push(null);
    this.ready.resolve();
  }
  error(err) {
    this.err = err;
    this.ready.reject(err);
  }
  [Symbol.asyncIterator]() {
    return {
      next: async () => {
        if (this.err) {
          throw this.err;
        }
        if (!this.buffer.length) {
          await this.ready.promise;
        }
        const value = this.buffer.shift();
        if (!this.buffer.length) {
          this.ready = createTask();
        }
        return {
          value,
          done: !value
        };
      }
    };
  }
}
class LazyPromise {
  executor;
  promise;
  constructor(executor) {
    this.executor = executor;
  }
  then(onfulfilled, onrejected) {
    this.promise ??= new Promise(this.executor);
    return this.promise.then(onfulfilled, onrejected);
  }
}
function lazy(fn) {
  return new LazyPromise((resolve, reject) => {
    try {
      resolve(fn());
    } catch (e) {
      reject(e);
    }
  });
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  Channel,
  LazyPromise,
  lazy
});
//# sourceMappingURL=async.js.map