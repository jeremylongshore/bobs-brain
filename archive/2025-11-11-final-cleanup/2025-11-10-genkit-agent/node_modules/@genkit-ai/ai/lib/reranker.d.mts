import { z, Action } from '@genkit-ai/core';
import { Registry } from '@genkit-ai/core/registry';
import { b as DocumentData, D as Document, P as Part } from './document-SEV6zxye.mjs';

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

type RerankerFn<RerankerOptions extends z.ZodTypeAny> = (query: Document, documents: Document[], queryOpts: z.infer<RerankerOptions>) => Promise<RerankerResponse>;
/**
 * Zod schema for a reranked document metadata.
 */
declare const RankedDocumentMetadataSchema: z.ZodObject<{
    score: z.ZodNumber;
}, "passthrough", z.ZodTypeAny, z.objectOutputType<{
    score: z.ZodNumber;
}, z.ZodTypeAny, "passthrough">, z.objectInputType<{
    score: z.ZodNumber;
}, z.ZodTypeAny, "passthrough">>;
declare const RankedDocumentDataSchema: z.ZodObject<{
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
    }>]>, "many">;
    metadata: z.ZodObject<{
        score: z.ZodNumber;
    }, "passthrough", z.ZodTypeAny, z.objectOutputType<{
        score: z.ZodNumber;
    }, z.ZodTypeAny, "passthrough">, z.objectInputType<{
        score: z.ZodNumber;
    }, z.ZodTypeAny, "passthrough">>;
}, "strip", z.ZodTypeAny, {
    metadata: {
        score: number;
    } & {
        [k: string]: unknown;
    };
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
    })[];
}, {
    metadata: {
        score: number;
    } & {
        [k: string]: unknown;
    };
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
    })[];
}>;
type RankedDocumentData = z.infer<typeof RankedDocumentDataSchema>;
declare class RankedDocument extends Document implements RankedDocumentData {
    content: Part[];
    metadata: {
        score: number;
    } & Record<string, any>;
    constructor(data: RankedDocumentData);
    /**
     * Returns the score of the document.
     * @returns The score of the document.
     */
    score(): number;
}
declare const RerankerRequestSchema: z.ZodObject<{
    query: z.ZodObject<{
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
        }>]>, "many">;
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodAny>>;
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
        })[];
        metadata?: Record<string, any> | undefined;
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
        })[];
        metadata?: Record<string, any> | undefined;
    }>;
    documents: z.ZodArray<z.ZodObject<{
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
        }>]>, "many">;
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodAny>>;
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
        })[];
        metadata?: Record<string, any> | undefined;
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
        })[];
        metadata?: Record<string, any> | undefined;
    }>, "many">;
    options: z.ZodOptional<z.ZodAny>;
}, "strip", z.ZodTypeAny, {
    documents: {
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
        })[];
        metadata?: Record<string, any> | undefined;
    }[];
    query: {
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
        })[];
        metadata?: Record<string, any> | undefined;
    };
    options?: any;
}, {
    documents: {
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
        })[];
        metadata?: Record<string, any> | undefined;
    }[];
    query: {
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
        })[];
        metadata?: Record<string, any> | undefined;
    };
    options?: any;
}>;
declare const RerankerResponseSchema: z.ZodObject<{
    documents: z.ZodArray<z.ZodObject<{
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
        }>]>, "many">;
        metadata: z.ZodObject<{
            score: z.ZodNumber;
        }, "passthrough", z.ZodTypeAny, z.objectOutputType<{
            score: z.ZodNumber;
        }, z.ZodTypeAny, "passthrough">, z.objectInputType<{
            score: z.ZodNumber;
        }, z.ZodTypeAny, "passthrough">>;
    }, "strip", z.ZodTypeAny, {
        metadata: {
            score: number;
        } & {
            [k: string]: unknown;
        };
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
        })[];
    }, {
        metadata: {
            score: number;
        } & {
            [k: string]: unknown;
        };
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
        })[];
    }>, "many">;
}, "strip", z.ZodTypeAny, {
    documents: {
        metadata: {
            score: number;
        } & {
            [k: string]: unknown;
        };
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
        })[];
    }[];
}, {
    documents: {
        metadata: {
            score: number;
        } & {
            [k: string]: unknown;
        };
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
        })[];
    }[];
}>;
type RerankerResponse = z.infer<typeof RerankerResponseSchema>;
declare const RerankerInfoSchema: z.ZodObject<{
    label: z.ZodOptional<z.ZodString>;
    /** Supported model capabilities. */
    supports: z.ZodOptional<z.ZodObject<{
        /** Model can process media as part of the prompt (multimodal input). */
        media: z.ZodOptional<z.ZodBoolean>;
    }, "strip", z.ZodTypeAny, {
        media?: boolean | undefined;
    }, {
        media?: boolean | undefined;
    }>>;
}, "strip", z.ZodTypeAny, {
    label?: string | undefined;
    supports?: {
        media?: boolean | undefined;
    } | undefined;
}, {
    label?: string | undefined;
    supports?: {
        media?: boolean | undefined;
    } | undefined;
}>;
type RerankerInfo = z.infer<typeof RerankerInfoSchema>;
type RerankerAction<CustomOptions extends z.ZodTypeAny = z.ZodTypeAny> = Action<typeof RerankerRequestSchema, typeof RerankerResponseSchema> & {
    __configSchema?: CustomOptions;
};
/**
 *  Creates a reranker action for the provided {@link RerankerFn} implementation and registers it in the registry.
 */
declare function defineReranker<OptionsType extends z.ZodTypeAny = z.ZodTypeAny>(registry: Registry, options: {
    name: string;
    configSchema?: OptionsType;
    info?: RerankerInfo;
}, runner: RerankerFn<OptionsType>): RerankerAction<OptionsType>;
/**
 *  Creates a reranker action for the provided {@link RerankerFn} implementation.
 */
declare function reranker<OptionsType extends z.ZodTypeAny = z.ZodTypeAny>(options: {
    name: string;
    configSchema?: OptionsType;
    info?: RerankerInfo;
}, runner: RerankerFn<OptionsType>): RerankerAction<OptionsType>;
interface RerankerParams<CustomOptions extends z.ZodTypeAny = z.ZodTypeAny> {
    reranker: RerankerArgument<CustomOptions>;
    query: string | DocumentData;
    documents: DocumentData[];
    options?: z.infer<CustomOptions>;
}
type RerankerArgument<CustomOptions extends z.ZodTypeAny = z.ZodTypeAny> = RerankerAction<CustomOptions> | RerankerReference<CustomOptions> | string;
/**
 * Reranks documents from a {@link RerankerArgument} based on the provided query.
 */
declare function rerank<CustomOptions extends z.ZodTypeAny>(registry: Registry, params: RerankerParams<CustomOptions>): Promise<Array<RankedDocument>>;
declare const CommonRerankerOptionsSchema: z.ZodObject<{
    k: z.ZodOptional<z.ZodNumber>;
}, "strip", z.ZodTypeAny, {
    k?: number | undefined;
}, {
    k?: number | undefined;
}>;
interface RerankerReference<CustomOptions extends z.ZodTypeAny> {
    name: string;
    configSchema?: CustomOptions;
    info?: RerankerInfo;
}
/**
 * Helper method to configure a {@link RerankerReference} to a plugin.
 */
declare function rerankerRef<CustomOptionsSchema extends z.ZodTypeAny = z.ZodTypeAny>(options: RerankerReference<CustomOptionsSchema>): RerankerReference<CustomOptionsSchema>;

export { CommonRerankerOptionsSchema, RankedDocument, type RankedDocumentData, RankedDocumentDataSchema, RankedDocumentMetadataSchema, type RerankerAction, type RerankerArgument, type RerankerFn, type RerankerInfo, RerankerInfoSchema, type RerankerParams, type RerankerReference, defineReranker, rerank, reranker, rerankerRef };
