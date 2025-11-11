import { z } from '@genkit-ai/core';

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

/**
 * Zod schema of message part.
 */
declare const PartSchema: z.ZodUnion<[z.ZodObject<{
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
}>]>;
/**
 * Message part.
 */
type Part = z.infer<typeof PartSchema>;
/**
 * Zod schema of a message role.
 */
declare const RoleSchema: z.ZodEnum<["system", "user", "model", "tool"]>;
/**
 * Message role.
 */
type Role = z.infer<typeof RoleSchema>;
/**
 * Zod schema of a message.
 */
declare const MessageSchema: z.ZodObject<{
    role: z.ZodEnum<["system", "user", "model", "tool"]>;
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
    metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
}, "strip", z.ZodTypeAny, {
    role: "model" | "system" | "user" | "tool";
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
    metadata?: Record<string, unknown> | undefined;
}, {
    role: "model" | "system" | "user" | "tool";
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
    metadata?: Record<string, unknown> | undefined;
}>;
/**
 * Model message data.
 */
type MessageData = z.infer<typeof MessageSchema>;
/**
 * Zod schema of model info metadata.
 */
declare const ModelInfoSchema: z.ZodObject<{
    /** Acceptable names for this model (e.g. different versions). */
    versions: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    /** Friendly label for this model (e.g. "Google AI - Gemini Pro") */
    label: z.ZodOptional<z.ZodString>;
    /** Model Specific configuration. */
    configSchema: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodAny>>;
    /** Supported model capabilities. */
    supports: z.ZodOptional<z.ZodObject<{
        /** Model can process historical messages passed with a prompt. */
        multiturn: z.ZodOptional<z.ZodBoolean>;
        /** Model can process media as part of the prompt (multimodal input). */
        media: z.ZodOptional<z.ZodBoolean>;
        /** Model can perform tool calls. */
        tools: z.ZodOptional<z.ZodBoolean>;
        /** Model can accept messages with role "system". */
        systemRole: z.ZodOptional<z.ZodBoolean>;
        /** Model can output this type of data. */
        output: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
        /** Model supports output in these content types. */
        contentType: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
        /** Model can natively support document-based context grounding. */
        context: z.ZodOptional<z.ZodBoolean>;
        /** Model can natively support constrained generation. */
        constrained: z.ZodOptional<z.ZodEnum<["none", "all", "no-tools"]>>;
        /** Model supports controlling tool choice, e.g. forced tool calling. */
        toolChoice: z.ZodOptional<z.ZodBoolean>;
    }, "strip", z.ZodTypeAny, {
        tools?: boolean | undefined;
        toolChoice?: boolean | undefined;
        output?: string[] | undefined;
        context?: boolean | undefined;
        media?: boolean | undefined;
        contentType?: string[] | undefined;
        constrained?: "none" | "all" | "no-tools" | undefined;
        multiturn?: boolean | undefined;
        systemRole?: boolean | undefined;
    }, {
        tools?: boolean | undefined;
        toolChoice?: boolean | undefined;
        output?: string[] | undefined;
        context?: boolean | undefined;
        media?: boolean | undefined;
        contentType?: string[] | undefined;
        constrained?: "none" | "all" | "no-tools" | undefined;
        multiturn?: boolean | undefined;
        systemRole?: boolean | undefined;
    }>>;
    /** At which stage of development this model is.
     * - `featured` models are recommended for general use.
     * - `stable` models are well-tested and reliable.
     * - `unstable` models are experimental and may change.
     * - `legacy` models are no longer recommended for new projects.
     * - `deprecated` models are deprecated by the provider and may be removed in future versions.
     */
    stage: z.ZodOptional<z.ZodEnum<["featured", "stable", "unstable", "legacy", "deprecated"]>>;
}, "strip", z.ZodTypeAny, {
    versions?: string[] | undefined;
    label?: string | undefined;
    configSchema?: Record<string, any> | undefined;
    supports?: {
        tools?: boolean | undefined;
        toolChoice?: boolean | undefined;
        output?: string[] | undefined;
        context?: boolean | undefined;
        media?: boolean | undefined;
        contentType?: string[] | undefined;
        constrained?: "none" | "all" | "no-tools" | undefined;
        multiturn?: boolean | undefined;
        systemRole?: boolean | undefined;
    } | undefined;
    stage?: "featured" | "stable" | "unstable" | "legacy" | "deprecated" | undefined;
}, {
    versions?: string[] | undefined;
    label?: string | undefined;
    configSchema?: Record<string, any> | undefined;
    supports?: {
        tools?: boolean | undefined;
        toolChoice?: boolean | undefined;
        output?: string[] | undefined;
        context?: boolean | undefined;
        media?: boolean | undefined;
        contentType?: string[] | undefined;
        constrained?: "none" | "all" | "no-tools" | undefined;
        multiturn?: boolean | undefined;
        systemRole?: boolean | undefined;
    } | undefined;
    stage?: "featured" | "stable" | "unstable" | "legacy" | "deprecated" | undefined;
}>;
/**
 * Model info metadata.
 */
type ModelInfo = z.infer<typeof ModelInfoSchema>;
/**
 * Zod schema of a tool definition.
 */
declare const ToolDefinitionSchema: z.ZodObject<{
    name: z.ZodString;
    description: z.ZodString;
    inputSchema: z.ZodOptional<z.ZodNullable<z.ZodRecord<z.ZodString, z.ZodAny>>>;
    outputSchema: z.ZodOptional<z.ZodNullable<z.ZodRecord<z.ZodString, z.ZodAny>>>;
    metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodAny>>;
}, "strip", z.ZodTypeAny, {
    name: string;
    description: string;
    metadata?: Record<string, any> | undefined;
    inputSchema?: Record<string, any> | null | undefined;
    outputSchema?: Record<string, any> | null | undefined;
}, {
    name: string;
    description: string;
    metadata?: Record<string, any> | undefined;
    inputSchema?: Record<string, any> | null | undefined;
    outputSchema?: Record<string, any> | null | undefined;
}>;
/**
 * Tool definition.
 */
type ToolDefinition = z.infer<typeof ToolDefinitionSchema>;
/**
 * Configuration parameter descriptions.
 */
declare const GenerationCommonConfigDescriptions: {
    temperature: string;
    maxOutputTokens: string;
    topK: string;
    topP: string;
};
/**
 * Zod schema of a common config object.
 */
declare const GenerationCommonConfigSchema: z.ZodObject<{
    version: z.ZodOptional<z.ZodString>;
    temperature: z.ZodOptional<z.ZodNumber>;
    maxOutputTokens: z.ZodOptional<z.ZodNumber>;
    topK: z.ZodOptional<z.ZodNumber>;
    topP: z.ZodOptional<z.ZodNumber>;
    stopSequences: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
}, "passthrough", z.ZodTypeAny, z.objectOutputType<{
    version: z.ZodOptional<z.ZodString>;
    temperature: z.ZodOptional<z.ZodNumber>;
    maxOutputTokens: z.ZodOptional<z.ZodNumber>;
    topK: z.ZodOptional<z.ZodNumber>;
    topP: z.ZodOptional<z.ZodNumber>;
    stopSequences: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
}, z.ZodTypeAny, "passthrough">, z.objectInputType<{
    version: z.ZodOptional<z.ZodString>;
    temperature: z.ZodOptional<z.ZodNumber>;
    maxOutputTokens: z.ZodOptional<z.ZodNumber>;
    topK: z.ZodOptional<z.ZodNumber>;
    topP: z.ZodOptional<z.ZodNumber>;
    stopSequences: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
}, z.ZodTypeAny, "passthrough">>;
/**
 * Common config object.
 */
type GenerationCommonConfig = typeof GenerationCommonConfigSchema;
/**
 * Zod schema of output config.
 */
declare const OutputConfigSchema: z.ZodObject<{
    format: z.ZodOptional<z.ZodString>;
    schema: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodAny>>;
    constrained: z.ZodOptional<z.ZodBoolean>;
    contentType: z.ZodOptional<z.ZodString>;
}, "strip", z.ZodTypeAny, {
    contentType?: string | undefined;
    format?: string | undefined;
    schema?: Record<string, any> | undefined;
    constrained?: boolean | undefined;
}, {
    contentType?: string | undefined;
    format?: string | undefined;
    schema?: Record<string, any> | undefined;
    constrained?: boolean | undefined;
}>;
/**
 * Output config.
 */
type OutputConfig = z.infer<typeof OutputConfigSchema>;
/** ModelRequestSchema represents the parameters that are passed to a model when generating content. */
declare const ModelRequestSchema: z.ZodObject<{
    messages: z.ZodArray<z.ZodObject<{
        role: z.ZodEnum<["system", "user", "model", "tool"]>;
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
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
    }, "strip", z.ZodTypeAny, {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    }, {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    }>, "many">;
    config: z.ZodOptional<z.ZodAny>;
    tools: z.ZodOptional<z.ZodArray<z.ZodObject<{
        name: z.ZodString;
        description: z.ZodString;
        inputSchema: z.ZodOptional<z.ZodNullable<z.ZodRecord<z.ZodString, z.ZodAny>>>;
        outputSchema: z.ZodOptional<z.ZodNullable<z.ZodRecord<z.ZodString, z.ZodAny>>>;
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodAny>>;
    }, "strip", z.ZodTypeAny, {
        name: string;
        description: string;
        metadata?: Record<string, any> | undefined;
        inputSchema?: Record<string, any> | null | undefined;
        outputSchema?: Record<string, any> | null | undefined;
    }, {
        name: string;
        description: string;
        metadata?: Record<string, any> | undefined;
        inputSchema?: Record<string, any> | null | undefined;
        outputSchema?: Record<string, any> | null | undefined;
    }>, "many">>;
    toolChoice: z.ZodOptional<z.ZodEnum<["auto", "required", "none"]>>;
    output: z.ZodOptional<z.ZodObject<{
        format: z.ZodOptional<z.ZodString>;
        schema: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodAny>>;
        constrained: z.ZodOptional<z.ZodBoolean>;
        contentType: z.ZodOptional<z.ZodString>;
    }, "strip", z.ZodTypeAny, {
        contentType?: string | undefined;
        format?: string | undefined;
        schema?: Record<string, any> | undefined;
        constrained?: boolean | undefined;
    }, {
        contentType?: string | undefined;
        format?: string | undefined;
        schema?: Record<string, any> | undefined;
        constrained?: boolean | undefined;
    }>>;
    docs: z.ZodOptional<z.ZodArray<z.ZodObject<{
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
    }>, "many">>;
}, "strip", z.ZodTypeAny, {
    messages: {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    }[];
    docs?: {
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
    }[] | undefined;
    tools?: {
        name: string;
        description: string;
        metadata?: Record<string, any> | undefined;
        inputSchema?: Record<string, any> | null | undefined;
        outputSchema?: Record<string, any> | null | undefined;
    }[] | undefined;
    toolChoice?: "auto" | "required" | "none" | undefined;
    config?: any;
    output?: {
        contentType?: string | undefined;
        format?: string | undefined;
        schema?: Record<string, any> | undefined;
        constrained?: boolean | undefined;
    } | undefined;
}, {
    messages: {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    }[];
    docs?: {
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
    }[] | undefined;
    tools?: {
        name: string;
        description: string;
        metadata?: Record<string, any> | undefined;
        inputSchema?: Record<string, any> | null | undefined;
        outputSchema?: Record<string, any> | null | undefined;
    }[] | undefined;
    toolChoice?: "auto" | "required" | "none" | undefined;
    config?: any;
    output?: {
        contentType?: string | undefined;
        format?: string | undefined;
        schema?: Record<string, any> | undefined;
        constrained?: boolean | undefined;
    } | undefined;
}>;
/** ModelRequest represents the parameters that are passed to a model when generating content. */
interface ModelRequest<CustomOptionsSchema extends z.ZodTypeAny = z.ZodTypeAny> extends z.infer<typeof ModelRequestSchema> {
    config?: z.infer<CustomOptionsSchema>;
}
/**
 * Zod schema of a generate request.
 */
declare const GenerateRequestSchema: z.ZodObject<{
    messages: z.ZodArray<z.ZodObject<{
        role: z.ZodEnum<["system", "user", "model", "tool"]>;
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
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
    }, "strip", z.ZodTypeAny, {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    }, {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    }>, "many">;
    config: z.ZodOptional<z.ZodAny>;
    tools: z.ZodOptional<z.ZodArray<z.ZodObject<{
        name: z.ZodString;
        description: z.ZodString;
        inputSchema: z.ZodOptional<z.ZodNullable<z.ZodRecord<z.ZodString, z.ZodAny>>>;
        outputSchema: z.ZodOptional<z.ZodNullable<z.ZodRecord<z.ZodString, z.ZodAny>>>;
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodAny>>;
    }, "strip", z.ZodTypeAny, {
        name: string;
        description: string;
        metadata?: Record<string, any> | undefined;
        inputSchema?: Record<string, any> | null | undefined;
        outputSchema?: Record<string, any> | null | undefined;
    }, {
        name: string;
        description: string;
        metadata?: Record<string, any> | undefined;
        inputSchema?: Record<string, any> | null | undefined;
        outputSchema?: Record<string, any> | null | undefined;
    }>, "many">>;
    toolChoice: z.ZodOptional<z.ZodEnum<["auto", "required", "none"]>>;
    output: z.ZodOptional<z.ZodObject<{
        format: z.ZodOptional<z.ZodString>;
        schema: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodAny>>;
        constrained: z.ZodOptional<z.ZodBoolean>;
        contentType: z.ZodOptional<z.ZodString>;
    }, "strip", z.ZodTypeAny, {
        contentType?: string | undefined;
        format?: string | undefined;
        schema?: Record<string, any> | undefined;
        constrained?: boolean | undefined;
    }, {
        contentType?: string | undefined;
        format?: string | undefined;
        schema?: Record<string, any> | undefined;
        constrained?: boolean | undefined;
    }>>;
    docs: z.ZodOptional<z.ZodArray<z.ZodObject<{
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
    }>, "many">>;
} & {
    /** @deprecated All responses now return a single candidate. This will always be `undefined`. */
    candidates: z.ZodOptional<z.ZodNumber>;
}, "strip", z.ZodTypeAny, {
    messages: {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    }[];
    docs?: {
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
    }[] | undefined;
    tools?: {
        name: string;
        description: string;
        metadata?: Record<string, any> | undefined;
        inputSchema?: Record<string, any> | null | undefined;
        outputSchema?: Record<string, any> | null | undefined;
    }[] | undefined;
    toolChoice?: "auto" | "required" | "none" | undefined;
    config?: any;
    output?: {
        contentType?: string | undefined;
        format?: string | undefined;
        schema?: Record<string, any> | undefined;
        constrained?: boolean | undefined;
    } | undefined;
    candidates?: number | undefined;
}, {
    messages: {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    }[];
    docs?: {
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
    }[] | undefined;
    tools?: {
        name: string;
        description: string;
        metadata?: Record<string, any> | undefined;
        inputSchema?: Record<string, any> | null | undefined;
        outputSchema?: Record<string, any> | null | undefined;
    }[] | undefined;
    toolChoice?: "auto" | "required" | "none" | undefined;
    config?: any;
    output?: {
        contentType?: string | undefined;
        format?: string | undefined;
        schema?: Record<string, any> | undefined;
        constrained?: boolean | undefined;
    } | undefined;
    candidates?: number | undefined;
}>;
/**
 * Generate request data.
 */
type GenerateRequestData = z.infer<typeof GenerateRequestSchema>;
/**
 * Generate request.
 */
interface GenerateRequest<CustomOptionsSchema extends z.ZodTypeAny = z.ZodTypeAny> extends z.infer<typeof GenerateRequestSchema> {
    config?: z.infer<CustomOptionsSchema>;
}
/**
 * Zod schema of usage info from a generate request.
 */
declare const GenerationUsageSchema: z.ZodObject<{
    inputTokens: z.ZodOptional<z.ZodNumber>;
    outputTokens: z.ZodOptional<z.ZodNumber>;
    totalTokens: z.ZodOptional<z.ZodNumber>;
    inputCharacters: z.ZodOptional<z.ZodNumber>;
    outputCharacters: z.ZodOptional<z.ZodNumber>;
    inputImages: z.ZodOptional<z.ZodNumber>;
    outputImages: z.ZodOptional<z.ZodNumber>;
    inputVideos: z.ZodOptional<z.ZodNumber>;
    outputVideos: z.ZodOptional<z.ZodNumber>;
    inputAudioFiles: z.ZodOptional<z.ZodNumber>;
    outputAudioFiles: z.ZodOptional<z.ZodNumber>;
    custom: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodNumber>>;
    thoughtsTokens: z.ZodOptional<z.ZodNumber>;
    cachedContentTokens: z.ZodOptional<z.ZodNumber>;
}, "strip", z.ZodTypeAny, {
    custom?: Record<string, number> | undefined;
    inputTokens?: number | undefined;
    outputTokens?: number | undefined;
    totalTokens?: number | undefined;
    inputCharacters?: number | undefined;
    outputCharacters?: number | undefined;
    inputImages?: number | undefined;
    outputImages?: number | undefined;
    inputVideos?: number | undefined;
    outputVideos?: number | undefined;
    inputAudioFiles?: number | undefined;
    outputAudioFiles?: number | undefined;
    thoughtsTokens?: number | undefined;
    cachedContentTokens?: number | undefined;
}, {
    custom?: Record<string, number> | undefined;
    inputTokens?: number | undefined;
    outputTokens?: number | undefined;
    totalTokens?: number | undefined;
    inputCharacters?: number | undefined;
    outputCharacters?: number | undefined;
    inputImages?: number | undefined;
    outputImages?: number | undefined;
    inputVideos?: number | undefined;
    outputVideos?: number | undefined;
    inputAudioFiles?: number | undefined;
    outputAudioFiles?: number | undefined;
    thoughtsTokens?: number | undefined;
    cachedContentTokens?: number | undefined;
}>;
/**
 * Usage info from a generate request.
 */
type GenerationUsage = z.infer<typeof GenerationUsageSchema>;
/** Model response finish reason enum. */
declare const FinishReasonSchema: z.ZodEnum<["stop", "length", "blocked", "interrupted", "other", "unknown"]>;
/** @deprecated All responses now return a single candidate. Only the first candidate will be used if supplied. */
declare const CandidateSchema: z.ZodObject<{
    index: z.ZodNumber;
    message: z.ZodObject<{
        role: z.ZodEnum<["system", "user", "model", "tool"]>;
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
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
    }, "strip", z.ZodTypeAny, {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    }, {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    }>;
    usage: z.ZodOptional<z.ZodObject<{
        inputTokens: z.ZodOptional<z.ZodNumber>;
        outputTokens: z.ZodOptional<z.ZodNumber>;
        totalTokens: z.ZodOptional<z.ZodNumber>;
        inputCharacters: z.ZodOptional<z.ZodNumber>;
        outputCharacters: z.ZodOptional<z.ZodNumber>;
        inputImages: z.ZodOptional<z.ZodNumber>;
        outputImages: z.ZodOptional<z.ZodNumber>;
        inputVideos: z.ZodOptional<z.ZodNumber>;
        outputVideos: z.ZodOptional<z.ZodNumber>;
        inputAudioFiles: z.ZodOptional<z.ZodNumber>;
        outputAudioFiles: z.ZodOptional<z.ZodNumber>;
        custom: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodNumber>>;
        thoughtsTokens: z.ZodOptional<z.ZodNumber>;
        cachedContentTokens: z.ZodOptional<z.ZodNumber>;
    }, "strip", z.ZodTypeAny, {
        custom?: Record<string, number> | undefined;
        inputTokens?: number | undefined;
        outputTokens?: number | undefined;
        totalTokens?: number | undefined;
        inputCharacters?: number | undefined;
        outputCharacters?: number | undefined;
        inputImages?: number | undefined;
        outputImages?: number | undefined;
        inputVideos?: number | undefined;
        outputVideos?: number | undefined;
        inputAudioFiles?: number | undefined;
        outputAudioFiles?: number | undefined;
        thoughtsTokens?: number | undefined;
        cachedContentTokens?: number | undefined;
    }, {
        custom?: Record<string, number> | undefined;
        inputTokens?: number | undefined;
        outputTokens?: number | undefined;
        totalTokens?: number | undefined;
        inputCharacters?: number | undefined;
        outputCharacters?: number | undefined;
        inputImages?: number | undefined;
        outputImages?: number | undefined;
        inputVideos?: number | undefined;
        outputVideos?: number | undefined;
        inputAudioFiles?: number | undefined;
        outputAudioFiles?: number | undefined;
        thoughtsTokens?: number | undefined;
        cachedContentTokens?: number | undefined;
    }>>;
    finishReason: z.ZodEnum<["stop", "length", "blocked", "interrupted", "other", "unknown"]>;
    finishMessage: z.ZodOptional<z.ZodString>;
    custom: z.ZodUnknown;
}, "strip", z.ZodTypeAny, {
    message: {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    };
    finishReason: "length" | "unknown" | "stop" | "blocked" | "interrupted" | "other";
    index: number;
    custom?: unknown;
    finishMessage?: string | undefined;
    usage?: {
        custom?: Record<string, number> | undefined;
        inputTokens?: number | undefined;
        outputTokens?: number | undefined;
        totalTokens?: number | undefined;
        inputCharacters?: number | undefined;
        outputCharacters?: number | undefined;
        inputImages?: number | undefined;
        outputImages?: number | undefined;
        inputVideos?: number | undefined;
        outputVideos?: number | undefined;
        inputAudioFiles?: number | undefined;
        outputAudioFiles?: number | undefined;
        thoughtsTokens?: number | undefined;
        cachedContentTokens?: number | undefined;
    } | undefined;
}, {
    message: {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    };
    finishReason: "length" | "unknown" | "stop" | "blocked" | "interrupted" | "other";
    index: number;
    custom?: unknown;
    finishMessage?: string | undefined;
    usage?: {
        custom?: Record<string, number> | undefined;
        inputTokens?: number | undefined;
        outputTokens?: number | undefined;
        totalTokens?: number | undefined;
        inputCharacters?: number | undefined;
        outputCharacters?: number | undefined;
        inputImages?: number | undefined;
        outputImages?: number | undefined;
        inputVideos?: number | undefined;
        outputVideos?: number | undefined;
        inputAudioFiles?: number | undefined;
        outputAudioFiles?: number | undefined;
        thoughtsTokens?: number | undefined;
        cachedContentTokens?: number | undefined;
    } | undefined;
}>;
/** @deprecated All responses now return a single candidate. Only the first candidate will be used if supplied. */
type CandidateData = z.infer<typeof CandidateSchema>;
/** @deprecated All responses now return a single candidate. Only the first candidate will be used if supplied. */
declare const CandidateErrorSchema: z.ZodObject<{
    index: z.ZodNumber;
    code: z.ZodEnum<["blocked", "other", "unknown"]>;
    message: z.ZodOptional<z.ZodString>;
}, "strip", z.ZodTypeAny, {
    code: "unknown" | "blocked" | "other";
    index: number;
    message?: string | undefined;
}, {
    code: "unknown" | "blocked" | "other";
    index: number;
    message?: string | undefined;
}>;
/** @deprecated All responses now return a single candidate. Only the first candidate will be used if supplied. */
type CandidateError = z.infer<typeof CandidateErrorSchema>;
/**
 * Zod schema of a model response.
 */
declare const ModelResponseSchema: z.ZodObject<{
    message: z.ZodOptional<z.ZodObject<{
        role: z.ZodEnum<["system", "user", "model", "tool"]>;
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
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
    }, "strip", z.ZodTypeAny, {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    }, {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    }>>;
    finishReason: z.ZodEnum<["stop", "length", "blocked", "interrupted", "other", "unknown"]>;
    finishMessage: z.ZodOptional<z.ZodString>;
    latencyMs: z.ZodOptional<z.ZodNumber>;
    usage: z.ZodOptional<z.ZodObject<{
        inputTokens: z.ZodOptional<z.ZodNumber>;
        outputTokens: z.ZodOptional<z.ZodNumber>;
        totalTokens: z.ZodOptional<z.ZodNumber>;
        inputCharacters: z.ZodOptional<z.ZodNumber>;
        outputCharacters: z.ZodOptional<z.ZodNumber>;
        inputImages: z.ZodOptional<z.ZodNumber>;
        outputImages: z.ZodOptional<z.ZodNumber>;
        inputVideos: z.ZodOptional<z.ZodNumber>;
        outputVideos: z.ZodOptional<z.ZodNumber>;
        inputAudioFiles: z.ZodOptional<z.ZodNumber>;
        outputAudioFiles: z.ZodOptional<z.ZodNumber>;
        custom: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodNumber>>;
        thoughtsTokens: z.ZodOptional<z.ZodNumber>;
        cachedContentTokens: z.ZodOptional<z.ZodNumber>;
    }, "strip", z.ZodTypeAny, {
        custom?: Record<string, number> | undefined;
        inputTokens?: number | undefined;
        outputTokens?: number | undefined;
        totalTokens?: number | undefined;
        inputCharacters?: number | undefined;
        outputCharacters?: number | undefined;
        inputImages?: number | undefined;
        outputImages?: number | undefined;
        inputVideos?: number | undefined;
        outputVideos?: number | undefined;
        inputAudioFiles?: number | undefined;
        outputAudioFiles?: number | undefined;
        thoughtsTokens?: number | undefined;
        cachedContentTokens?: number | undefined;
    }, {
        custom?: Record<string, number> | undefined;
        inputTokens?: number | undefined;
        outputTokens?: number | undefined;
        totalTokens?: number | undefined;
        inputCharacters?: number | undefined;
        outputCharacters?: number | undefined;
        inputImages?: number | undefined;
        outputImages?: number | undefined;
        inputVideos?: number | undefined;
        outputVideos?: number | undefined;
        inputAudioFiles?: number | undefined;
        outputAudioFiles?: number | undefined;
        thoughtsTokens?: number | undefined;
        cachedContentTokens?: number | undefined;
    }>>;
    /** @deprecated use `raw` instead */
    custom: z.ZodUnknown;
    raw: z.ZodUnknown;
    request: z.ZodOptional<z.ZodObject<{
        messages: z.ZodArray<z.ZodObject<{
            role: z.ZodEnum<["system", "user", "model", "tool"]>;
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
            metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
        }, "strip", z.ZodTypeAny, {
            role: "model" | "system" | "user" | "tool";
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
            metadata?: Record<string, unknown> | undefined;
        }, {
            role: "model" | "system" | "user" | "tool";
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
            metadata?: Record<string, unknown> | undefined;
        }>, "many">;
        config: z.ZodOptional<z.ZodAny>;
        tools: z.ZodOptional<z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            description: z.ZodString;
            inputSchema: z.ZodOptional<z.ZodNullable<z.ZodRecord<z.ZodString, z.ZodAny>>>;
            outputSchema: z.ZodOptional<z.ZodNullable<z.ZodRecord<z.ZodString, z.ZodAny>>>;
            metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodAny>>;
        }, "strip", z.ZodTypeAny, {
            name: string;
            description: string;
            metadata?: Record<string, any> | undefined;
            inputSchema?: Record<string, any> | null | undefined;
            outputSchema?: Record<string, any> | null | undefined;
        }, {
            name: string;
            description: string;
            metadata?: Record<string, any> | undefined;
            inputSchema?: Record<string, any> | null | undefined;
            outputSchema?: Record<string, any> | null | undefined;
        }>, "many">>;
        toolChoice: z.ZodOptional<z.ZodEnum<["auto", "required", "none"]>>;
        output: z.ZodOptional<z.ZodObject<{
            format: z.ZodOptional<z.ZodString>;
            schema: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodAny>>;
            constrained: z.ZodOptional<z.ZodBoolean>;
            contentType: z.ZodOptional<z.ZodString>;
        }, "strip", z.ZodTypeAny, {
            contentType?: string | undefined;
            format?: string | undefined;
            schema?: Record<string, any> | undefined;
            constrained?: boolean | undefined;
        }, {
            contentType?: string | undefined;
            format?: string | undefined;
            schema?: Record<string, any> | undefined;
            constrained?: boolean | undefined;
        }>>;
        docs: z.ZodOptional<z.ZodArray<z.ZodObject<{
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
        }>, "many">>;
    } & {
        /** @deprecated All responses now return a single candidate. This will always be `undefined`. */
        candidates: z.ZodOptional<z.ZodNumber>;
    }, "strip", z.ZodTypeAny, {
        messages: {
            role: "model" | "system" | "user" | "tool";
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
            metadata?: Record<string, unknown> | undefined;
        }[];
        docs?: {
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
        }[] | undefined;
        tools?: {
            name: string;
            description: string;
            metadata?: Record<string, any> | undefined;
            inputSchema?: Record<string, any> | null | undefined;
            outputSchema?: Record<string, any> | null | undefined;
        }[] | undefined;
        toolChoice?: "auto" | "required" | "none" | undefined;
        config?: any;
        output?: {
            contentType?: string | undefined;
            format?: string | undefined;
            schema?: Record<string, any> | undefined;
            constrained?: boolean | undefined;
        } | undefined;
        candidates?: number | undefined;
    }, {
        messages: {
            role: "model" | "system" | "user" | "tool";
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
            metadata?: Record<string, unknown> | undefined;
        }[];
        docs?: {
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
        }[] | undefined;
        tools?: {
            name: string;
            description: string;
            metadata?: Record<string, any> | undefined;
            inputSchema?: Record<string, any> | null | undefined;
            outputSchema?: Record<string, any> | null | undefined;
        }[] | undefined;
        toolChoice?: "auto" | "required" | "none" | undefined;
        config?: any;
        output?: {
            contentType?: string | undefined;
            format?: string | undefined;
            schema?: Record<string, any> | undefined;
            constrained?: boolean | undefined;
        } | undefined;
        candidates?: number | undefined;
    }>>;
    operation: z.ZodOptional<z.ZodObject<{
        action: z.ZodOptional<z.ZodString>;
        id: z.ZodString;
        done: z.ZodOptional<z.ZodBoolean>;
        output: z.ZodOptional<z.ZodAny>;
        error: z.ZodOptional<z.ZodObject<{
            message: z.ZodString;
        }, "passthrough", z.ZodTypeAny, z.objectOutputType<{
            message: z.ZodString;
        }, z.ZodTypeAny, "passthrough">, z.objectInputType<{
            message: z.ZodString;
        }, z.ZodTypeAny, "passthrough">>>;
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodAny>>;
    }, "strip", z.ZodTypeAny, {
        id: string;
        error?: z.objectOutputType<{
            message: z.ZodString;
        }, z.ZodTypeAny, "passthrough"> | undefined;
        output?: any;
        metadata?: Record<string, any> | undefined;
        action?: string | undefined; /** At which stage of development this model is.
         * - `featured` models are recommended for general use.
         * - `stable` models are well-tested and reliable.
         * - `unstable` models are experimental and may change.
         * - `legacy` models are no longer recommended for new projects.
         * - `deprecated` models are deprecated by the provider and may be removed in future versions.
         */
        done?: boolean | undefined;
    }, {
        id: string;
        error?: z.objectInputType<{
            message: z.ZodString;
        }, z.ZodTypeAny, "passthrough"> | undefined;
        output?: any;
        metadata?: Record<string, any> | undefined;
        action?: string | undefined;
        done?: boolean | undefined;
    }>>;
}, "strip", z.ZodTypeAny, {
    finishReason: "length" | "unknown" | "stop" | "blocked" | "interrupted" | "other";
    message?: {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    } | undefined;
    custom?: unknown;
    finishMessage?: string | undefined;
    latencyMs?: number | undefined;
    usage?: {
        custom?: Record<string, number> | undefined;
        inputTokens?: number | undefined;
        outputTokens?: number | undefined;
        totalTokens?: number | undefined;
        inputCharacters?: number | undefined;
        outputCharacters?: number | undefined;
        inputImages?: number | undefined;
        outputImages?: number | undefined;
        inputVideos?: number | undefined;
        outputVideos?: number | undefined;
        inputAudioFiles?: number | undefined;
        outputAudioFiles?: number | undefined;
        thoughtsTokens?: number | undefined;
        cachedContentTokens?: number | undefined;
    } | undefined;
    raw?: unknown;
    request?: {
        messages: {
            role: "model" | "system" | "user" | "tool";
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
            metadata?: Record<string, unknown> | undefined;
        }[];
        docs?: {
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
        }[] | undefined;
        tools?: {
            name: string;
            description: string;
            metadata?: Record<string, any> | undefined;
            inputSchema?: Record<string, any> | null | undefined;
            outputSchema?: Record<string, any> | null | undefined;
        }[] | undefined;
        toolChoice?: "auto" | "required" | "none" | undefined;
        config?: any;
        output?: {
            contentType?: string | undefined;
            format?: string | undefined;
            schema?: Record<string, any> | undefined;
            constrained?: boolean | undefined;
        } | undefined;
        candidates?: number | undefined;
    } | undefined;
    operation?: {
        id: string;
        error?: z.objectOutputType<{
            message: z.ZodString;
        }, z.ZodTypeAny, "passthrough"> | undefined;
        output?: any;
        metadata?: Record<string, any> | undefined;
        action?: string | undefined; /** At which stage of development this model is.
         * - `featured` models are recommended for general use.
         * - `stable` models are well-tested and reliable.
         * - `unstable` models are experimental and may change.
         * - `legacy` models are no longer recommended for new projects.
         * - `deprecated` models are deprecated by the provider and may be removed in future versions.
         */
        done?: boolean | undefined;
    } | undefined;
}, {
    finishReason: "length" | "unknown" | "stop" | "blocked" | "interrupted" | "other";
    message?: {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    } | undefined;
    custom?: unknown;
    finishMessage?: string | undefined;
    latencyMs?: number | undefined;
    usage?: {
        custom?: Record<string, number> | undefined;
        inputTokens?: number | undefined;
        outputTokens?: number | undefined;
        totalTokens?: number | undefined;
        inputCharacters?: number | undefined;
        outputCharacters?: number | undefined;
        inputImages?: number | undefined;
        outputImages?: number | undefined;
        inputVideos?: number | undefined;
        outputVideos?: number | undefined;
        inputAudioFiles?: number | undefined;
        outputAudioFiles?: number | undefined;
        thoughtsTokens?: number | undefined;
        cachedContentTokens?: number | undefined;
    } | undefined;
    raw?: unknown;
    request?: {
        messages: {
            role: "model" | "system" | "user" | "tool";
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
            metadata?: Record<string, unknown> | undefined;
        }[];
        docs?: {
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
        }[] | undefined;
        tools?: {
            name: string;
            description: string;
            metadata?: Record<string, any> | undefined;
            inputSchema?: Record<string, any> | null | undefined;
            outputSchema?: Record<string, any> | null | undefined;
        }[] | undefined;
        toolChoice?: "auto" | "required" | "none" | undefined;
        config?: any;
        output?: {
            contentType?: string | undefined;
            format?: string | undefined;
            schema?: Record<string, any> | undefined;
            constrained?: boolean | undefined;
        } | undefined;
        candidates?: number | undefined;
    } | undefined;
    operation?: {
        id: string;
        error?: z.objectInputType<{
            message: z.ZodString;
        }, z.ZodTypeAny, "passthrough"> | undefined;
        output?: any;
        metadata?: Record<string, any> | undefined;
        action?: string | undefined;
        done?: boolean | undefined;
    } | undefined;
}>;
/**
 * Model response data.
 */
type ModelResponseData = z.infer<typeof ModelResponseSchema>;
/**
 * Zod schema of generaete response.
 */
declare const GenerateResponseSchema: z.ZodObject<{
    message: z.ZodOptional<z.ZodObject<{
        role: z.ZodEnum<["system", "user", "model", "tool"]>;
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
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
    }, "strip", z.ZodTypeAny, {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    }, {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    }>>;
    finishMessage: z.ZodOptional<z.ZodString>;
    latencyMs: z.ZodOptional<z.ZodNumber>;
    usage: z.ZodOptional<z.ZodObject<{
        inputTokens: z.ZodOptional<z.ZodNumber>;
        outputTokens: z.ZodOptional<z.ZodNumber>;
        totalTokens: z.ZodOptional<z.ZodNumber>;
        inputCharacters: z.ZodOptional<z.ZodNumber>;
        outputCharacters: z.ZodOptional<z.ZodNumber>;
        inputImages: z.ZodOptional<z.ZodNumber>;
        outputImages: z.ZodOptional<z.ZodNumber>;
        inputVideos: z.ZodOptional<z.ZodNumber>;
        outputVideos: z.ZodOptional<z.ZodNumber>;
        inputAudioFiles: z.ZodOptional<z.ZodNumber>;
        outputAudioFiles: z.ZodOptional<z.ZodNumber>;
        custom: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodNumber>>;
        thoughtsTokens: z.ZodOptional<z.ZodNumber>;
        cachedContentTokens: z.ZodOptional<z.ZodNumber>;
    }, "strip", z.ZodTypeAny, {
        custom?: Record<string, number> | undefined;
        inputTokens?: number | undefined;
        outputTokens?: number | undefined;
        totalTokens?: number | undefined;
        inputCharacters?: number | undefined;
        outputCharacters?: number | undefined;
        inputImages?: number | undefined;
        outputImages?: number | undefined;
        inputVideos?: number | undefined;
        outputVideos?: number | undefined;
        inputAudioFiles?: number | undefined;
        outputAudioFiles?: number | undefined;
        thoughtsTokens?: number | undefined;
        cachedContentTokens?: number | undefined;
    }, {
        custom?: Record<string, number> | undefined;
        inputTokens?: number | undefined;
        outputTokens?: number | undefined;
        totalTokens?: number | undefined;
        inputCharacters?: number | undefined;
        outputCharacters?: number | undefined;
        inputImages?: number | undefined;
        outputImages?: number | undefined;
        inputVideos?: number | undefined;
        outputVideos?: number | undefined;
        inputAudioFiles?: number | undefined;
        outputAudioFiles?: number | undefined;
        thoughtsTokens?: number | undefined;
        cachedContentTokens?: number | undefined;
    }>>;
    custom: z.ZodUnknown;
    raw: z.ZodUnknown;
    request: z.ZodOptional<z.ZodObject<{
        messages: z.ZodArray<z.ZodObject<{
            role: z.ZodEnum<["system", "user", "model", "tool"]>;
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
            metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
        }, "strip", z.ZodTypeAny, {
            role: "model" | "system" | "user" | "tool";
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
            metadata?: Record<string, unknown> | undefined;
        }, {
            role: "model" | "system" | "user" | "tool";
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
            metadata?: Record<string, unknown> | undefined;
        }>, "many">;
        config: z.ZodOptional<z.ZodAny>;
        tools: z.ZodOptional<z.ZodArray<z.ZodObject<{
            name: z.ZodString;
            description: z.ZodString;
            inputSchema: z.ZodOptional<z.ZodNullable<z.ZodRecord<z.ZodString, z.ZodAny>>>;
            outputSchema: z.ZodOptional<z.ZodNullable<z.ZodRecord<z.ZodString, z.ZodAny>>>;
            metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodAny>>;
        }, "strip", z.ZodTypeAny, {
            name: string;
            description: string;
            metadata?: Record<string, any> | undefined;
            inputSchema?: Record<string, any> | null | undefined;
            outputSchema?: Record<string, any> | null | undefined;
        }, {
            name: string;
            description: string;
            metadata?: Record<string, any> | undefined;
            inputSchema?: Record<string, any> | null | undefined;
            outputSchema?: Record<string, any> | null | undefined;
        }>, "many">>;
        toolChoice: z.ZodOptional<z.ZodEnum<["auto", "required", "none"]>>;
        output: z.ZodOptional<z.ZodObject<{
            format: z.ZodOptional<z.ZodString>;
            schema: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodAny>>;
            constrained: z.ZodOptional<z.ZodBoolean>;
            contentType: z.ZodOptional<z.ZodString>;
        }, "strip", z.ZodTypeAny, {
            contentType?: string | undefined;
            format?: string | undefined;
            schema?: Record<string, any> | undefined;
            constrained?: boolean | undefined;
        }, {
            contentType?: string | undefined;
            format?: string | undefined;
            schema?: Record<string, any> | undefined;
            constrained?: boolean | undefined;
        }>>;
        docs: z.ZodOptional<z.ZodArray<z.ZodObject<{
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
        }>, "many">>;
    } & {
        /** @deprecated All responses now return a single candidate. This will always be `undefined`. */
        candidates: z.ZodOptional<z.ZodNumber>;
    }, "strip", z.ZodTypeAny, {
        messages: {
            role: "model" | "system" | "user" | "tool";
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
            metadata?: Record<string, unknown> | undefined;
        }[];
        docs?: {
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
        }[] | undefined;
        tools?: {
            name: string;
            description: string;
            metadata?: Record<string, any> | undefined;
            inputSchema?: Record<string, any> | null | undefined;
            outputSchema?: Record<string, any> | null | undefined;
        }[] | undefined;
        toolChoice?: "auto" | "required" | "none" | undefined;
        config?: any;
        output?: {
            contentType?: string | undefined;
            format?: string | undefined;
            schema?: Record<string, any> | undefined;
            constrained?: boolean | undefined;
        } | undefined;
        candidates?: number | undefined;
    }, {
        messages: {
            role: "model" | "system" | "user" | "tool";
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
            metadata?: Record<string, unknown> | undefined;
        }[];
        docs?: {
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
        }[] | undefined;
        tools?: {
            name: string;
            description: string;
            metadata?: Record<string, any> | undefined;
            inputSchema?: Record<string, any> | null | undefined;
            outputSchema?: Record<string, any> | null | undefined;
        }[] | undefined;
        toolChoice?: "auto" | "required" | "none" | undefined;
        config?: any;
        output?: {
            contentType?: string | undefined;
            format?: string | undefined;
            schema?: Record<string, any> | undefined;
            constrained?: boolean | undefined;
        } | undefined;
        candidates?: number | undefined;
    }>>;
    operation: z.ZodOptional<z.ZodObject<{
        action: z.ZodOptional<z.ZodString>;
        id: z.ZodString;
        done: z.ZodOptional<z.ZodBoolean>;
        output: z.ZodOptional<z.ZodAny>;
        error: z.ZodOptional<z.ZodObject<{
            message: z.ZodString;
        }, "passthrough", z.ZodTypeAny, z.objectOutputType<{
            message: z.ZodString;
        }, z.ZodTypeAny, "passthrough">, z.objectInputType<{
            message: z.ZodString;
        }, z.ZodTypeAny, "passthrough">>>;
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodAny>>;
    }, "strip", z.ZodTypeAny, {
        id: string;
        error?: z.objectOutputType<{
            message: z.ZodString;
        }, z.ZodTypeAny, "passthrough"> | undefined;
        output?: any;
        metadata?: Record<string, any> | undefined;
        action?: string | undefined; /** At which stage of development this model is.
         * - `featured` models are recommended for general use.
         * - `stable` models are well-tested and reliable.
         * - `unstable` models are experimental and may change.
         * - `legacy` models are no longer recommended for new projects.
         * - `deprecated` models are deprecated by the provider and may be removed in future versions.
         */
        done?: boolean | undefined;
    }, {
        id: string;
        error?: z.objectInputType<{
            message: z.ZodString;
        }, z.ZodTypeAny, "passthrough"> | undefined;
        output?: any;
        metadata?: Record<string, any> | undefined;
        action?: string | undefined;
        done?: boolean | undefined;
    }>>;
} & {
    candidates: z.ZodOptional<z.ZodArray<z.ZodObject<{
        index: z.ZodNumber;
        message: z.ZodObject<{
            role: z.ZodEnum<["system", "user", "model", "tool"]>;
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
            metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
        }, "strip", z.ZodTypeAny, {
            role: "model" | "system" | "user" | "tool";
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
            metadata?: Record<string, unknown> | undefined;
        }, {
            role: "model" | "system" | "user" | "tool";
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
            metadata?: Record<string, unknown> | undefined;
        }>;
        usage: z.ZodOptional<z.ZodObject<{
            inputTokens: z.ZodOptional<z.ZodNumber>;
            outputTokens: z.ZodOptional<z.ZodNumber>;
            totalTokens: z.ZodOptional<z.ZodNumber>;
            inputCharacters: z.ZodOptional<z.ZodNumber>;
            outputCharacters: z.ZodOptional<z.ZodNumber>;
            inputImages: z.ZodOptional<z.ZodNumber>;
            outputImages: z.ZodOptional<z.ZodNumber>;
            inputVideos: z.ZodOptional<z.ZodNumber>;
            outputVideos: z.ZodOptional<z.ZodNumber>;
            inputAudioFiles: z.ZodOptional<z.ZodNumber>;
            outputAudioFiles: z.ZodOptional<z.ZodNumber>;
            custom: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodNumber>>;
            thoughtsTokens: z.ZodOptional<z.ZodNumber>;
            cachedContentTokens: z.ZodOptional<z.ZodNumber>;
        }, "strip", z.ZodTypeAny, {
            custom?: Record<string, number> | undefined;
            inputTokens?: number | undefined;
            outputTokens?: number | undefined;
            totalTokens?: number | undefined;
            inputCharacters?: number | undefined;
            outputCharacters?: number | undefined;
            inputImages?: number | undefined;
            outputImages?: number | undefined;
            inputVideos?: number | undefined;
            outputVideos?: number | undefined;
            inputAudioFiles?: number | undefined;
            outputAudioFiles?: number | undefined;
            thoughtsTokens?: number | undefined;
            cachedContentTokens?: number | undefined;
        }, {
            custom?: Record<string, number> | undefined;
            inputTokens?: number | undefined;
            outputTokens?: number | undefined;
            totalTokens?: number | undefined;
            inputCharacters?: number | undefined;
            outputCharacters?: number | undefined;
            inputImages?: number | undefined;
            outputImages?: number | undefined;
            inputVideos?: number | undefined;
            outputVideos?: number | undefined;
            inputAudioFiles?: number | undefined;
            outputAudioFiles?: number | undefined;
            thoughtsTokens?: number | undefined;
            cachedContentTokens?: number | undefined;
        }>>;
        finishReason: z.ZodEnum<["stop", "length", "blocked", "interrupted", "other", "unknown"]>;
        finishMessage: z.ZodOptional<z.ZodString>;
        custom: z.ZodUnknown;
    }, "strip", z.ZodTypeAny, {
        message: {
            role: "model" | "system" | "user" | "tool";
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
            metadata?: Record<string, unknown> | undefined;
        };
        finishReason: "length" | "unknown" | "stop" | "blocked" | "interrupted" | "other";
        index: number;
        custom?: unknown;
        finishMessage?: string | undefined;
        usage?: {
            custom?: Record<string, number> | undefined;
            inputTokens?: number | undefined;
            outputTokens?: number | undefined;
            totalTokens?: number | undefined;
            inputCharacters?: number | undefined;
            outputCharacters?: number | undefined;
            inputImages?: number | undefined;
            outputImages?: number | undefined;
            inputVideos?: number | undefined;
            outputVideos?: number | undefined;
            inputAudioFiles?: number | undefined;
            outputAudioFiles?: number | undefined;
            thoughtsTokens?: number | undefined;
            cachedContentTokens?: number | undefined;
        } | undefined;
    }, {
        message: {
            role: "model" | "system" | "user" | "tool";
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
            metadata?: Record<string, unknown> | undefined;
        };
        finishReason: "length" | "unknown" | "stop" | "blocked" | "interrupted" | "other";
        index: number;
        custom?: unknown;
        finishMessage?: string | undefined;
        usage?: {
            custom?: Record<string, number> | undefined;
            inputTokens?: number | undefined;
            outputTokens?: number | undefined;
            totalTokens?: number | undefined;
            inputCharacters?: number | undefined;
            outputCharacters?: number | undefined;
            inputImages?: number | undefined;
            outputImages?: number | undefined;
            inputVideos?: number | undefined;
            outputVideos?: number | undefined;
            inputAudioFiles?: number | undefined;
            outputAudioFiles?: number | undefined;
            thoughtsTokens?: number | undefined;
            cachedContentTokens?: number | undefined;
        } | undefined;
    }>, "many">>;
    finishReason: z.ZodOptional<z.ZodEnum<["stop", "length", "blocked", "interrupted", "other", "unknown"]>>;
}, "strip", z.ZodTypeAny, {
    message?: {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    } | undefined;
    custom?: unknown;
    candidates?: {
        message: {
            role: "model" | "system" | "user" | "tool";
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
            metadata?: Record<string, unknown> | undefined;
        };
        finishReason: "length" | "unknown" | "stop" | "blocked" | "interrupted" | "other";
        index: number;
        custom?: unknown;
        finishMessage?: string | undefined;
        usage?: {
            custom?: Record<string, number> | undefined;
            inputTokens?: number | undefined;
            outputTokens?: number | undefined;
            totalTokens?: number | undefined;
            inputCharacters?: number | undefined;
            outputCharacters?: number | undefined;
            inputImages?: number | undefined;
            outputImages?: number | undefined;
            inputVideos?: number | undefined;
            outputVideos?: number | undefined;
            inputAudioFiles?: number | undefined;
            outputAudioFiles?: number | undefined;
            thoughtsTokens?: number | undefined;
            cachedContentTokens?: number | undefined;
        } | undefined;
    }[] | undefined;
    finishReason?: "length" | "unknown" | "stop" | "blocked" | "interrupted" | "other" | undefined;
    finishMessage?: string | undefined;
    latencyMs?: number | undefined;
    usage?: {
        custom?: Record<string, number> | undefined;
        inputTokens?: number | undefined;
        outputTokens?: number | undefined;
        totalTokens?: number | undefined;
        inputCharacters?: number | undefined;
        outputCharacters?: number | undefined;
        inputImages?: number | undefined;
        outputImages?: number | undefined;
        inputVideos?: number | undefined;
        outputVideos?: number | undefined;
        inputAudioFiles?: number | undefined;
        outputAudioFiles?: number | undefined;
        thoughtsTokens?: number | undefined;
        cachedContentTokens?: number | undefined;
    } | undefined;
    raw?: unknown;
    request?: {
        messages: {
            role: "model" | "system" | "user" | "tool";
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
            metadata?: Record<string, unknown> | undefined;
        }[];
        docs?: {
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
        }[] | undefined;
        tools?: {
            name: string;
            description: string;
            metadata?: Record<string, any> | undefined;
            inputSchema?: Record<string, any> | null | undefined;
            outputSchema?: Record<string, any> | null | undefined;
        }[] | undefined;
        toolChoice?: "auto" | "required" | "none" | undefined;
        config?: any;
        output?: {
            contentType?: string | undefined;
            format?: string | undefined;
            schema?: Record<string, any> | undefined;
            constrained?: boolean | undefined;
        } | undefined;
        candidates?: number | undefined;
    } | undefined;
    operation?: {
        id: string;
        error?: z.objectOutputType<{
            message: z.ZodString;
        }, z.ZodTypeAny, "passthrough"> | undefined;
        output?: any;
        metadata?: Record<string, any> | undefined;
        action?: string | undefined; /** At which stage of development this model is.
         * - `featured` models are recommended for general use.
         * - `stable` models are well-tested and reliable.
         * - `unstable` models are experimental and may change.
         * - `legacy` models are no longer recommended for new projects.
         * - `deprecated` models are deprecated by the provider and may be removed in future versions.
         */
        done?: boolean | undefined;
    } | undefined;
}, {
    message?: {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    } | undefined;
    custom?: unknown;
    candidates?: {
        message: {
            role: "model" | "system" | "user" | "tool";
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
            metadata?: Record<string, unknown> | undefined;
        };
        finishReason: "length" | "unknown" | "stop" | "blocked" | "interrupted" | "other";
        index: number;
        custom?: unknown;
        finishMessage?: string | undefined;
        usage?: {
            custom?: Record<string, number> | undefined;
            inputTokens?: number | undefined;
            outputTokens?: number | undefined;
            totalTokens?: number | undefined;
            inputCharacters?: number | undefined;
            outputCharacters?: number | undefined;
            inputImages?: number | undefined;
            outputImages?: number | undefined;
            inputVideos?: number | undefined;
            outputVideos?: number | undefined;
            inputAudioFiles?: number | undefined;
            outputAudioFiles?: number | undefined;
            thoughtsTokens?: number | undefined;
            cachedContentTokens?: number | undefined;
        } | undefined;
    }[] | undefined;
    finishReason?: "length" | "unknown" | "stop" | "blocked" | "interrupted" | "other" | undefined;
    finishMessage?: string | undefined;
    latencyMs?: number | undefined;
    usage?: {
        custom?: Record<string, number> | undefined;
        inputTokens?: number | undefined;
        outputTokens?: number | undefined;
        totalTokens?: number | undefined;
        inputCharacters?: number | undefined;
        outputCharacters?: number | undefined;
        inputImages?: number | undefined;
        outputImages?: number | undefined;
        inputVideos?: number | undefined;
        outputVideos?: number | undefined;
        inputAudioFiles?: number | undefined;
        outputAudioFiles?: number | undefined;
        thoughtsTokens?: number | undefined;
        cachedContentTokens?: number | undefined;
    } | undefined;
    raw?: unknown;
    request?: {
        messages: {
            role: "model" | "system" | "user" | "tool";
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
            metadata?: Record<string, unknown> | undefined;
        }[];
        docs?: {
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
        }[] | undefined;
        tools?: {
            name: string;
            description: string;
            metadata?: Record<string, any> | undefined;
            inputSchema?: Record<string, any> | null | undefined;
            outputSchema?: Record<string, any> | null | undefined;
        }[] | undefined;
        toolChoice?: "auto" | "required" | "none" | undefined;
        config?: any;
        output?: {
            contentType?: string | undefined;
            format?: string | undefined;
            schema?: Record<string, any> | undefined;
            constrained?: boolean | undefined;
        } | undefined;
        candidates?: number | undefined;
    } | undefined;
    operation?: {
        id: string;
        error?: z.objectInputType<{
            message: z.ZodString;
        }, z.ZodTypeAny, "passthrough"> | undefined;
        output?: any;
        metadata?: Record<string, any> | undefined;
        action?: string | undefined;
        done?: boolean | undefined;
    } | undefined;
}>;
/**
 * Generate response data.
 */
type GenerateResponseData = z.infer<typeof GenerateResponseSchema>;
/** ModelResponseChunkSchema represents a chunk of content to stream to the client. */
declare const ModelResponseChunkSchema: z.ZodObject<{
    role: z.ZodOptional<z.ZodEnum<["system", "user", "model", "tool"]>>;
    /** index of the message this chunk belongs to. */
    index: z.ZodOptional<z.ZodNumber>;
    /** The chunk of content to stream right now. */
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
    /** Model-specific extra information attached to this chunk. */
    custom: z.ZodOptional<z.ZodUnknown>;
    /** If true, the chunk includes all data from previous chunks. Otherwise, considered to be incremental. */
    aggregated: z.ZodOptional<z.ZodBoolean>;
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
    role?: "model" | "system" | "user" | "tool" | undefined;
    custom?: unknown;
    index?: number | undefined;
    aggregated?: boolean | undefined;
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
    role?: "model" | "system" | "user" | "tool" | undefined;
    custom?: unknown;
    index?: number | undefined;
    aggregated?: boolean | undefined;
}>;
type ModelResponseChunkData = z.infer<typeof ModelResponseChunkSchema>;
declare const GenerateResponseChunkSchema: z.ZodObject<{
    role: z.ZodOptional<z.ZodEnum<["system", "user", "model", "tool"]>>;
    /** index of the message this chunk belongs to. */
    index: z.ZodOptional<z.ZodNumber>;
    /** The chunk of content to stream right now. */
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
    /** Model-specific extra information attached to this chunk. */
    custom: z.ZodOptional<z.ZodUnknown>;
    /** If true, the chunk includes all data from previous chunks. Otherwise, considered to be incremental. */
    aggregated: z.ZodOptional<z.ZodBoolean>;
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
    role?: "model" | "system" | "user" | "tool" | undefined;
    custom?: unknown;
    index?: number | undefined;
    aggregated?: boolean | undefined;
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
    role?: "model" | "system" | "user" | "tool" | undefined;
    custom?: unknown;
    index?: number | undefined;
    aggregated?: boolean | undefined;
}>;
type GenerateResponseChunkData = z.infer<typeof GenerateResponseChunkSchema>;
declare const GenerateActionOutputConfig: z.ZodObject<{
    format: z.ZodOptional<z.ZodString>;
    contentType: z.ZodOptional<z.ZodString>;
    instructions: z.ZodOptional<z.ZodUnion<[z.ZodBoolean, z.ZodString]>>;
    jsonSchema: z.ZodOptional<z.ZodAny>;
    constrained: z.ZodOptional<z.ZodBoolean>;
}, "strip", z.ZodTypeAny, {
    contentType?: string | undefined;
    format?: string | undefined;
    constrained?: boolean | undefined;
    instructions?: string | boolean | undefined;
    jsonSchema?: any;
}, {
    contentType?: string | undefined;
    format?: string | undefined;
    constrained?: boolean | undefined;
    instructions?: string | boolean | undefined;
    jsonSchema?: any;
}>;
declare const GenerateActionOptionsSchema: z.ZodObject<{
    /** A model name (e.g. `vertexai/gemini-1.0-pro`). */
    model: z.ZodString;
    /** Retrieved documents to be used as context for this generation. */
    docs: z.ZodOptional<z.ZodArray<z.ZodObject<{
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
    }>, "many">>;
    /** Conversation history for multi-turn prompting when supported by the underlying model. */
    messages: z.ZodArray<z.ZodObject<{
        role: z.ZodEnum<["system", "user", "model", "tool"]>;
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
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodUnknown>>;
    }, "strip", z.ZodTypeAny, {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    }, {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    }>, "many">;
    /** List of registered tool names for this generation if supported by the underlying model. */
    tools: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    /** List of registered resource names for this generation if supported by the underlying model. */
    resources: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    /** Tool calling mode. `auto` lets the model decide whether to use tools, `required` forces the model to choose a tool, and `none` forces the model not to use any tools. Defaults to `auto`.  */
    toolChoice: z.ZodOptional<z.ZodEnum<["auto", "required", "none"]>>;
    /** Configuration for the generation request. */
    config: z.ZodOptional<z.ZodAny>;
    /** Configuration for the desired output of the request. Defaults to the model's default output if unspecified. */
    output: z.ZodOptional<z.ZodObject<{
        format: z.ZodOptional<z.ZodString>;
        contentType: z.ZodOptional<z.ZodString>;
        instructions: z.ZodOptional<z.ZodUnion<[z.ZodBoolean, z.ZodString]>>;
        jsonSchema: z.ZodOptional<z.ZodAny>;
        constrained: z.ZodOptional<z.ZodBoolean>;
    }, "strip", z.ZodTypeAny, {
        contentType?: string | undefined;
        format?: string | undefined;
        constrained?: boolean | undefined;
        instructions?: string | boolean | undefined;
        jsonSchema?: any;
    }, {
        contentType?: string | undefined;
        format?: string | undefined;
        constrained?: boolean | undefined;
        instructions?: string | boolean | undefined;
        jsonSchema?: any;
    }>>;
    /** Options for resuming an interrupted generation. */
    resume: z.ZodOptional<z.ZodObject<{
        respond: z.ZodOptional<z.ZodArray<z.ZodObject<{
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
        }>, "many">>;
        restart: z.ZodOptional<z.ZodArray<z.ZodObject<{
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
        }>, "many">>;
        metadata: z.ZodOptional<z.ZodRecord<z.ZodString, z.ZodAny>>;
    }, "strip", z.ZodTypeAny, {
        metadata?: Record<string, any> | undefined;
        respond?: {
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
        }[] | undefined;
        restart?: {
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
        }[] | undefined;
    }, {
        metadata?: Record<string, any> | undefined;
        respond?: {
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
        }[] | undefined;
        restart?: {
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
        }[] | undefined;
    }>>;
    /** When true, return tool calls for manual processing instead of automatically resolving them. */
    returnToolRequests: z.ZodOptional<z.ZodBoolean>;
    /** Maximum number of tool call iterations that can be performed in a single generate call (default 5). */
    maxTurns: z.ZodOptional<z.ZodNumber>;
    /** Custom step name for this generate call to display in trace views. Defaults to "generate". */
    stepName: z.ZodOptional<z.ZodString>;
}, "strip", z.ZodTypeAny, {
    model: string;
    messages: {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    }[];
    docs?: {
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
    }[] | undefined;
    tools?: string[] | undefined;
    resources?: string[] | undefined;
    toolChoice?: "auto" | "required" | "none" | undefined;
    config?: any;
    output?: {
        contentType?: string | undefined;
        format?: string | undefined;
        constrained?: boolean | undefined;
        instructions?: string | boolean | undefined;
        jsonSchema?: any;
    } | undefined;
    resume?: {
        metadata?: Record<string, any> | undefined;
        respond?: {
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
        }[] | undefined;
        restart?: {
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
        }[] | undefined;
    } | undefined;
    returnToolRequests?: boolean | undefined;
    maxTurns?: number | undefined;
    stepName?: string | undefined;
}, {
    model: string;
    messages: {
        role: "model" | "system" | "user" | "tool";
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
        metadata?: Record<string, unknown> | undefined;
    }[];
    docs?: {
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
    }[] | undefined;
    tools?: string[] | undefined;
    resources?: string[] | undefined;
    toolChoice?: "auto" | "required" | "none" | undefined;
    config?: any;
    output?: {
        contentType?: string | undefined;
        format?: string | undefined;
        constrained?: boolean | undefined;
        instructions?: string | boolean | undefined;
        jsonSchema?: any;
    } | undefined;
    resume?: {
        metadata?: Record<string, any> | undefined;
        respond?: {
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
        }[] | undefined;
        restart?: {
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
        }[] | undefined;
    } | undefined;
    returnToolRequests?: boolean | undefined;
    maxTurns?: number | undefined;
    stepName?: string | undefined;
}>;
type GenerateActionOptions = z.infer<typeof GenerateActionOptionsSchema>;

export { type CandidateData, type CandidateError, CandidateErrorSchema, CandidateSchema, FinishReasonSchema, type GenerateActionOptions, GenerateActionOptionsSchema, GenerateActionOutputConfig, type GenerateRequest, type GenerateRequestData, GenerateRequestSchema, type GenerateResponseChunkData, GenerateResponseChunkSchema, type GenerateResponseData, GenerateResponseSchema, type GenerationCommonConfig, GenerationCommonConfigDescriptions, GenerationCommonConfigSchema, type GenerationUsage, GenerationUsageSchema, type MessageData, MessageSchema, type ModelInfo, ModelInfoSchema, type ModelRequest, ModelRequestSchema, type ModelResponseChunkData, ModelResponseChunkSchema, type ModelResponseData, ModelResponseSchema, type OutputConfig, OutputConfigSchema, type Part, PartSchema, type Role, RoleSchema, type ToolDefinition, ToolDefinitionSchema };
