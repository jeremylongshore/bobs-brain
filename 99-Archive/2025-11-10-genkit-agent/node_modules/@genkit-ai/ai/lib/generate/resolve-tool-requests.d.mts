import { Registry } from '@genkit-ai/core/registry';
import { l as ToolRequestPart, m as ToolResponsePart } from '../document-SEV6zxye.mjs';
import { GenerateActionOptions, MessageData, GenerateResponseData } from '../model-types.mjs';
import { w as ToolAction, z as ToolRunOptions } from '../generate-B-EKqoSX.mjs';
import '@genkit-ai/core';
import './chunk.mjs';
import './response.mjs';
import '../message.mjs';
import '../model-aQReSBZ2.mjs';
import '../formats/types.mjs';
import '../resource.mjs';

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

declare function toToolMap(tools: ToolAction[]): Record<string, ToolAction>;
/** Ensures that each tool has a unique name. */
declare function assertValidToolNames(tools: ToolAction[]): void;
declare function toPendingOutput(part: ToolRequestPart, response: ToolResponsePart): ToolRequestPart;
declare function resolveToolRequest(rawRequest: GenerateActionOptions, part: ToolRequestPart, toolMap: Record<string, ToolAction>, runOptions?: ToolRunOptions): Promise<{
    response?: ToolResponsePart;
    interrupt?: ToolRequestPart;
    preamble?: GenerateActionOptions;
}>;
/**
 * resolveToolRequests is responsible for executing the tools requested by the model for a single turn. it
 * returns either a toolMessage to append or a revisedModelMessage when an interrupt occurs, and a transferPreamble
 * if a prompt tool is called
 */
declare function resolveToolRequests(registry: Registry, rawRequest: GenerateActionOptions, generatedMessage: MessageData): Promise<{
    revisedModelMessage?: MessageData;
    toolMessage?: MessageData;
    transferPreamble?: GenerateActionOptions;
}>;
/** Amends message history to handle `resume` arguments. Returns the amended history. */
declare function resolveResumeOption(registry: Registry, rawRequest: GenerateActionOptions): Promise<{
    revisedRequest?: GenerateActionOptions;
    interruptedResponse?: GenerateResponseData;
    toolMessage?: MessageData;
}>;
declare function resolveRestartedTools(registry: Registry, rawRequest: GenerateActionOptions): Promise<ToolRequestPart[]>;

export { assertValidToolNames, resolveRestartedTools, resolveResumeOption, resolveToolRequest, resolveToolRequests, toPendingOutput, toToolMap };
