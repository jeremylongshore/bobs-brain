#!/usr/bin/env python3
"""
BOB BRAIN v5.0 - The Universal Assistant with Memory
This is Bob with FULL Graphiti integration, BigQuery knowledge, and learning capabilities
"""

import asyncio
import hashlib
import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from flask import Flask, jsonify, request
from google import genai
from google.cloud import bigquery, datastore
from google.genai import types
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)


class BobBrainV5:
    """Bob as Jeremy's Universal Assistant with Full Memory"""

    def __init__(self):
        """Initialize Bob with complete integration"""

        # Core configuration
        self.project_id = os.environ.get("GCP_PROJECT", "bobs-house-ai")
        self.location = os.environ.get("GCP_LOCATION", "us-central1")
        self.user_id = "jeremy"  # Track who Bob is assisting

        logger.info("=" * 60)
        logger.info("🧠 BOB BRAIN v5.0 - UNIVERSAL ASSISTANT WITH MEMORY")
        logger.info(f"📍 Project: {self.project_id}")
        logger.info("=" * 60)

        # Initialize all components
        self._init_genai()
        self._init_graphiti()
        self._init_bigquery()
        self._init_datastore()
        self._init_circle_of_life()
        self._init_slack()

        # Memory tracking
        self.conversation_context = []
        self.processed_events = set()
        self.max_events = 1000

        # Thread pool for async operations
        self.executor = ThreadPoolExecutor(max_workers=3)

        logger.info("✅ BOB BRAIN v5.0 INITIALIZATION COMPLETE!")
        logger.info("🧠 Ready to remember everything and learn from corrections")
        logger.info("=" * 60)

    def _init_genai(self):
        """Initialize Google Gen AI SDK"""
        try:
            import google.auth

            credentials, project = google.auth.default()

            self.genai_client = genai.Client(vertexai=True, project=self.project_id, location=self.location)

            # Try multiple models
            model_attempts = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-flash-002"]

            self.model_name = None
            self.model_available = False

            for model_name in model_attempts:
                try:
                    test_response = self.genai_client.models.generate_content(
                        model=model_name, contents="Say 'ready' if you work"
                    )

                    if test_response and test_response.candidates:
                        logger.info(f"✅ Google Gen AI: {model_name} initialized")
                        self.model_name = model_name
                        self.model_available = True
                        break

                except Exception as e:
                    logger.warning(f"Model {model_name} failed: {str(e)[:100]}")
                    continue

            if not self.model_available:
                logger.error("❌ No Gen AI models available")

        except Exception as e:
            logger.error(f"❌ Google Gen AI initialization failed: {e}")
            self.genai_client = None
            self.model_available = False

    def _init_graphiti(self):
        """Initialize memory system (Neo4j/Graphiti with enhanced configuration)"""
        try:
            # Import Neo4j driver
            from neo4j import GraphDatabase

            neo4j_uri = os.environ.get("NEO4J_URI", "bolt://10.128.0.2:7687")
            neo4j_user = os.environ.get("NEO4J_USER", "neo4j")
            neo4j_password = os.environ.get("NEO4J_PASSWORD", "BobBrain2025")

            # Create driver with optimized settings for VPC connection
            driver = GraphDatabase.driver(
                neo4j_uri,
                auth=(neo4j_user, neo4j_password),
                connection_timeout=10,  # Increased for VPC
                max_connection_pool_size=5,
                keep_alive=True,
                max_connection_lifetime=3600,  # 1 hour
                connection_acquisition_timeout=30,
            )

            # Test connection with retry logic
            connected = False
            for attempt in range(3):
                try:
                    with driver.session() as session:
                        result = session.run("RETURN 1 as test")
                        test_result = result.single()
                        if test_result and test_result[0] == 1:
                            logger.info(f"✅ Neo4j: Connected to {neo4j_uri} via VPC")
                            self.neo4j_driver = driver
                            self.memory_available = True
                            connected = True
                            break
                except Exception as e:
                    logger.warning(f"Neo4j connection attempt {attempt + 1} failed: {str(e)[:50]}")
                    if attempt < 2:
                        time.sleep(2)
            
            if connected:
                # Now try Graphiti with Google Gemini support
                try:
                    from graphiti_core import Graphiti
                    from graphiti_core.llm_client import LLMClient
                    from graphiti_core.embedder import Embedder
                    
                    # Configure Graphiti to use Google Gemini
                    llm_client = LLMClient(
                        model="gemini-2.5-flash",
                        provider="google-genai",
                        temperature=0.0,
                    )
                    
                    embedder = Embedder(
                        model="text-embedding-004",
                        provider="google-genai",
                    )

                    self.graphiti = Graphiti(
                        uri=neo4j_uri,
                        user=neo4j_user,
                        password=neo4j_password,
                        llm_client=llm_client,
                        embedder=embedder,
                    )
                    
                    logger.info("✅ Graphiti: Advanced memory with Gemini integration initialized")
                    self.graphiti_available = True
                    return  # Success!

                except (ImportError, Exception) as graphiti_error:
                    logger.warning(f"⚠️ Graphiti setup failed: {str(graphiti_error)[:100]}")
                    logger.info("📝 Using direct Neo4j without Graphiti abstraction")
                    self.graphiti = None
                    self.graphiti_available = False
                    return  # Still have Neo4j
            
            # If we get here, Neo4j connection failed
            if driver:
                driver.close()

        except ImportError:
            logger.warning("⚠️ Neo4j driver not available")
        except Exception as e:
            logger.warning(f"⚠️ Memory system setup failed: {str(e)[:100]}")

        # Fallback: Use in-memory storage
        logger.info("📝 Using in-memory conversation storage (no persistence)")
        self.neo4j_driver = None
        self.graphiti = None
        self.graphiti_available = False
        self.memory_available = False
        self.memory_cache = []  # Simple in-memory cache as fallback

    def _init_bigquery(self):
        """Initialize BigQuery for massive knowledge warehouse"""
        try:
            self.bq_client = bigquery.Client(project=self.project_id)

            # Create datasets if they don't exist
            datasets = ["knowledge_base", "conversations", "scraped_data"]
            for dataset_name in datasets:
                dataset_id = f"{self.project_id}.{dataset_name}"
                try:
                    self.bq_client.get_dataset(dataset_id)
                    logger.info(f"✅ BigQuery dataset exists: {dataset_name}")
                except Exception:
                    dataset = bigquery.Dataset(dataset_id)
                    dataset.location = self.location
                    self.bq_client.create_dataset(dataset, exists_ok=True)
                    logger.info(f"✅ BigQuery dataset created: {dataset_name}")

            logger.info("✅ BigQuery: Knowledge warehouse ready")

        except Exception as e:
            logger.warning(f"⚠️ BigQuery not available: {e}")
            self.bq_client = None

    def _init_datastore(self):
        """Initialize Datastore for MVP3 diagnostic data access"""
        try:
            self.datastore_client = datastore.Client(project="diagnostic-pro-mvp")

            # Test connection by attempting a simple query
            query = self.datastore_client.query(kind="diagnostic_submissions")
            query.keys_only()
            list(query.fetch(limit=1))  # Test connection

            logger.info("✅ Datastore: Connected to MVP3 diagnostic data")
            self.datastore_available = True

        except Exception as e:
            logger.warning(f"⚠️ Datastore not available: {e}")
            self.datastore_client = None
            self.datastore_available = False

    def _init_circle_of_life(self):
        """Initialize Circle of Life learning system"""
        try:
            # Try multiple import methods for compatibility
            try:
                import src.circle_of_life as col_module
            except ImportError:
                try:
                    from . import circle_of_life as col_module
                except ImportError:
                    import circle_of_life as col_module

            self.circle_of_life = col_module.get_circle_of_life()
            logger.info("🔄 Circle of Life: Learning system initialized")
            self.circle_available = True
        except Exception as e:
            logger.warning(f"⚠️ Circle of Life not available: {e}")
            self.circle_of_life = None
            self.circle_available = False

    def _init_slack(self):
        """Initialize Slack client"""
        self.slack_token = os.environ.get("SLACK_BOT_TOKEN")

        if self.slack_token:
            self.slack_client = WebClient(token=self.slack_token)
            logger.info("✅ Slack: Client initialized")
        else:
            logger.warning("⚠️ Slack: No SLACK_BOT_TOKEN found")
            self.slack_client = None

    async def remember_conversation(self, user_message, bot_response, user="jeremy"):
        """Store conversation in memory system"""
        try:
            # Try Graphiti first (best option)
            if self.graphiti_available and self.graphiti:
                try:
                    episode_content = f"User ({user}): {user_message}\nBob: {bot_response}"
                    await self.graphiti.add_episode(
                        name=f"conversation_{datetime.now().isoformat()}",
                        episode_body=episode_content,
                        source_description=f"Conversation with {user}",
                        reference_time=datetime.now(),
                    )
                    logger.info("💾 Stored conversation in Graphiti")
                except Exception as e:
                    logger.warning(f"Graphiti storage failed: {str(e)[:100]}")

            # Try direct Neo4j (good fallback)
            elif hasattr(self, "neo4j_driver") and self.neo4j_driver:
                try:
                    with self.neo4j_driver.session() as session:
                        session.run(
                            """
                            CREATE (c:Conversation {
                                user: $user,
                                message: $message,
                                response: $response,
                                timestamp: datetime(),
                                id: $id
                            })
                        """,
                            user=user,
                            message=user_message,
                            response=bot_response,
                            id=hashlib.md5(f"{user_message}{bot_response}".encode()).hexdigest(),
                        )
                    logger.info("💾 Stored conversation in Neo4j")
                except Exception as e:
                    logger.warning(f"Neo4j storage failed: {str(e)[:100]}")

            # In-memory fallback
            else:
                if not hasattr(self, "memory_cache"):
                    self.memory_cache = []

                conversation = {
                    "user": user,
                    "message": user_message,
                    "response": bot_response,
                    "timestamp": datetime.now().isoformat(),
                }

                self.memory_cache.append(conversation)
                # Keep only last 100 conversations in memory
                if len(self.memory_cache) > 100:
                    self.memory_cache = self.memory_cache[-100:]

                logger.info("💾 Stored conversation in memory cache")

            # Always try to store in BigQuery for analytics
            if self.bq_client:
                try:
                    table_id = f"{self.project_id}.conversations.history"
                    rows = [
                        {
                            "user": user,
                            "message": user_message,
                            "response": bot_response,
                            "timestamp": datetime.now().isoformat(),
                        }
                    ]

                    # Try to insert directly first
                    errors = self.bq_client.insert_rows_json(table_id, rows)
                    if not errors:
                        logger.info("💾 Stored conversation in BigQuery")
                    else:
                        logger.warning(f"BigQuery insert errors: {errors}")

                except Exception as bq_error:
                    logger.warning(f"BigQuery storage failed: {str(bq_error)[:100]}")

        except Exception as e:
            logger.error(f"Failed to remember conversation: {e}")

    async def recall_conversations(self, query, user="jeremy"):
        """Recall relevant past conversations"""
        context = []

        try:
            # Try Graphiti search first
            if self.graphiti_available and self.graphiti:
                try:
                    results = await self.graphiti.search(query=query, num_results=5)

                    for result in results:
                        if hasattr(result, "content"):
                            context.append(result.content)

                    if context:
                        logger.info(f"📚 Recalled {len(context)} conversations from Graphiti")

                except Exception as e:
                    logger.warning(f"Graphiti search failed: {str(e)[:100]}")

            # Try direct Neo4j search
            elif hasattr(self, "neo4j_driver") and self.neo4j_driver:
                try:
                    with self.neo4j_driver.session() as session:
                        result = session.run(
                            """
                            MATCH (c:Conversation)
                            WHERE c.user = $user
                            AND (toLower(c.message) CONTAINS toLower($query)
                                 OR toLower(c.response) CONTAINS toLower($query))
                            RETURN c.message as message, c.response as response, c.timestamp as timestamp
                            ORDER BY c.timestamp DESC
                            LIMIT 5
                        """,
                            user=user,
                            query=query,
                        )

                        for record in result:
                            context.append(f"Previous: {record['message']}\nBob said: {record['response']}")

                    if context:
                        logger.info(f"📚 Recalled {len(context)} conversations from Neo4j")

                except Exception as e:
                    logger.warning(f"Neo4j search failed: {str(e)[:100]}")

            # Try in-memory cache
            elif hasattr(self, "memory_cache") and self.memory_cache:
                query_lower = query.lower()
                for conv in reversed(self.memory_cache[-20:]):  # Check last 20 conversations
                    if query_lower in conv["message"].lower() or query_lower in conv["response"].lower():
                        context.append(f"Previous: {conv['message']}\nBob said: {conv['response']}")

                if context:
                    logger.info(f"📚 Recalled {len(context)} conversations from memory cache")

            # Also check BigQuery if we don't have enough context
            if self.bq_client and len(context) < 3:
                try:
                    query_sql = f"""
                    SELECT message, response, timestamp
                    FROM `{self.project_id}.conversations.history`
                    WHERE user = @user
                    AND (LOWER(message) LIKE LOWER(@pattern) OR LOWER(response) LIKE LOWER(@pattern))
                    ORDER BY timestamp DESC
                    LIMIT 3
                    """

                    job_config = bigquery.QueryJobConfig(
                        query_parameters=[
                            bigquery.ScalarQueryParameter("user", "STRING", user),
                            bigquery.ScalarQueryParameter("pattern", "STRING", f"%{query}%"),
                        ]
                    )

                    query_job = self.bq_client.query(query_sql, job_config=job_config)
                    results = query_job.result()

                    rows = list(results)  # Convert to list first
                    for row in rows:
                        context.append(f"Previous: {row.message}\nBob said: {row.response}")

                    if len(rows) > 0:
                        logger.info(f"📚 Added {len(rows)} conversations from BigQuery")

                except Exception as e:
                    logger.warning(f"BigQuery search failed: {str(e)[:100]}")

        except Exception as e:
            logger.error(f"Failed to recall conversations: {e}")

        return context[:5]  # Return max 5 relevant conversations

    async def get_recent_conversations(self, user="jeremy", limit=3):
        """Get the most recent conversations regardless of content"""
        context = []

        try:
            # Try in-memory cache first (most reliable for recent conversations)
            if hasattr(self, "memory_cache") and self.memory_cache:
                recent_convs = [conv for conv in self.memory_cache if conv["user"] == user][-limit:]
                for conv in reversed(recent_convs):  # Most recent first
                    context.append(f"Recent: {conv['message']}\nBob said: {conv['response']}")

                if context:
                    logger.info(f"📚 Retrieved {len(context)} recent conversations from memory")
                    return context

            # Try BigQuery for recent conversations
            if self.bq_client:
                try:
                    query_sql = f"""
                    SELECT message, response, timestamp
                    FROM `{self.project_id}.conversations.history`
                    WHERE user = @user
                    ORDER BY timestamp DESC
                    LIMIT @limit
                    """

                    job_config = bigquery.QueryJobConfig(
                        query_parameters=[
                            bigquery.ScalarQueryParameter("user", "STRING", user),
                            bigquery.ScalarQueryParameter("limit", "INTEGER", limit),
                        ]
                    )

                    query_job = self.bq_client.query(query_sql, job_config=job_config)
                    results = query_job.result()

                    rows = list(results)
                    for row in rows:
                        context.append(f"Recent: {row.message}\nBob said: {row.response}")

                    if rows:
                        logger.info(f"📚 Retrieved {len(rows)} recent conversations from BigQuery")

                except Exception as e:
                    logger.warning(f"BigQuery recent conversations failed: {str(e)[:100]}")

        except Exception as e:
            logger.error(f"Failed to get recent conversations: {e}")

        return context

    def query_knowledge_base(self, query):
        """Query BigQuery knowledge warehouse"""
        knowledge = []

        if not self.bq_client:
            return knowledge

        try:
            # Query repair manuals (if table exists)
            try:
                manual_query = f"""
                SELECT content, source
                FROM `{self.project_id}.knowledge_base.repair_manuals`
                WHERE LOWER(content) LIKE LOWER(@pattern)
                LIMIT 3
                """

                job_config = bigquery.QueryJobConfig(
                    query_parameters=[bigquery.ScalarQueryParameter("pattern", "STRING", f"%{query}%")]
                )

                results = self.bq_client.query(manual_query, job_config=job_config).result()

                for row in results:
                    knowledge.append(f"📖 Manual: {row.content[:200]}... (Source: {row.source})")
            except Exception:
                pass

            # Query forum posts (if table exists)
            try:
                forum_query = f"""
                SELECT question, answer, upvotes
                FROM `{self.project_id}.knowledge_base.forum_posts`
                WHERE LOWER(question) LIKE LOWER(@pattern) OR LOWER(answer) LIKE LOWER(@pattern)
                ORDER BY upvotes DESC
                LIMIT 3
                """

                job_config = bigquery.QueryJobConfig(
                    query_parameters=[bigquery.ScalarQueryParameter("pattern", "STRING", f"%{query}%")]
                )

                results = self.bq_client.query(forum_query, job_config=job_config).result()

                for row in results:
                    knowledge.append(f"💬 Forum: Q: {row.question}\nA: {row.answer} (👍 {row.upvotes})")
            except Exception:
                pass

            # Query scraped data
            try:
                scraped_query = f"""
                SELECT repair_type, AVG(quoted_price) as avg_price, COUNT(*) as num_quotes
                FROM `{self.project_id}.scraped_data.repair_quotes`
                WHERE LOWER(repair_type) LIKE LOWER(@pattern)
                GROUP BY repair_type
                LIMIT 3
                """

                job_config = bigquery.QueryJobConfig(
                    query_parameters=[bigquery.ScalarQueryParameter("pattern", "STRING", f"%{query}%")]
                )

                results = self.bq_client.query(scraped_query, job_config=job_config).result()

                for row in results:
                    knowledge.append(f"💰 {row.repair_type}: Avg ${row.avg_price:.2f} ({row.num_quotes} quotes)")
            except Exception:
                pass

        except Exception as e:
            logger.error(f"Knowledge base query error: {e}")

        return knowledge

    def query_bobcat_s740_knowledge(self, query):
        """Query Bobcat S740 specific knowledge from scraped data"""
        s740_knowledge = []
        
        if not self.bq_client:
            return s740_knowledge
        
        try:
            # Query S740 issues and solutions
            s740_query = f"""
            SELECT 
                problem_type,
                problem_description,
                solution,
                ARRAY_TO_STRING(parts_needed, ', ') as parts,
                ARRAY_TO_STRING(error_codes, ', ') as codes,
                difficulty,
                cost_estimate
            FROM `{self.project_id}.skidsteer_knowledge.bobcat_s740_issues`
            WHERE LOWER(problem_description) LIKE LOWER(@pattern)
               OR LOWER(solution) LIKE LOWER(@pattern)
               OR LOWER(ARRAY_TO_STRING(error_codes, ' ')) LIKE LOWER(@pattern)
            LIMIT 5
            """
            
            job_config = bigquery.QueryJobConfig(
                query_parameters=[bigquery.ScalarQueryParameter("pattern", "STRING", f"%{query}%")]
            )
            
            results = self.bq_client.query(s740_query, job_config=job_config).result()
            
            for row in results:
                knowledge_item = f"🚜 Bobcat S740 {row.problem_type}:\n"
                knowledge_item += f"Problem: {row.problem_description[:200]}...\n"
                if row.solution:
                    knowledge_item += f"Solution: {row.solution[:200]}...\n"
                if row.codes:
                    knowledge_item += f"Error Codes: {row.codes}\n"
                if row.parts:
                    knowledge_item += f"Parts: {row.parts}\n"
                knowledge_item += f"Difficulty: {row.difficulty}, Cost: {row.cost_estimate}"
                
                s740_knowledge.append(knowledge_item)
            
            # Query equipment hacks
            hack_query = f"""
            SELECT 
                hack_type,
                title,
                description,
                benefits,
                cost
            FROM `{self.project_id}.skidsteer_knowledge.equipment_hacks`
            WHERE equipment_model = 'S740'
              AND (LOWER(description) LIKE LOWER(@pattern)
                   OR LOWER(benefits) LIKE LOWER(@pattern))
            LIMIT 3
            """
            
            results = self.bq_client.query(hack_query, job_config=job_config).result()
            
            for row in results:
                hack_item = f"💡 S740 Hack ({row.hack_type}): {row.title}\n"
                hack_item += f"{row.description[:150]}...\n"
                if row.benefits:
                    hack_item += f"Benefits: {row.benefits[:100]}..."
                
                s740_knowledge.append(hack_item)
            
            # Query maintenance schedules
            maintenance_query = f"""
            SELECT 
                service_type,
                interval_hours,
                description,
                ARRAY_TO_STRING(parts_required, ', ') as parts,
                dealer_cost,
                diy_cost
            FROM `{self.project_id}.skidsteer_knowledge.maintenance_schedules`
            WHERE equipment_model = 'Bobcat S740'
              AND LOWER(service_type) LIKE LOWER(@pattern)
            LIMIT 3
            """
            
            results = self.bq_client.query(maintenance_query, job_config=job_config).result()
            
            for row in results:
                maint_item = f"🔧 S740 Maintenance: {row.service_type} (every {row.interval_hours} hrs)\n"
                maint_item += f"{row.description}\n"
                if row.parts:
                    maint_item += f"Parts: {row.parts}\n"
                maint_item += f"Cost: Dealer ${row.dealer_cost}, DIY ${row.diy_cost}"
                
                s740_knowledge.append(maint_item)
                
        except Exception as e:
            logger.debug(f"S740 knowledge query error: {e}")
        
        return s740_knowledge

    async def learn_from_correction(self, original, correction, user="jeremy"):
        """Learn when user corrects Bob"""
        try:
            learning_entry = {
                "original": original,
                "correction": correction,
                "user": user,
                "timestamp": datetime.now().isoformat(),
            }

            # Store in Neo4j/Graphiti
            if self.graphiti_available and self.graphiti:
                await self.graphiti.add_episode(
                    name=f"correction_{datetime.now().isoformat()}",
                    episode_body=f"User corrected: '{original}' should be '{correction}'",
                    source_description=f"Learning from {user}",
                    reference_time=datetime.now(),
                )

            elif self.neo4j_driver:
                with self.neo4j_driver.session() as session:
                    session.run(
                        """
                        CREATE (l:Learning {
                            original: $original,
                            correction: $correction,
                            user: $user,
                            timestamp: datetime()
                        })
                    """,
                        **learning_entry,
                    )

            # Store in BigQuery for analysis
            if self.bq_client:
                table_id = f"{self.project_id}.conversations.corrections"

                try:
                    table = self.bq_client.get_table(table_id)
                except Exception:
                    schema = [
                        bigquery.SchemaField("original", "STRING"),
                        bigquery.SchemaField("correction", "STRING"),
                        bigquery.SchemaField("user", "STRING"),
                        bigquery.SchemaField("timestamp", "TIMESTAMP"),
                    ]
                    table = bigquery.Table(table_id, schema=schema)
                    table = self.bq_client.create_table(table, exists_ok=True)

                errors = self.bq_client.insert_rows_json(table_id, [learning_entry])
                if not errors:
                    logger.info(f"📚 Learned: {original} → {correction}")

        except Exception as e:
            logger.error(f"Failed to learn from correction: {e}")

    async def process_message(self, text, user="jeremy", channel=None):
        """Process message with full memory and learning"""

        try:
            # Check if this is a correction
            if any(word in text.lower() for word in ["actually", "no it's", "correction", "wrong"]):
                # Extract the correction
                await self.learn_from_correction(
                    self.conversation_context[-1] if self.conversation_context else "", text, user
                )

            # Recall relevant past conversations
            # For questions about recent context, get the last few conversations
            if any(phrase in text.lower() for phrase in ["just ask", "what did i", "previous", "before", "earlier"]):
                memory_context = await self.get_recent_conversations(user, limit=3)
            else:
                memory_context = await self.recall_conversations(text, user)

            # Query knowledge base
            knowledge = self.query_knowledge_base(text)
            
            # Query Bobcat S740 specific knowledge if relevant
            s740_knowledge = []
            if any(word in text.lower() for word in ["bobcat", "s740", "skid", "loader", "hydraulic", "dpf", "def"]):
                s740_knowledge = self.query_bobcat_s740_knowledge(text)
                if s740_knowledge:
                    logger.info(f"🚜 Found {len(s740_knowledge)} Bobcat S740 knowledge items")

            # Get Circle of Life insights if available
            circle_insights = None
            if self.circle_available and self.circle_of_life:
                try:
                    circle_insights = await self.circle_of_life.apply_learning(text)
                    logger.info(
                        f"🔄 Circle of Life provided {len(circle_insights.get('suggested_solutions', []))} solutions"
                    )
                except Exception as e:
                    logger.warning(f"Circle of Life query failed: {e}")

            # Build full context
            context_parts = []

            if memory_context:
                context_parts.append("📝 From our previous conversations:")
                context_parts.extend(memory_context[:3])

            if knowledge:
                context_parts.append("\n📚 From knowledge base:")
                context_parts.extend(knowledge[:3])
            
            if s740_knowledge:
                context_parts.append("\n🚜 Bobcat S740 specific knowledge:")
                context_parts.extend(s740_knowledge[:3])

            if circle_insights and circle_insights.get("suggested_solutions"):
                context_parts.append("\n🔄 From Circle of Life learning:")
                context_parts.append(f"Problem category: {circle_insights['category']}")
                context_parts.append(f"Confidence: {circle_insights['confidence']:.1%}")
                for solution in circle_insights["suggested_solutions"][:2]:
                    context_parts.append(f"• {solution[:200]}")

            context = "\n".join(context_parts) if context_parts else ""

            # Build prompt as Jeremy's assistant
            prompt = f"""You are Bob, Jeremy's development assistant and knowledge system.

Current user: {user}
Current project: Bob's Brain - Universal knowledge system with Graphiti, BigQuery, and learning capabilities

Your personality:
- You remember ALL our conversations
- You learn from corrections and improve
- You help with code, architecture, and project planning
- You track our project progress
- You can handle questions about cars, boats, motorcycles, coding, anything
- You speak as Jeremy's partner, not customer service

{context}

User message: {text}

Instructions:
- If this seems like a correction, acknowledge you've learned
- Use any relevant context from our past conversations
- Reference specific knowledge if you have it
- Be helpful, direct, and remember you're Jeremy's assistant
- If discussing our project, show you understand where we are

Response:"""

            # Generate response with Gemini
            if self.genai_client and self.model_available:
                try:
                    response = self.genai_client.models.generate_content(
                        model=self.model_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            temperature=0.7, max_output_tokens=1024, top_p=0.95, top_k=40
                        ),
                    )

                    # Extract text from response
                    if response and response.candidates and response.candidates[0].content.parts:
                        final_response = ""
                        for part in response.candidates[0].content.parts:
                            if part.text:
                                final_response += part.text

                        if final_response:
                            # Remember this conversation
                            await self.remember_conversation(text, final_response, user)

                            # Track context
                            self.conversation_context.append(final_response)
                            if len(self.conversation_context) > 10:
                                self.conversation_context.pop(0)

                            return final_response
                        else:
                            return "I'm processing that, but having trouble forming a response. Let me try again."
                    else:
                        return "I understand, but I'm having trouble generating a proper response right now."

                except Exception as gen_error:
                    logger.error(f"Generation error: {gen_error}")
                    return f"I encountered an issue, but I'm still here. What do you need help with?"
            else:
                # Fallback without model
                return self._get_fallback_response(text, context)

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return f"I hit a snag, but I'm learning. Tell me what you need."

    def _get_fallback_response(self, text, context=""):
        """Fallback response when Gen AI is unavailable"""
        text_lower = text.lower()

        response = "My AI model is temporarily offline, but "

        if context:
            response += f"I found this in my memory:\n{context[:500]}\n\n"

        if "hello" in text_lower or "hi" in text_lower:
            response += "Hey Jeremy! I'm Bob, ready to help with the project."
        elif "graphiti" in text_lower:
            response += "Graphiti is our auto-organizing brain - dump data and it figures out relationships."
        elif "bigquery" in text_lower:
            response += "BigQuery is our massive warehouse - petabytes of manuals, forums, everything."
        elif "remember" in text_lower:
            response += "I'm storing everything we discuss in Neo4j/Graphiti for perfect recall."
        else:
            response += f"Regarding '{text}' - I'll have a better answer once my AI is back."

        return response


# Initialize Bob Brain v5
bob = BobBrainV5()


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "service": "Bob Brain v5.0",
            "version": "5.0.0",
            "model": f"{bob.model_name} (NEW Gen AI SDK)" if bob.model_available else "No model",
            "components": {
                "genai": bob.model_available,
                "graphiti": bob.graphiti_available if hasattr(bob, "graphiti_available") else False,
                "neo4j": hasattr(bob, "neo4j_driver") and bob.neo4j_driver is not None,
                "memory": (hasattr(bob, "memory_available") and bob.memory_available)
                or (hasattr(bob, "memory_cache") and len(bob.memory_cache) >= 0),
                "bigquery": bob.bq_client is not None,
                "datastore": hasattr(bob, "datastore_available") and bob.datastore_available,
                "circle_of_life": hasattr(bob, "circle_available") and bob.circle_available,
                "slack": bob.slack_client is not None,
            },
            "capabilities": {
                "memory": "Full conversation memory",
                "learning": "Learns from corrections",
                "knowledge": "BigQuery warehouse ready",
                "personality": "Jeremy's assistant",
            },
            "sdk": "Google Gen AI SDK",
            "project": bob.project_id,
            "timestamp": time.time(),
        }
    )


@app.route("/slack/events", methods=["POST"])
def slack_events():
    """Handle Slack events"""
    try:
        data = request.json
        logger.info(f"Received Slack event type: {data.get('type')}")

        # URL verification for Slack
        if data.get("type") == "url_verification":
            logger.info("Slack URL verification request")
            return jsonify({"challenge": data["challenge"]})

        # Handle event callbacks
        if data.get("type") == "event_callback":
            event = data.get("event", {})
            event_id = data.get("event_id")
            event_type = event.get("type")

            logger.info(f"Processing event: {event_type}, ID: {event_id}")

            # Prevent duplicate processing
            if event_id in bob.processed_events:
                logger.info(f"Duplicate event {event_id}, skipping")
                return jsonify({"status": "duplicate"})

            bob.processed_events.add(event_id)

            # Clean old events
            if len(bob.processed_events) > bob.max_events:
                bob.processed_events = set(list(bob.processed_events)[-500:])

            # Process messages
            if event_type == "message" and not event.get("bot_id"):
                text = event.get("text", "")
                channel = event.get("channel")
                user = event.get("user")

                logger.info(f"Message from user {user}: {text[:50]}...")

                # Process with async loop
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(bob.process_message(text, user, channel))

                # Send response to Slack
                logger.info(f"About to send response. Client: {bool(bob.slack_client)}, Channel: {channel}")
                if bob.slack_client and channel:
                    try:
                        logger.info(f"Sending to Slack: {response[:100]}")
                        result = bob.slack_client.chat_postMessage(
                            channel=channel, 
                            text=response,
                            timeout=5  # Add explicit timeout
                        )
                        logger.info(f"✅ Responded: {response[:50]}...")
                        logger.info(f"Slack response: {result.get('ok', 'unknown')}")
                    except SlackApiError as e:
                        logger.error(f"Slack API error: {e.response['error']}")
                    except Exception as e:
                        logger.error(f"Unexpected error sending to Slack: {str(e)}")
                else:
                    logger.warning(f"No Slack client ({bool(bob.slack_client)}) or channel ({channel})")

            # Handle app mentions
            elif event_type == "app_mention":
                text = event.get("text", "")
                channel = event.get("channel")
                user = event.get("user")

                # Remove @mention
                text = " ".join(w for w in text.split() if not w.startswith("<@"))

                logger.info(f"App mention from {user}: {text[:50]}...")

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(bob.process_message(text, user, channel))

                if bob.slack_client and channel:
                    try:
                        bob.slack_client.chat_postMessage(channel=channel, text=response)
                        logger.info(f"✅ Responded to mention")
                    except SlackApiError as e:
                        logger.error(f"Slack API error: {e.response['error']}")
            else:
                logger.info(f"Ignoring event type: {event_type}")

        return jsonify({"status": "ok"})

    except Exception as e:
        logger.error(f"Slack event processing error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/test", methods=["GET", "POST"])
def test():
    """Test endpoint with full capabilities"""
    if request.method == "POST":
        data = request.json or {}
        text = data.get("text", "Hello Bob!")
        user = data.get("user", "jeremy")
    else:
        text = request.args.get("text", "Hello Bob!")
        user = request.args.get("user", "jeremy")

    # Process the message
    start_time = time.time()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(bob.process_message(text, user))

    processing_time = time.time() - start_time

    return jsonify(
        {
            "question": text,
            "response": response,
            "user": user,
            "model_used": f"{bob.model_name} (NEW Gen AI SDK)" if bob.model_available else "No model",
            "processing_time_seconds": round(processing_time, 2),
            "components_status": {
                "genai": "✅" if bob.model_available else "❌",
                "memory": "✅" if bob.graphiti_available or bob.neo4j_driver else "❌",
                "bigquery": "✅" if bob.bq_client else "❌",
                "datastore": "✅" if bob.datastore_client else "❌",
                "slack": "✅" if bob.slack_client else "❌",
            },
            "capabilities": {
                "remembers": True,
                "learns": True,
                "queries_knowledge": True,
                "personality": "Jeremy's assistant",
            },
            "version": "5.0.0",
        }
    )


@app.route("/learn", methods=["POST"])
def learn():
    """Endpoint to explicitly teach Bob something"""
    data = request.json or {}
    original = data.get("original", "")
    correction = data.get("correction", "")
    user = data.get("user", "jeremy")

    if not correction:
        return jsonify({"error": "No correction provided"}), 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bob.learn_from_correction(original, correction, user))

    return jsonify(
        {
            "status": "learned",
            "original": original,
            "correction": correction,
            "message": f"Thanks for teaching me! I'll remember that {correction}",
        }
    )


@app.route("/circle-of-life/metrics", methods=["GET"])
def circle_metrics():
    """Get Circle of Life system metrics"""
    if not (hasattr(bob, "circle_available") and bob.circle_available):
        return jsonify({"error": "Circle of Life not available"}), 503

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    metrics = loop.run_until_complete(bob.circle_of_life.get_system_metrics())

    return jsonify(metrics)


@app.route("/circle-of-life/ingest", methods=["POST"])
def circle_ingest():
    """Manually trigger Circle of Life data ingestion"""
    if not (hasattr(bob, "circle_available") and bob.circle_available):
        return jsonify({"error": "Circle of Life not available"}), 503

    data = request.json or {}
    limit = data.get("limit", 10)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    insights = loop.run_until_complete(bob.circle_of_life.ingest_diagnostic_data(limit=limit))

    return jsonify(
        {
            "status": "success",
            "insights_ingested": len(insights),
            "message": f"Ingested {len(insights)} diagnostic insights into Circle of Life",
        }
    )


@app.route("/mvp3/submit-diagnostic", methods=["POST"])
def mvp3_submit():
    """Endpoint for MVP3 to submit diagnostic data and get Bob's insights"""
    data = request.json or {}
    problem = data.get("problem_description", "")
    equipment = data.get("equipment_type", "")
    service = data.get("service_type", "")

    if not problem:
        return jsonify({"error": "No problem description provided"}), 400

    # Get Bob's insights using Circle of Life
    response = {"bob_analysis": "", "suggested_solutions": [], "confidence": 0.0, "similar_cases": []}

    if hasattr(bob, "circle_available") and bob.circle_available:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Get Circle of Life insights
        circle_insights = loop.run_until_complete(bob.circle_of_life.apply_learning(problem))

        response["suggested_solutions"] = circle_insights.get("suggested_solutions", [])
        response["confidence"] = circle_insights.get("confidence", 0.0)
        response["similar_cases"] = circle_insights.get("similar_cases", [])

        # Get Bob's AI analysis if available
        if bob.model_available:
            full_context = f"Equipment: {equipment}\nService: {service}\nProblem: {problem}"
            bob_response = loop.run_until_complete(bob.process_message(full_context))
            response["bob_analysis"] = bob_response

    # Store the diagnostic submission for future learning
    if hasattr(bob, "datastore_available") and bob.datastore_available:
        # This would normally be stored in Datastore, but we're just acknowledging it
        logger.info(f"📝 Received diagnostic from MVP3: {problem[:100]}")

    return jsonify(response)


@app.route("/mvp3/feedback", methods=["POST"])
def mvp3_feedback():
    """Endpoint for MVP3 to provide feedback on Bob's suggestions"""
    data = request.json or {}
    problem = data.get("problem", "")
    suggested = data.get("suggested_solution", "")
    actual = data.get("actual_solution", "")
    success = data.get("success", False)
    rating = data.get("rating", 0)

    if not all([problem, actual]):
        return jsonify({"error": "Missing required feedback data"}), 400

    if hasattr(bob, "circle_available") and bob.circle_available:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Record feedback in Circle of Life
        loop.run_until_complete(bob.circle_of_life.feedback_loop(problem, suggested, actual, success, rating))

        # If unsuccessful, trigger immediate learning
        if not success:
            loop.run_until_complete(bob.learn_from_correction(suggested, actual))

        return jsonify(
            {
                "status": "feedback_recorded",
                "message": "Thanks for the feedback! Bob is learning.",
                "learning_triggered": not success,
            }
        )

    return jsonify({"error": "Circle of Life not available"}), 503


@app.route("/", methods=["GET"])
def index():
    """Root endpoint"""
    return jsonify(
        {
            "service": "Bob's Brain v5.0 - Universal Assistant with Circle of Life",
            "status": "operational",
            "version": "5.0.0",
            "description": "Jeremy's assistant with continuous learning from MVP3 diagnostics",
            "endpoints": {
                "/": "This help message",
                "/health": "Health check with component status",
                "/test": "Test Bob's response and memory",
                "/learn": "Teach Bob a correction",
                "/circle-of-life/metrics": "Get Circle of Life learning metrics",
                "/circle-of-life/ingest": "Trigger diagnostic data ingestion",
                "/mvp3/submit-diagnostic": "Submit diagnostic for Bob's analysis",
                "/mvp3/feedback": "Provide feedback on Bob's suggestions",
                "/slack/events": "Slack event handler",
            },
            "architecture": {
                "ai_model": f"{bob.model_name} via Google Gen AI SDK" if bob.model_available else "Model offline",
                "memory": "Graphiti/Neo4j for perfect recall",
                "knowledge": "BigQuery warehouse for massive data",
                "learning": "Circle of Life continuous learning from MVP3",
                "data_storage": "Datastore for diagnostic insights",
                "deployment": "Google Cloud Run",
            },
            "capabilities": [
                "🧠 Remembers all conversations",
                "📚 Learns from corrections",
                "🔍 Queries massive knowledge base",
                "🔄 Circle of Life continuous learning from MVP3",
                "💬 Acts as development assistant",
                "🚗🚤🏍️ Handles cars, boats, motorcycles, everything",
                "♻️ Auto-organizes dumped data with Graphiti",
                "📊 Pattern recognition from diagnostic data",
            ],
            "user": "Jeremy Longshore",
            "purpose": "Universal knowledge and development assistant",
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"🚀 Starting Bob Brain v5.0 with Circle of Life on port {port}")
    logger.info("🧠 Memory: ACTIVE | Learning: ENABLED | Knowledge: READY")
    logger.info("🔄 Circle of Life: Continuous learning from MVP3 diagnostics")
    app.run(host="0.0.0.0", port=port, debug=False)
