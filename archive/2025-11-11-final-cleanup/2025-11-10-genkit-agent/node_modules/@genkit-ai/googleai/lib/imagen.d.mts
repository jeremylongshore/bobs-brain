import { z, Genkit } from 'genkit';
import { ModelAction } from 'genkit/model';

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

type KNOWN_IMAGEN_MODELS = 'imagen-3.0-generate-002';
/**
 * See https://ai.google.dev/gemini-api/docs/image-generation#imagen-model
 */
declare const ImagenConfigSchema: z.ZodObject<{
    numberOfImages: z.ZodOptional<z.ZodNumber>;
    aspectRatio: z.ZodOptional<z.ZodEnum<["1:1", "9:16", "16:9", "3:4", "4:3"]>>;
    personGeneration: z.ZodOptional<z.ZodEnum<["dont_allow", "allow_adult", "allow_all"]>>;
}, "passthrough", z.ZodTypeAny, z.objectOutputType<{
    numberOfImages: z.ZodOptional<z.ZodNumber>;
    aspectRatio: z.ZodOptional<z.ZodEnum<["1:1", "9:16", "16:9", "3:4", "4:3"]>>;
    personGeneration: z.ZodOptional<z.ZodEnum<["dont_allow", "allow_adult", "allow_all"]>>;
}, z.ZodTypeAny, "passthrough">, z.objectInputType<{
    numberOfImages: z.ZodOptional<z.ZodNumber>;
    aspectRatio: z.ZodOptional<z.ZodEnum<["1:1", "9:16", "16:9", "3:4", "4:3"]>>;
    personGeneration: z.ZodOptional<z.ZodEnum<["dont_allow", "allow_adult", "allow_all"]>>;
}, z.ZodTypeAny, "passthrough">>;
declare const GENERIC_IMAGEN_INFO: {
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
declare function defineImagenModel(ai: Genkit, name: string, apiKey?: string | false): ModelAction;

export { GENERIC_IMAGEN_INFO, ImagenConfigSchema, type KNOWN_IMAGEN_MODELS, defineImagenModel };
