import { Action, z, ActionContext } from '@genkit-ai/core';
import { Registry } from '@genkit-ai/core/registry';

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
 * Options for defining a resource.
 */
interface ResourceOptions {
    /**
     * Resource name. If not specified, uri or template will be used as name.
     */
    name?: string;
    /**
     * The URI of the resource. Can contain template variables.
     */
    uri?: string;
    /**
     * The URI template (ex. `my://resource/{id}`). See RFC6570 for specification.
     */
    template?: string;
    /**
     * A description of the resource.
     */
    description?: string;
    /**
     * Resource metadata.
     */
    metadata?: Record<string, any>;
}
declare const ResourceInputSchema: z.ZodObject<{
    uri: z.ZodString;
}, "strip", z.ZodTypeAny, {
    uri: string;
}, {
    uri: string;
}>;
type ResourceInput = z.infer<typeof ResourceInputSchema>;
declare const ResourceOutputSchema: z.ZodObject<{
    content: z.ZodArray<z.ZodUnion<[z.ZodObject<{
        media: z.ZodOptional<z.ZodNever>;
        toolRequest: z.ZodOptional<z.ZodNever>;
        toolResponse: z.ZodOptional<z.ZodNever>;
        data: z.ZodOptional<z.ZodUnknown>;
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
        custom: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
        reasoning: z.ZodOptional<z.ZodNever>;
        resource: z.ZodOptional<z.ZodNever>;
    } & {
        text: z.ZodString;
    }, "strip", z.ZodTypeAny, {
        text: string;
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        media?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    }, {
        text: string;
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        media?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    }>, z.ZodObject<{
        text: z.ZodOptional<z.ZodNever>;
        toolRequest: z.ZodOptional<z.ZodNever>;
        toolResponse: z.ZodOptional<z.ZodNever>;
        data: z.ZodOptional<z.ZodUnknown>;
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
        custom: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
        reasoning: z.ZodOptional<z.ZodNever>;
        resource: z.ZodOptional<z.ZodNever>;
    } & {
        media: z.ZodObject<{
            contentType: z.ZodOptional<z.ZodString>;
            url: z.ZodString;
        }, "strip", z.ZodTypeAny, {
            url: string;
            contentType?: string | undefined;
        }, {
            url: string;
            contentType?: string | undefined;
        }>;
    }, "strip", z.ZodTypeAny, {
        media: {
            url: string;
            contentType?: string | undefined;
        };
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    }, {
        media: {
            url: string;
            contentType?: string | undefined;
        };
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    }>, z.ZodObject<{
        text: z.ZodOptional<z.ZodNever>;
        media: z.ZodOptional<z.ZodNever>;
        toolResponse: z.ZodOptional<z.ZodNever>;
        data: z.ZodOptional<z.ZodUnknown>;
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
        custom: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
        reasoning: z.ZodOptional<z.ZodNever>;
        resource: z.ZodOptional<z.ZodNever>;
    } & {
        toolRequest: z.ZodObject<{
            ref: z.ZodOptional<z.ZodString>;
            name: z.ZodString;
            input: z.ZodOptional<z.ZodUnknown>;
        }, "strip", z.ZodTypeAny, {
            name: string;
            ref?: string | undefined;
            input?: unknown;
        }, {
            name: string;
            ref?: string | undefined;
            input?: unknown;
        }>;
    }, "strip", z.ZodTypeAny, {
        toolRequest: {
            name: string;
            ref?: string | undefined;
            input?: unknown;
        };
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    }, {
        toolRequest: {
            name: string;
            ref?: string | undefined;
            input?: unknown;
        };
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    }>, z.ZodObject<{
        text: z.ZodOptional<z.ZodNever>;
        media: z.ZodOptional<z.ZodNever>;
        toolRequest: z.ZodOptional<z.ZodNever>;
        data: z.ZodOptional<z.ZodUnknown>;
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
        custom: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
        reasoning: z.ZodOptional<z.ZodNever>;
        resource: z.ZodOptional<z.ZodNever>;
    } & {
        toolResponse: z.ZodObject<{
            ref: z.ZodOptional<z.ZodString>;
            name: z.ZodString;
            output: z.ZodOptional<z.ZodUnknown>;
        }, "strip", z.ZodTypeAny, {
            name: string;
            output?: unknown;
            ref?: string | undefined;
        }, {
            name: string;
            output?: unknown;
            ref?: string | undefined;
        }>;
    }, "strip", z.ZodTypeAny, {
        toolResponse: {
            name: string;
            output?: unknown;
            ref?: string | undefined;
        };
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolRequest?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    }, {
        toolResponse: {
            name: string;
            output?: unknown;
            ref?: string | undefined;
        };
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolRequest?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    }>, z.ZodObject<{
        text: z.ZodOptional<z.ZodNever>;
        media: z.ZodOptional<z.ZodNever>;
        toolRequest: z.ZodOptional<z.ZodNever>;
        toolResponse: z.ZodOptional<z.ZodNever>;
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
        custom: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
        reasoning: z.ZodOptional<z.ZodNever>;
        resource: z.ZodOptional<z.ZodNever>;
    } & {
        data: z.ZodUnknown;
    }, "strip", z.ZodTypeAny, {
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    }, {
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    }>, z.ZodObject<{
        text: z.ZodOptional<z.ZodNever>;
        media: z.ZodOptional<z.ZodNever>;
        toolRequest: z.ZodOptional<z.ZodNever>;
        toolResponse: z.ZodOptional<z.ZodNever>;
        data: z.ZodOptional<z.ZodUnknown>;
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
        reasoning: z.ZodOptional<z.ZodNever>;
        resource: z.ZodOptional<z.ZodNever>;
    } & {
        custom: z.ZodRecord<z.ZodString, z.ZodAny>;
    }, "strip", z.ZodTypeAny, {
        custom: Record<string, any>;
        metadata?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    }, {
        custom: Record<string, any>;
        metadata?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    }>, z.ZodObject<{
        text: z.ZodOptional<z.ZodNever>;
        media: z.ZodOptional<z.ZodNever>;
        toolRequest: z.ZodOptional<z.ZodNever>;
        toolResponse: z.ZodOptional<z.ZodNever>;
        data: z.ZodOptional<z.ZodUnknown>;
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
        custom: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
        resource: z.ZodOptional<z.ZodNever>;
    } & {
        reasoning: z.ZodString;
    }, "strip", z.ZodTypeAny, {
        reasoning: string;
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        resource?: undefined;
    }, {
        reasoning: string;
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        resource?: undefined;
    }>, z.ZodObject<{
        text: z.ZodOptional<z.ZodNever>;
        media: z.ZodOptional<z.ZodNever>;
        toolRequest: z.ZodOptional<z.ZodNever>;
        toolResponse: z.ZodOptional<z.ZodNever>;
        data: z.ZodOptional<z.ZodUnknown>;
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
        custom: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
        reasoning: z.ZodOptional<z.ZodNever>;
    } & {
        resource: z.ZodObject<{
            uri: z.ZodString;
        }, "strip", z.ZodTypeAny, {
            uri: string;
        }, {
            uri: string;
        }>;
    }, "strip", z.ZodTypeAny, {
        resource: {
            uri: string;
        };
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
    }, {
        resource: {
            uri: string;
        };
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
    }>]>, "many">;
}, "strip", z.ZodTypeAny, {
    content: ({
        text: string;
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        media?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    } | {
        media: {
            url: string;
            contentType?: string | undefined;
        };
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    } | {
        toolRequest: {
            name: string;
            ref?: string | undefined;
            input?: unknown;
        };
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    } | {
        toolResponse: {
            name: string;
            output?: unknown;
            ref?: string | undefined;
        };
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolRequest?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    } | {
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    } | {
        custom: Record<string, any>;
        metadata?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    } | {
        reasoning: string;
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        resource?: undefined;
    } | {
        resource: {
            uri: string;
        };
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
    })[];
}, {
    content: ({
        text: string;
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        media?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    } | {
        media: {
            url: string;
            contentType?: string | undefined;
        };
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    } | {
        toolRequest: {
            name: string;
            ref?: string | undefined;
            input?: unknown;
        };
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    } | {
        toolResponse: {
            name: string;
            output?: unknown;
            ref?: string | undefined;
        };
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolRequest?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    } | {
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    } | {
        custom: Record<string, any>;
        metadata?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
        resource?: undefined;
    } | {
        reasoning: string;
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        resource?: undefined;
    } | {
        resource: {
            uri: string;
        };
        metadata?: Record<string, unknown> | undefined;
        custom?: Record<string, unknown> | undefined;
        text?: undefined;
        media?: undefined;
        toolRequest?: undefined;
        toolResponse?: undefined;
        data?: unknown;
        reasoning?: undefined;
    })[];
}>;
type ResourceOutput = z.infer<typeof ResourceOutputSchema>;
/**
 * A function that returns parts for a given resource.
 */
type ResourceFn = (input: ResourceInput, ctx: ActionContext) => ResourceOutput | Promise<ResourceOutput>;
/**
 * A resource action.
 */
interface ResourceAction extends Action<typeof ResourceInputSchema, typeof ResourceOutputSchema> {
    matches(input: ResourceInput): boolean;
}
/**
 * A reference to a resource in the form of a name or a ResourceAction.
 */
type ResourceArgument = ResourceAction | string;
declare function resolveResources(registry: Registry, resources?: ResourceArgument[]): Promise<ResourceAction[]>;
declare function lookupResourceByName(registry: Registry, name: string): Promise<ResourceAction>;
/**
 * Defines a resource.
 *
 * @param registry The registry to register the resource with.
 * @param opts The resource options.
 * @param fn The resource function.
 * @returns The resource action.
 */
declare function defineResource(registry: Registry, opts: ResourceOptions, fn: ResourceFn): ResourceAction;
/**
 * A dynamic action with a `resource` type. Dynamic resources are detached actions -- not associated with any registry.
 */
type DynamicResourceAction = ResourceAction & {
    __action: {
        metadata: {
            type: 'resource';
        };
    };
    /** @deprecated no-op, for backwards compatibility only. */
    attach(registry: Registry): ResourceAction;
    matches(input: ResourceInput): boolean;
};
/**
 * Finds a matching resource in the registry. If not found returns undefined.
 */
declare function findMatchingResource(registry: Registry, resources: ResourceAction[], input: ResourceInput): Promise<ResourceAction | undefined>;
/** Checks whether provided object is a dynamic resource. */
declare function isDynamicResourceAction(t: unknown): t is ResourceAction;
/**
 * Defines a dynamic resource. Dynamic resources are just like regular resources but will not be
 * registered in the Genkit registry and can be defined dynamically at runtime.
 */
declare function resource(opts: ResourceOptions, fn: ResourceFn): ResourceAction;
/**
 * Defines a dynamic resource. Dynamic resources are just like regular resources but will not be
 * registered in the Genkit registry and can be defined dynamically at runtime.
 *
 * @deprecated renamed to {@link resource}.
 */
declare function dynamicResource(opts: ResourceOptions, fn: ResourceFn): DynamicResourceAction;

export { type DynamicResourceAction, type ResourceAction, type ResourceArgument, type ResourceFn, type ResourceInput, ResourceInputSchema, type ResourceOptions, type ResourceOutput, ResourceOutputSchema, defineResource, dynamicResource, findMatchingResource, isDynamicResourceAction, lookupResourceByName, resolveResources, resource };
