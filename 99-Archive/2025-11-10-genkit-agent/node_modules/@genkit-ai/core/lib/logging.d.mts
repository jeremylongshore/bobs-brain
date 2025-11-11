/**
 * Copyright 2024 Google LLC
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
declare class Logger {
    readonly defaultLogger: {
        shouldLog(targetLevel: string): boolean;
        debug(...args: any): void;
        info(...args: any): void;
        warn(...args: any): void;
        error(...args: any): void;
        level: string;
    };
    init(fn: any): void;
    info(...args: any): void;
    debug(...args: any): void;
    error(...args: any): void;
    warn(...args: any): void;
    setLogLevel(level: 'error' | 'warn' | 'info' | 'debug'): void;
    logStructured(msg: string, metadata: any): void;
    logStructuredError(msg: string, metadata: any): void;
}
/**
 * Genkit logger.
 *
 * ```ts
 * import { logger } from 'genkit/logging';
 *
 * logger.setLogLevel('debug');
 * ```
 */
declare const logger: Logger;

export { logger };
