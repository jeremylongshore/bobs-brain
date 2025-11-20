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
export {
  Channel,
  LazyPromise,
  lazy
};
//# sourceMappingURL=async.mjs.map