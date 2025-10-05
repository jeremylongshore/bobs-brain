#!/usr/bin/env python3
"""
Complete Vertex AI Integration for Graphiti
Replaces OpenAI with Google's Vertex AI
"""

from graphiti_core import Graphiti
from graphiti_core.llm_client import LLMClient
from graphiti_core.embedder import EmbedderClient
import vertexai
from vertexai.language_models import TextEmbeddingModel
from vertexai.generative_models import GenerativeModel
import asyncio
import json

class VertexAILLM(LLMClient):
    """Custom LLM client for Vertex AI Gemini"""
    
    def __init__(self):
        vertexai.init(project='bobs-house-ai', location='us-central1')
        self.model = GenerativeModel('gemini-1.5-flash')
    
    async def generate_response(self, messages, **kwargs):
        """Generate response compatible with Graphiti"""
        # Convert OpenAI-style messages to Gemini prompt
        prompt = "\n".join([m.get('content', '') for m in messages])
        response = self.model.generate_content(prompt)
        return {"content": response.text}
    
    async def extract_entities(self, text):
        """Extract entities from text using Gemini"""
        prompt = f"""
        Extract all entities (people, places, products, concepts) from this text.
        Return as JSON array.
        
        Text: {text}
        
        Entities JSON:
        """
        response = self.model.generate_content(prompt)
        return json.loads(response.text)

class VertexAIEmbedder(EmbedderClient):
    """Custom embedder using Vertex AI"""
    
    def __init__(self):
        vertexai.init(project='bobs-house-ai', location='us-central1')
        self.model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    
    async def create_embedding(self, text):
        """Create embeddings for Neo4j vector storage"""
        embeddings = self.model.get_embeddings([text])
        return embeddings[0].values  # Returns 768-dim vector

class BobWithFullVertexAI:
    """Bob's Brain fully powered by Vertex AI"""
    
    def __init__(self):
        # Initialize Graphiti with Vertex AI instead of OpenAI
        self.graphiti = Graphiti(
            uri="bolt://10.128.0.2:7687",
            user="neo4j",
            password="<REDACTED_NEO4J_PASSWORD>",
            llm_client=VertexAILLM(),        # Vertex for LLM
            embedder=VertexAIEmbedder()       # Vertex for embeddings
        )
        
        # Direct Gemini model for responses
        self.gemini = GenerativeModel('gemini-1.5-flash')
    
    async def process_conversation(self, user_message):
        """Complete pipeline with Vertex AI"""
        
        # 1. Extract entities using Vertex AI
        entities = await self.graphiti.llm_client.extract_entities(user_message)
        print(f"Extracted entities: {entities}")
        
        # 2. Create embeddings with Vertex AI
        embedding = await self.graphiti.embedder.create_embedding(user_message)
        print(f"Created {len(embedding)}-dim embedding")
        
        # 3. Search knowledge graph (uses Vertex embeddings)
        context = await self.graphiti.search(
            query=user_message,
            num_results=5
        )
        
        # 4. Generate response with Gemini
        prompt = f"""
        You are Bob, an AI assistant with access to a knowledge graph.
        
        Context from memory:
        {context}
        
        User: {user_message}
        Bob:
        """
        
        response = self.gemini.generate_content(prompt)
        
        # 5. Store in knowledge graph
        await self.graphiti.add_episode(
            name=f"conversation_{datetime.now().isoformat()}",
            episode_body=f"User: {user_message}\nBob: {response.text}",
            source_description="Slack conversation",
            reference_time=datetime.now()
        )
        
        return response.text

# Usage example
async def demo():
    bob = BobWithFullVertexAI()
    
    # Test the full pipeline
    response = await bob.process_conversation(
        "What do you know about Jeremy and DiagnosticPro?"
    )
    print(f"Bob's response: {response}")

if __name__ == "__main__":
    asyncio.run(demo())