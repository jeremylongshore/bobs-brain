import { z, Genkit } from 'genkit';
import { BackgroundModelAction } from 'genkit/model';

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

type KNOWN_VEO_MODELS = 'veo-2.0-generate-001';
/**
 * See https://ai.google.dev/gemini-api/docs/video
 */
declare const VeoConfigSchema: z.ZodObject<{
    negativePrompt: z.ZodOptional<z.ZodString>;
    aspectRatio: z.ZodOptional<z.ZodEnum<["9:16", "16:9"]>>;
    personGeneration: z.ZodOptional<z.ZodEnum<["dont_allow", "allow_adult", "allow_all"]>>;
    durationSeconds: z.ZodOptional<z.ZodNumber>;
    enhance_prompt: z.ZodOptional<z.ZodBoolean>;
}, "passthrough", z.ZodTypeAny, z.objectOutputType<{
    negativePrompt: z.ZodOptional<z.ZodString>;
    aspectRatio: z.ZodOptional<z.ZodEnum<["9:16", "16:9"]>>;
    personGeneration: z.ZodOptional<z.ZodEnum<["dont_allow", "allow_adult", "allow_all"]>>;
    durationSeconds: z.ZodOptional<z.ZodNumber>;
    enhance_prompt: z.ZodOptional<z.ZodBoolean>;
}, z.ZodTypeAny, "passthrough">, z.objectInputType<{
    negativePrompt: z.ZodOptional<z.ZodString>;
    aspectRatio: z.ZodOptional<z.ZodEnum<["9:16", "16:9"]>>;
    personGeneration: z.ZodOptional<z.ZodEnum<["dont_allow", "allow_adult", "allow_all"]>>;
    durationSeconds: z.ZodOptional<z.ZodNumber>;
    enhance_prompt: z.ZodOptional<z.ZodBoolean>;
}, z.ZodTypeAny, "passthrough">>;
declare const GENERIC_VEO_INFO: {
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
};
declare function defineVeoModel(ai: Genkit, name: string, apiKey?: string | false): BackgroundModelAction<typeof VeoConfigSchema>;

export { GENERIC_VEO_INFO, type KNOWN_VEO_MODELS, VeoConfigSchema, defineVeoModel };
