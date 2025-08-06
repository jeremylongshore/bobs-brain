#!/usr/bin/env python3
"""
Bob's Brain - ReAct Reasoning with Open Source Components ONLY
Using: LangChain ReAct Agent + Ollama + ChromaDB + Existing Tools
NO CUSTOM REASONING CODE - ALL OPEN SOURCE
"""

import sqlite3
import asyncio
from pathlib import Path
from datetime import datetime
from typing import List
import logging

# LangChain Open Source ReAct Components
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BobReActOpenSource:
    """Bob using ONLY Open Source ReAct Components"""

    def __init__(self):
        self.home_dir = Path.home() / ".bob_brain"
        self.db_path = self.home_dir / "bob_memory.db"

        # Create directories
        self.home_dir.mkdir(exist_ok=True)
        (self.home_dir / "chroma").mkdir(exist_ok=True)

        # Setup database
        self._setup_database()

        # Initialize Open Source LLM (Ollama) with timeout
        self.llm = Ollama(model="mistral:7b", temperature=0.1, timeout=30)

        # Initialize Open Source Embeddings (Ollama)
        self.embeddings = OllamaEmbeddings(model="mistral:7b")

        # Initialize Open Source Vector Store (ChromaDB)
        self.vectorstore = Chroma(
            persist_directory=str(self.home_dir / "chroma"),
            embedding_function=self.embeddings,
            collection_name="bob_knowledge",
        )

        # Initialize Open Source Memory (LangChain)
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

        # Setup Open Source Tools
        self.tools = self._create_opensource_tools()

        # Create Open Source ReAct Agent
        self.agent_executor = self._create_react_agent()

        logger.info("🔗 Bob ReAct - Open Source Components Ready!")

    def _setup_database(self):
        """Setup SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    message TEXT,
                    response TEXT,
                    reasoning_steps TEXT
                )
            """
            )

    def _create_opensource_tools(self) -> List[Tool]:
        """Create tools using Open Source components"""
        return [
            Tool(
                name="Knowledge_Search",
                description="Search the knowledge base for relevant information",
                func=self._knowledge_search_tool,
            ),
            Tool(
                name="Web_Scrape",
                description="Scrape content from a website URL",
                func=self._web_scrape_tool,
            ),
            Tool(
                name="System_Status",
                description="Get current system and project status",
                func=self._system_status_tool,
            ),
            Tool(
                name="Remember_Info",
                description="Store important information in the knowledge base",
                func=self._remember_info_tool,
            ),
        ]

    def _knowledge_search_tool(self, query: str) -> str:
        """Open Source knowledge search using ChromaDB"""
        try:
            docs = self.vectorstore.similarity_search(query, k=3)
            if docs:
                results = []
                for i, doc in enumerate(docs, 1):
                    results.append(f"{i}. {doc.page_content[:200]}...")
                return f"Found {len(docs)} relevant items:\n" + "\n".join(results)
            else:
                return "No relevant information found in knowledge base."
        except Exception as e:
            return f"Knowledge search failed: {str(e)}"

    def _web_scrape_tool(self, url: str) -> str:
        """Open Source web scraping"""
        try:
            import requests
            from bs4 import BeautifulSoup

            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            text = soup.get_text()

            # Clean and limit text
            lines = (line.strip() for line in text.splitlines())
            clean_text = "\n".join(line for line in lines if line)

            if len(clean_text) > 1000:
                clean_text = clean_text[:1000] + "..."

            return f"Scraped content from {url}:\n{clean_text}"

        except Exception as e:
            return f"Web scraping failed: {str(e)}"

    def _system_status_tool(self, query: str) -> str:
        """Get system status"""
        try:
            import psutil

            memory = psutil.virtual_memory()

            status = f"""System Status:
- Available RAM: {memory.available / (1024**3):.1f}GB
- Memory Usage: {memory.percent:.1f}%
- Knowledge Items: {self.vectorstore._collection.count()}
- Projects: DiagnosticPro (90% complete), Bob's Brain (ReAct enabled)
"""
            return status
        except Exception as e:
            return f"System status unavailable: {str(e)}"

    def _remember_info_tool(self, info: str) -> str:
        """Store information using Open Source vector store"""
        try:
            # Add to ChromaDB vector store
            self.vectorstore.add_texts([info])

            # Also store in SQLite
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO conversations (timestamp, message, response)
                    VALUES (?, ?, ?)
                """,
                    (datetime.now().isoformat(), "remember_info", info),
                )

            return "Information stored successfully in knowledge base."
        except Exception as e:
            return f"Failed to store information: {str(e)}"

    def _create_react_agent(self) -> AgentExecutor:
        """Create Open Source ReAct Agent using LangChain"""

        # Open Source ReAct Prompt Template
        react_prompt = PromptTemplate.from_template(
            """
You are Bob, Jeremy's AI assistant with access to tools and reasoning capabilities.

You have access to the following tools:
{tools}

Use the following format for reasoning:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
"""
        )

        # Create Open Source ReAct Agent
        agent = create_react_agent(llm=self.llm, tools=self.tools, prompt=react_prompt)

        # Create Agent Executor with optimized settings
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=3,
            max_execution_time=45,
            early_stopping_method="generate",
        )

    async def chat(self, message: str) -> str:
        """Chat using Open Source ReAct Agent"""
        try:
            # Use LangChain ReAct Agent - OPEN SOURCE REASONING
            response = self.agent_executor.invoke(
                {"input": message, "chat_history": self.memory.chat_memory.messages}
            )

            # Store conversation
            self._store_conversation(message, response["output"])

            return response["output"]

        except Exception as e:
            logger.error(f"ReAct agent error: {e}")
            return f"❌ ReAct reasoning failed: {str(e)}"

    def _store_conversation(self, message: str, response: str):
        """Store conversation in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO conversations
                    (timestamp, message, response, reasoning_steps)
                    VALUES (?, ?, ?, ?)
                """,
                    (
                        datetime.now().isoformat(),
                        message,
                        response,
                        "langchain_react_agent",
                    ),
                )
        except Exception as e:
            logger.error(f"Failed to store conversation: {e}")

    def get_status(self) -> str:
        """Get Bob's Open Source ReAct status"""
        try:
            knowledge_count = self.vectorstore._collection.count()
        except Exception:
            knowledge_count = "Unknown"

        status = f"""
🔗 Bob ReAct - Open Source Components Status:

🧠 Open Source LLM: Ollama Mistral 7B
🗄️ Open Source Vector DB: ChromaDB ({knowledge_count} items)
🔗 Open Source Agent: LangChain ReAct Agent
🧰 Open Source Tools: 4 available
💾 Database: SQLite

🎯 ReAct Reasoning: ✅ ACTIVE
- Thought → Action → Observation → Repeat
- Multi-step problem solving
- Tool integration and reasoning
- Memory and context retention

🚀 Bob is now using professional Open Source ReAct reasoning!
        """.strip()

        return status


async def main():
    """Main Open Source ReAct interface"""
    print("🔗 Bob's Brain - Open Source ReAct Reasoning")
    print("Using: LangChain + Ollama + ChromaDB + ReAct Agent")
    print("Type 'exit' to quit, 'status' for capabilities\n")

    try:
        bob = BobReActOpenSource()
        print(bob.get_status())

        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("👋 Bob ReAct: Reasoning complete!")
                    break

                if user_input.lower() == "status":
                    print(bob.get_status())
                    continue

                if user_input:
                    print("\n🤔 Bob is reasoning...")
                    response = await bob.chat(user_input)
                    print(f"\n🤖 Bob: {response}")

            except KeyboardInterrupt:
                print("\n👋 Bob ReAct: Shutting down reasoning!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    except Exception as e:
        print(f"❌ Failed to initialize Bob ReAct: {e}")
        print("Make sure Ollama is running with mistral:7b model")


if __name__ == "__main__":
    asyncio.run(main())
