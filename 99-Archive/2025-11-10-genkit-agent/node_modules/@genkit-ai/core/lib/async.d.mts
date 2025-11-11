/**
 * Copyright 2025 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
/**
 * A handle to a promise and its resolvers.
 */
interface Task<T> {
    resolve: (result: T) => void;
    reject: (err: unknown) => void;
    promise: Promise<T>;
}
/**
 * A class designed to help turn repeated callbacks into async iterators.
 * Based loosely on a combination of Go channels and Promises.
 */
declare class Channel<T> implements AsyncIterable<T> {
    private ready;
    private buffer;
    private err;
    send(value: T): void;
    close(): void;
    error(err: unknown): void;
    [Symbol.asyncIterator](): AsyncIterator<T>;
}
/**
 * A lazy promise that does not run its executor function until then is called.
 */
declare class LazyPromise<T> implements PromiseLike<T> {
    private executor;
    private promise;
    constructor(executor: (resolve?: any, reject?: any) => void | Promise<void>);
    then<TResult1 = T, TResult2 = never>(onfulfilled?: ((value: T) => TResult1 | PromiseLike<TResult1>) | undefined | null, onrejected?: ((reason: any) => TResult2 | PromiseLike<TResult2>) | undefined | null): PromiseLike<TResult1 | TResult2>;
}
/** Lazily call the provided function to resolve the LazyPromise. */
declare function lazy<T>(fn: () => T | PromiseLike<T>): PromiseLike<T>;

export { Channel, LazyPromise, type Task, lazy };
