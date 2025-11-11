import * as z from 'zod';
import { q as Action, T as ActionType, A as ActionMetadata, V as Registry } from './action-W3NVe6d0.js';
import 'json-schema';
import './context.js';
import './statusTypes.js';
import 'dotprompt';
import 'ajv';

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

type DapValue = {
    [K in ActionType]?: Action<z.ZodTypeAny, z.ZodTypeAny, z.ZodTypeAny>[];
};
declare class SimpleCache {
    private value;
    private expiresAt;
    private ttlMillis;
    private dap;
    private dapFn;
    private fetchPromise;
    constructor(dap: DynamicActionProviderAction, config: DapConfig, dapFn: DapFn);
    getOrFetch(): Promise<DapValue>;
    invalidate(): void;
}
interface DynamicRegistry {
    __cache: SimpleCache;
    invalidateCache(): void;
    getAction(actionType: string, actionName: string): Promise<Action<z.ZodTypeAny, z.ZodTypeAny, z.ZodTypeAny> | undefined>;
    listActionMetadata(actionType: string, actionName: string): Promise<ActionMetadata[]>;
}
type DynamicActionProviderAction = Action<z.ZodTypeAny, z.ZodTypeAny, z.ZodTypeAny> & DynamicRegistry & {
    __action: {
        metadata: {
            type: 'dynamic-action-provider';
        };
    };
};
declare function isDynamicActionProvider(obj: Action<z.ZodTypeAny, z.ZodTypeAny>): obj is DynamicActionProviderAction;
interface DapConfig {
    name: string;
    description?: string;
    cacheConfig?: {
        ttlMillis: number | undefined;
    };
    metadata?: Record<string, any>;
}
type DapFn = () => Promise<DapValue>;
type DapMetadata = {
    [K in ActionType]?: ActionMetadata[];
};
declare function defineDynamicActionProvider(registry: Registry, config: DapConfig | string, fn: DapFn): DynamicActionProviderAction;

export { type DapConfig, type DapFn, type DapMetadata, type DynamicActionProviderAction, type DynamicRegistry, defineDynamicActionProvider, isDynamicActionProvider };
