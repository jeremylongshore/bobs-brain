import { genkit, z } from '@genkit-ai/core';
import { vertexAI, gemini20Flash } from '@genkit-ai/vertexai';
import * as admin from 'firebase-admin';

// Initialize Firebase Admin
admin.initializeApp({
  projectId: 'bobs-brain',
});

// Initialize Genkit with Vertex AI
const ai = genkit({
  plugins: [
    vertexAI({
      projectId: 'bobs-brain',
      location: 'us-central1',
    }),
  ],
});

// Define Bob's main agent flow
export const bobAgent = ai.defineFlow(
  {
    name: 'bobAgent',
    inputSchema: z.object({
      query: z.string(),
      userId: z.string().optional(),
      context: z.record(z.any()).optional(),
    }),
    outputSchema: z.object({
      response: z.string(),
      metadata: z.record(z.any()).optional(),
    }),
  },
  async (input) => {
    const { query, userId, context } = input;

    // Generate response using Vertex AI Gemini 2.0 Flash (free tier)
    const response = await ai.generate({
      model: gemini20Flash,
      prompt: query,
      config: {
        temperature: 0.7,
        maxOutputTokens: 8192, // Gemini 2.0 Flash supports up to 8K tokens
      },
    });

    return {
      response: response.text,
      metadata: {
        model: 'gemini-2.0-flash',
        timestamp: new Date().toISOString(),
        userId,
      },
    };
  }
);

// Start the Genkit dev server
ai.startFlowServer({
  port: 3400,
});
