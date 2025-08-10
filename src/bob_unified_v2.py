#!/usr/bin/env python3
"""
Bob's Brain - Unified Slack Bot with ChromaDB Integration
Version 2.0 - Consolidated Edition
"""

import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Slack SDK
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

# ChromaDB for vector storage
import chromadb
from chromadb.config import Settings

# Vertex AI for chat
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

# Environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Slack app
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Initialize Vertex AI
project_id = os.environ.get("GCP_PROJECT", "bobs-house-ai")
location = os.environ.get("GCP_LOCATION", "us-central1")
vertexai.init(project=project_id, location=location)

# Initialize Gemini model
model = GenerativeModel("gemini-2.0-flash-exp")

# Initialize ChromaDB - Use Bob's Brain directory
CHROMA_PERSIST_DIR = os.environ.get("CHROMA_PERSIST_DIR", "/home/jeremylongshore/bobs_brain/data/vector_store")
chroma_client = chromadb.PersistentClient(
    path=CHROMA_PERSIST_DIR,
    settings=Settings(anonymized_telemetry=False)
)

# Get or create collection
try:
    collection = chroma_client.get_collection("bob_knowledge")
    logger.info(f"Loaded existing collection with {collection.count()} documents")
except:
    collection = chroma_client.create_collection(
        name="bob_knowledge",
        metadata={"description": "Bob's knowledge base"}
    )
    logger.info("Created new collection")

class KnowledgeLoader:
    """Load and index knowledge from various sources"""
    
    def __init__(self, collection):
        self.collection = collection
        self.doc_count = 0
    
    def load_file(self, filepath: str, metadata: Optional[Dict] = None):
        """Load a single file into the knowledge base"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Create metadata
            doc_metadata = {
                'source': filepath,
                'type': 'file',
                'loaded_at': datetime.now().isoformat()
            }
            if metadata:
                doc_metadata.update(metadata)
            
            # Add to collection
            doc_id = f"doc_{self.doc_count}"
            self.collection.add(
                documents=[content],
                metadatas=[doc_metadata],
                ids=[doc_id]
            )
            
            self.doc_count += 1
            logger.info(f"Loaded {filepath} as {doc_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load {filepath}: {e}")
            return False
    
    def load_directory(self, dirpath: str, extensions: List[str] = None):
        """Load all files from a directory"""
        if extensions is None:
            extensions = ['.txt', '.md', '.py', '.js', '.json', '.yaml', '.yml']
        
        loaded = 0
        for root, dirs, files in os.walk(dirpath):
            # Skip hidden directories and node_modules
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
            
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    filepath = os.path.join(root, file)
                    if self.load_file(filepath):
                        loaded += 1
        
        logger.info(f"Loaded {loaded} files from {dirpath}")
        return loaded

class BobBrain:
    """Bob's cognitive functions"""
    
    def __init__(self, collection):
        self.collection = collection
        self.conversation_history = {}
    
    def search_knowledge(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search knowledge base for relevant information"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            if results and results['documents']:
                return [
                    {
                        'content': doc,
                        'metadata': meta,
                        'distance': dist
                    }
                    for doc, meta, dist in zip(
                        results['documents'][0],
                        results['metadatas'][0],
                        results['distances'][0]
                    )
                ]
            return []
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    def generate_response(self, user_message: str, channel: str, user: str) -> str:
        """Generate a response using knowledge base and conversation history"""
        
        # Search for relevant knowledge
        knowledge = self.search_knowledge(user_message, n_results=3)
        
        # Build context
        context = "Relevant knowledge:\n"
        for item in knowledge:
            source = item['metadata'].get('source', 'unknown')
            context += f"- From {source}: {item['content'][:200]}...\n"
        
        # Get conversation history
        history_key = f"{channel}_{user}"
        history = self.conversation_history.get(history_key, [])
        
        # Build messages for OpenAI
        messages = [
            {
                "role": "system",
                "content": """You are Bob, a helpful AI assistant with access to a knowledge base.
                Use the provided context to answer questions accurately.
                Be friendly, professional, and concise.
                If you don't know something, say so honestly."""
            }
        ]
        
        # Add context if we have relevant knowledge
        if knowledge:
            messages.append({
                "role": "system",
                "content": f"Context from knowledge base:\n{context}"
            })
        
        # Add conversation history (last 5 messages)
        for msg in history[-5:]:
            messages.append(msg)
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Build prompt for Vertex AI
            prompt = f"""You are Bob, a helpful AI assistant with access to a knowledge base.
            
Context from knowledge base:
{context if knowledge else "No relevant context found."}

Conversation history:
{chr(10).join([f"{msg['role']}: {msg['content']}" for msg in history[-3:]])}

User: {user_message}

Please provide a helpful, professional, and concise response. If you don't know something, say so honestly."""
            
            # Generate with Vertex AI Gemini
            response = model.generate_content(
                prompt,
                generation_config=GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=500,
                )
            )
            
            reply = response.text
            
            # Update conversation history
            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": reply})
            self.conversation_history[history_key] = history[-10:]  # Keep last 10 messages
            
            return reply
            
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return "I apologize, but I'm having trouble generating a response right now. Please try again."

# Initialize Bob's brain
bob = BobBrain(collection)
knowledge_loader = KnowledgeLoader(collection)

# Slack event handlers
@app.event("app_mention")
def handle_mention(event, say):
    """Handle when Bob is mentioned"""
    try:
        user = event['user']
        channel = event['channel']
        text = event['text']
        
        # Remove the mention from the text
        text = text.replace(f"<@{event['bot_id']}>", "").strip()
        
        logger.info(f"Mention from {user} in {channel}: {text}")
        
        # Generate response
        response = bob.generate_response(text, channel, user)
        
        # Send response
        say(response, thread_ts=event.get('thread_ts', event['ts']))
        
    except Exception as e:
        logger.error(f"Error handling mention: {e}")
        say("Sorry, I encountered an error. Please try again.")

@app.event("message")
def handle_direct_message(event, say):
    """Handle direct messages to Bob"""
    if event.get('channel_type') == 'im' and 'bot_id' not in event:
        try:
            user = event['user']
            channel = event['channel']
            text = event['text']
            
            logger.info(f"DM from {user}: {text}")
            
            # Generate response
            response = bob.generate_response(text, channel, user)
            
            # Send response
            say(response)
            
        except Exception as e:
            logger.error(f"Error handling DM: {e}")
            say("Sorry, I encountered an error. Please try again.")

@app.command("/bob-learn")
def handle_learn_command(ack, respond, command):
    """Handle the /bob-learn slash command"""
    ack()
    
    try:
        text = command['text']
        user = command['user_id']
        
        # Store the learning in the knowledge base
        doc_id = f"learned_{datetime.now().timestamp()}"
        collection.add(
            documents=[text],
            metadatas=[{
                'source': f'slack_user_{user}',
                'type': 'learned',
                'timestamp': datetime.now().isoformat()
            }],
            ids=[doc_id]
        )
        
        respond(f"Thanks! I've learned: {text[:100]}...")
        
    except Exception as e:
        logger.error(f"Error in learn command: {e}")
        respond("Sorry, I couldn't learn that. Please try again.")

@app.command("/bob-search")
def handle_search_command(ack, respond, command):
    """Handle the /bob-search slash command"""
    ack()
    
    try:
        query = command['text']
        
        # Search knowledge base
        results = bob.search_knowledge(query, n_results=3)
        
        if results:
            response = "Here's what I found:\n\n"
            for i, result in enumerate(results, 1):
                source = result['metadata'].get('source', 'unknown')
                content = result['content'][:200]
                response += f"{i}. From {source}:\n   {content}...\n\n"
        else:
            response = "I couldn't find anything related to that query."
        
        respond(response)
        
    except Exception as e:
        logger.error(f"Error in search command: {e}")
        respond("Sorry, I couldn't search right now. Please try again.")

def load_initial_knowledge():
    """Load initial knowledge base if needed"""
    if collection.count() == 0:
        logger.info("Loading initial knowledge base...")
        
        # Load from knowledge directory if it exists
        knowledge_dir = os.environ.get("KNOWLEDGE_DIR", "./knowledge")
        if os.path.exists(knowledge_dir):
            loaded = knowledge_loader.load_directory(knowledge_dir)
            logger.info(f"Loaded {loaded} documents from {knowledge_dir}")
        
        # Load from archives if they exist
        archives_dir = os.environ.get("ARCHIVES_DIR", "./archives")
        if os.path.exists(archives_dir):
            loaded = knowledge_loader.load_directory(archives_dir)
            logger.info(f"Loaded {loaded} documents from {archives_dir}")
    
    logger.info(f"Knowledge base contains {collection.count()} documents")

def main():
    """Main entry point"""
    logger.info("Starting Bob's Brain v2.0...")
    
    # Check for tokens
    if "PLACEHOLDER" in os.environ.get("SLACK_BOT_TOKEN", ""):
        logger.warning("⚠️ Bob is starting with placeholder tokens!")
        logger.warning("⚠️ Update the environment variables with real Slack tokens to enable bot functionality")
        
        # Start a simple health check server
        from http.server import HTTPServer, BaseHTTPRequestHandler
        
        class HealthHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Bob's Brain is deployed but needs real Slack tokens. Update environment variables in Cloud Run.")
            def log_message(self, format, *args):
                pass
        
        port = int(os.environ.get("PORT", 5000))
        logger.info(f"Starting placeholder server on port {port}...")
        server = HTTPServer(('0.0.0.0', port), HealthHandler)
        server.serve_forever()
        return
    
    # Load initial knowledge
    load_initial_knowledge()
    
    # Start the app
    if os.environ.get("SLACK_APP_TOKEN"):
        # Socket mode for local development
        handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
        logger.info("Starting in Socket Mode...")
        handler.start()
    else:
        # Web server mode for production
        port = int(os.environ.get("PORT", 5000))
        logger.info(f"Starting web server on port {port}...")
        app.start(port=port)

if __name__ == "__main__":
    main()