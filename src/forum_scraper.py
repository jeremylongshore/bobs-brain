#!/usr/bin/env python3
"""
Forum Scraper for Bob's Brain - Circle of Life Integration
Scrapes repair and maintenance forums to build comprehensive knowledge base
Uses Playwright for JavaScript-heavy sites and integrates with BigQuery
"""

import asyncio
import hashlib
import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse

from google.cloud import bigquery
from playwright.async_api import async_playwright, Page, Browser

logger = logging.getLogger(__name__)


class ForumIntelligenceScraper:
    """
    Intelligent forum scraper that discovers, classifies, and extracts
    repair/maintenance knowledge from online forums
    """

    def __init__(self, project_id="bobs-house-ai"):
        """Initialize scraper with BigQuery integration"""
        self.project_id = project_id
        self.bq_client = bigquery.Client(project=project_id)
        self.browser = None
        self.context = None
        
        # Forum patterns for detection
        self.forum_patterns = {
            "vbulletin": ["vbulletin", "showthread.php", "forumdisplay.php"],
            "phpbb": ["phpbb", "viewtopic.php", "viewforum.php"],
            "discourse": ["discourse", "/t/", "/c/"],
            "xenforo": ["xenforo", "threads/", "forums/"],
            "invision": ["invision", "topic/", "forum/"],
            "smf": ["smf", "index.php?topic", "index.php?board"],
            "reddit": ["reddit.com", "/r/", "/comments/"],
            "tapatalk": ["tapatalk", "?fid=", "?tid="],
        }
        
        # Initialize BigQuery tables
        self._ensure_scraper_tables()
        logger.info("🕷️ Forum Intelligence Scraper initialized")

    def _ensure_scraper_tables(self):
        """Create BigQuery tables for scraped forum data"""
        dataset_id = f"{self.project_id}.scraped_data"
        dataset = bigquery.Dataset(dataset_id)
        dataset.description = "Forum scraped data for knowledge building"
        dataset.location = "US"
        
        try:
            self.bq_client.create_dataset(dataset, exists_ok=True)
            logger.info("📊 Scraped data dataset ready")
        except Exception as e:
            logger.debug(f"Dataset exists or error: {e}")
        
        # Create comprehensive forum tables
        tables = {
            "forums": [
                bigquery.SchemaField("forum_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("url", "STRING"),
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("platform", "STRING"),
                bigquery.SchemaField("requires_login", "BOOL"),
                bigquery.SchemaField("categories", "STRING", mode="REPEATED"),
                bigquery.SchemaField("member_count", "INT64"),
                bigquery.SchemaField("thread_count", "INT64"),
                bigquery.SchemaField("specialties", "STRING", mode="REPEATED"),
                bigquery.SchemaField("last_scraped", "TIMESTAMP"),
                bigquery.SchemaField("scrape_status", "STRING"),
            ],
            "forum_threads": [
                bigquery.SchemaField("thread_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("forum_id", "STRING"),
                bigquery.SchemaField("url", "STRING"),
                bigquery.SchemaField("title", "STRING"),
                bigquery.SchemaField("category", "STRING"),
                bigquery.SchemaField("problem_description", "STRING"),
                bigquery.SchemaField("solution", "STRING"),
                bigquery.SchemaField("equipment_mentioned", "STRING", mode="REPEATED"),
                bigquery.SchemaField("view_count", "INT64"),
                bigquery.SchemaField("reply_count", "INT64"),
                bigquery.SchemaField("solved", "BOOL"),
                bigquery.SchemaField("author", "STRING"),
                bigquery.SchemaField("created_date", "TIMESTAMP"),
                bigquery.SchemaField("scraped_at", "TIMESTAMP"),
            ],
            "expert_members": [
                bigquery.SchemaField("member_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("forum_id", "STRING"),
                bigquery.SchemaField("username", "STRING"),
                bigquery.SchemaField("reputation", "INT64"),
                bigquery.SchemaField("post_count", "INT64"),
                bigquery.SchemaField("specialties", "STRING", mode="REPEATED"),
                bigquery.SchemaField("helpful_posts", "INT64"),
                bigquery.SchemaField("profile_url", "STRING"),
            ],
            "repair_solutions": [
                bigquery.SchemaField("solution_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("problem_category", "STRING"),
                bigquery.SchemaField("problem", "STRING"),
                bigquery.SchemaField("solution", "STRING"),
                bigquery.SchemaField("equipment_type", "STRING"),
                bigquery.SchemaField("parts_needed", "STRING", mode="REPEATED"),
                bigquery.SchemaField("tools_required", "STRING", mode="REPEATED"),
                bigquery.SchemaField("difficulty_level", "STRING"),
                bigquery.SchemaField("time_estimate", "STRING"),
                bigquery.SchemaField("cost_estimate", "STRING"),
                bigquery.SchemaField("source_url", "STRING"),
                bigquery.SchemaField("confidence_score", "FLOAT64"),
                bigquery.SchemaField("extracted_at", "TIMESTAMP"),
            ],
        }
        
        for table_name, schema in tables.items():
            table_id = f"{self.project_id}.scraped_data.{table_name}"
            table = bigquery.Table(table_id, schema=schema)
            
            try:
                self.bq_client.create_table(table, exists_ok=True)
                logger.info(f"✅ Table ready: {table_name}")
            except Exception as e:
                logger.debug(f"Table {table_name} exists or error: {e}")

    async def initialize_browser(self):
        """Initialize Playwright browser for scraping"""
        if not self.browser:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--no-first-run',
                    '--no-zygote',
                    '--single-process',  # Important for Cloud Run
                ]
            )
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            logger.info("🌐 Browser initialized for scraping")

    async def close_browser(self):
        """Clean up browser resources"""
        if self.browser:
            await self.browser.close()
            self.browser = None
            self.context = None

    async def discover_forums(self, search_queries: List[str]) -> List[Dict]:
        """
        Discover repair forums using search queries
        """
        await self.initialize_browser()
        discovered_forums = []
        
        # Common repair forum domains to check
        known_forums = [
            "https://www.reddit.com/r/MechanicAdvice",
            "https://www.reddit.com/r/DIY",
            "https://www.reddit.com/r/fixit",
            "https://mechanics.stackexchange.com",
            "https://www.diychatroom.com",
            "https://www.doityourself.com/forum",
            "https://www.garagejournal.com/forum",
            "https://www.bobistheoilguy.com/forums",
            "https://www.cartalk.com/community",
            "https://www.justanswer.com",
            "https://repairpal.com/community",
            "https://www.yourmechanic.com/community",
        ]
        
        # Check each known forum
        for forum_url in known_forums:
            try:
                forum_info = await self.analyze_forum(forum_url)
                if forum_info:
                    discovered_forums.append(forum_info)
                    logger.info(f"✅ Discovered forum: {forum_url}")
            except Exception as e:
                logger.error(f"Failed to analyze {forum_url}: {e}")
        
        # Also search for forums based on queries
        for query in search_queries:
            try:
                search_url = f"https://www.google.com/search?q={query}+forum+repair+maintenance"
                page = await self.context.new_page()
                await page.goto(search_url, wait_until='networkidle')
                
                # Extract search results
                links = await page.evaluate("""
                    () => {
                        const links = [];
                        document.querySelectorAll('a[href*="forum"], a[href*="/r/"]').forEach(a => {
                            const href = a.href;
                            if (href && !href.includes('google.com')) {
                                links.push(href);
                            }
                        });
                        return links.slice(0, 10);
                    }
                """)
                
                await page.close()
                
                # Analyze each discovered forum
                for link in links:
                    try:
                        forum_info = await self.analyze_forum(link)
                        if forum_info and not any(f['url'] == forum_info['url'] for f in discovered_forums):
                            discovered_forums.append(forum_info)
                    except Exception as e:
                        logger.debug(f"Failed to analyze {link}: {e}")
                        
            except Exception as e:
                logger.error(f"Search failed for '{query}': {e}")
        
        logger.info(f"🔍 Discovered {len(discovered_forums)} forums total")
        return discovered_forums

    async def analyze_forum(self, url: str) -> Optional[Dict]:
        """
        Analyze a forum to determine its characteristics
        """
        try:
            page = await self.context.new_page()
            await page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Detect forum platform
            platform = await self._detect_platform(page, url)
            
            # Extract forum metadata
            forum_info = {
                "forum_id": hashlib.md5(url.encode()).hexdigest(),
                "url": url,
                "name": await self._extract_forum_name(page),
                "platform": platform,
                "requires_login": await self._check_login_requirement(page),
                "categories": await self._extract_categories(page, platform),
                "member_count": await self._extract_member_count(page),
                "thread_count": await self._extract_thread_count(page),
                "specialties": await self._identify_specialties(page),
                "last_scraped": datetime.now(),
                "scrape_status": "discovered",
            }
            
            await page.close()
            
            # Store forum info in BigQuery
            await self._store_forum_info(forum_info)
            
            return forum_info
            
        except Exception as e:
            logger.error(f"Failed to analyze forum {url}: {e}")
            return None

    async def _detect_platform(self, page: Page, url: str) -> str:
        """Detect the forum platform type"""
        page_content = await page.content()
        url_lower = url.lower()
        
        for platform, patterns in self.forum_patterns.items():
            for pattern in patterns:
                if pattern in url_lower or pattern in page_content.lower():
                    return platform
        
        # Check meta tags
        platform_meta = await page.evaluate("""
            () => {
                const generator = document.querySelector('meta[name="generator"]');
                return generator ? generator.content : null;
            }
        """)
        
        if platform_meta:
            return platform_meta.lower().split()[0]
        
        return "unknown"

    async def _extract_forum_name(self, page: Page) -> str:
        """Extract forum name"""
        try:
            return await page.evaluate("""
                () => {
                    const title = document.querySelector('title');
                    const h1 = document.querySelector('h1');
                    const siteName = document.querySelector('meta[property="og:site_name"]');
                    
                    if (siteName) return siteName.content;
                    if (h1) return h1.textContent.trim();
                    if (title) return title.textContent.split('|')[0].trim();
                    return 'Unknown Forum';
                }
            """)
        except:
            return "Unknown Forum"

    async def _check_login_requirement(self, page: Page) -> bool:
        """Check if forum requires login to view content"""
        try:
            login_indicators = await page.evaluate("""
                () => {
                    const loginRequired = document.querySelector('.login-required, .must-login');
                    const loginModal = document.querySelector('[class*="login-modal"]');
                    const restrictedContent = document.body.textContent.includes('must be logged in');
                    
                    return !!(loginRequired || loginModal || restrictedContent);
                }
            """)
            return login_indicators
        except:
            return False

    async def _extract_categories(self, page: Page, platform: str) -> List[str]:
        """Extract forum categories"""
        try:
            selectors = {
                "reddit": ".subreddit-sidebar .md h3",
                "discourse": ".category-list .category-name",
                "phpbb": ".forabg .header dt a",
                "vbulletin": ".forumbit_post .forumtitle",
                "default": '[class*="category"], [class*="forum-title"], [href*="/forum/"], [href*="/category/"]'
            }
            
            selector = selectors.get(platform, selectors["default"])
            
            categories = await page.evaluate(f"""
                () => {{
                    const elements = document.querySelectorAll('{selector}');
                    const cats = [];
                    elements.forEach(el => {{
                        const text = el.textContent.trim();
                        if (text && text.length < 100) {{
                            cats.push(text);
                        }}
                    }});
                    return cats.slice(0, 20);
                }}
            """)
            
            return categories
        except:
            return []

    async def _extract_member_count(self, page: Page) -> int:
        """Extract forum member count"""
        try:
            member_text = await page.evaluate("""
                () => {
                    const statsText = document.body.textContent;
                    const memberMatch = statsText.match(/(\\d+[,\\d]*)[\\s]*(members?|users?|subscribers?)/i);
                    if (memberMatch) {
                        return parseInt(memberMatch[1].replace(/,/g, ''));
                    }
                    return 0;
                }
            """)
            return member_text
        except:
            return 0

    async def _extract_thread_count(self, page: Page) -> int:
        """Extract forum thread count"""
        try:
            thread_text = await page.evaluate("""
                () => {
                    const statsText = document.body.textContent;
                    const threadMatch = statsText.match(/(\\d+[,\\d]*)[\\s]*(threads?|topics?|posts?|discussions?)/i);
                    if (threadMatch) {
                        return parseInt(threadMatch[1].replace(/,/g, ''));
                    }
                    return 0;
                }
            """)
            return thread_text
        except:
            return 0

    async def _identify_specialties(self, page: Page) -> List[str]:
        """Identify forum specialties based on content"""
        try:
            content = await page.evaluate("() => document.body.textContent.toLowerCase()")
            
            specialties = []
            specialty_keywords = {
                "automotive": ["car", "vehicle", "automotive", "mechanic"],
                "marine": ["boat", "marine", "nautical", "yacht"],
                "motorcycle": ["motorcycle", "bike", "harley", "honda"],
                "diesel": ["diesel", "truck", "heavy duty"],
                "electrical": ["electrical", "wiring", "voltage"],
                "hvac": ["hvac", "heating", "cooling", "air conditioning"],
                "plumbing": ["plumbing", "pipe", "drain", "water"],
                "appliance": ["appliance", "washer", "dryer", "refrigerator"],
            }
            
            for specialty, keywords in specialty_keywords.items():
                if any(keyword in content for keyword in keywords):
                    specialties.append(specialty)
            
            return specialties[:5]  # Limit to top 5 specialties
        except:
            return []

    async def scrape_forum_threads(self, forum_info: Dict, max_threads: int = 100) -> List[Dict]:
        """
        Scrape threads from a forum
        """
        if forum_info.get("requires_login"):
            logger.warning(f"⚠️ Forum requires login: {forum_info['url']}")
            return []
        
        await self.initialize_browser()
        threads = []
        
        try:
            page = await self.context.new_page()
            await page.goto(forum_info['url'], wait_until='networkidle')
            
            # Find thread links based on platform
            thread_selectors = {
                "reddit": 'a[href*="/comments/"]',
                "discourse": 'a.title[href*="/t/"]',
                "phpbb": 'a.topictitle',
                "vbulletin": 'a.title[href*="showthread"]',
                "default": 'a[href*="thread"], a[href*="topic"], a[class*="thread-title"]'
            }
            
            selector = thread_selectors.get(forum_info['platform'], thread_selectors["default"])
            
            # Extract thread URLs
            thread_urls = await page.evaluate(f"""
                () => {{
                    const links = document.querySelectorAll('{selector}');
                    const urls = [];
                    links.forEach(link => {{
                        if (link.href && !urls.includes(link.href)) {{
                            urls.push(link.href);
                        }}
                    }});
                    return urls.slice(0, {max_threads});
                }}
            """)
            
            await page.close()
            
            # Scrape each thread
            for thread_url in thread_urls[:max_threads]:
                try:
                    thread_data = await self.scrape_thread(thread_url, forum_info)
                    if thread_data:
                        threads.append(thread_data)
                        
                        # Store in BigQuery immediately
                        await self._store_thread_data(thread_data)
                        
                        # Extract and store solutions
                        if thread_data.get('solution'):
                            await self._extract_and_store_solution(thread_data)
                        
                except Exception as e:
                    logger.error(f"Failed to scrape thread {thread_url}: {e}")
                
                # Rate limiting
                await asyncio.sleep(1)
            
            logger.info(f"📚 Scraped {len(threads)} threads from {forum_info['name']}")
            
        except Exception as e:
            logger.error(f"Failed to scrape forum threads: {e}")
        
        return threads

    async def scrape_thread(self, url: str, forum_info: Dict) -> Optional[Dict]:
        """
        Scrape individual thread for repair/maintenance information
        """
        try:
            page = await self.context.new_page()
            await page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Extract thread data
            thread_data = {
                "thread_id": hashlib.md5(url.encode()).hexdigest(),
                "forum_id": forum_info['forum_id'],
                "url": url,
                "title": await self._extract_thread_title(page),
                "category": await self._extract_thread_category(page),
                "problem_description": await self._extract_problem(page),
                "solution": await self._extract_solution(page),
                "equipment_mentioned": await self._extract_equipment(page),
                "view_count": await self._extract_view_count(page),
                "reply_count": await self._extract_reply_count(page),
                "solved": await self._check_if_solved(page),
                "author": await self._extract_author(page),
                "created_date": await self._extract_date(page),
                "scraped_at": datetime.now(),
            }
            
            await page.close()
            return thread_data
            
        except Exception as e:
            logger.error(f"Failed to scrape thread {url}: {e}")
            return None

    async def _extract_thread_title(self, page: Page) -> str:
        """Extract thread title"""
        try:
            return await page.evaluate("""
                () => {
                    const h1 = document.querySelector('h1');
                    const title = document.querySelector('.thread-title, .topic-title, [class*="title"]');
                    const pageTitle = document.title;
                    
                    if (h1) return h1.textContent.trim();
                    if (title) return title.textContent.trim();
                    return pageTitle.split('|')[0].trim();
                }
            """)
        except:
            return "Unknown Thread"

    async def _extract_thread_category(self, page: Page) -> str:
        """Extract thread category"""
        try:
            return await page.evaluate("""
                () => {
                    const breadcrumb = document.querySelector('.breadcrumb li:nth-last-child(2)');
                    const category = document.querySelector('.category-name, .forum-name');
                    
                    if (breadcrumb) return breadcrumb.textContent.trim();
                    if (category) return category.textContent.trim();
                    return 'General';
                }
            """)
        except:
            return "General"

    async def _extract_problem(self, page: Page) -> str:
        """Extract problem description from first post"""
        try:
            return await page.evaluate("""
                () => {
                    const firstPost = document.querySelector('.post-content, .entry-content, .message-content, [class*="post-body"]');
                    if (firstPost) {
                        const text = firstPost.textContent.trim();
                        return text.substring(0, 1000);  // Limit to 1000 chars
                    }
                    return '';
                }
            """)
        except:
            return ""

    async def _extract_solution(self, page: Page) -> str:
        """Extract solution from thread"""
        try:
            return await page.evaluate("""
                () => {
                    // Look for marked solutions
                    const solution = document.querySelector('.solution, .best-answer, [class*="accepted"]');
                    if (solution) {
                        return solution.textContent.trim().substring(0, 1000);
                    }
                    
                    // Look for posts with "solved" or "fixed"
                    const posts = document.querySelectorAll('.post-content, .message-content');
                    for (const post of posts) {
                        const text = post.textContent.toLowerCase();
                        if (text.includes('solved') || text.includes('fixed') || text.includes('solution')) {
                            return post.textContent.trim().substring(0, 1000);
                        }
                    }
                    
                    return '';
                }
            """)
        except:
            return ""

    async def _extract_equipment(self, page: Page) -> List[str]:
        """Extract equipment/vehicle mentions"""
        try:
            content = await page.evaluate("() => document.body.textContent")
            
            # Common equipment patterns
            equipment_patterns = [
                r'\b\d{4}\s+\w+\s+\w+\b',  # Year Make Model
                r'\b[A-Z][a-z]+\s+[A-Z]\d+\b',  # Model numbers
                r'\b(?:Ford|Chevy|Toyota|Honda|BMW|Mercedes|Audi|VW|Nissan|Mazda)\s+\w+\b',
                r'\b(?:Yamaha|Suzuki|Kawasaki|Harley|Honda)\s+\w+\b',  # Motorcycles
                r'\b(?:John Deere|Caterpillar|Kubota|Case)\s+\w+\b',  # Equipment
            ]
            
            equipment = set()
            for pattern in equipment_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                equipment.update(matches[:5])  # Limit matches per pattern
            
            return list(equipment)[:10]  # Return top 10
        except:
            return []

    async def _extract_view_count(self, page: Page) -> int:
        """Extract thread view count"""
        try:
            return await page.evaluate("""
                () => {
                    const viewText = document.body.textContent;
                    const viewMatch = viewText.match(/(\\d+[,\\d]*)[\\s]*(views?|viewed)/i);
                    if (viewMatch) {
                        return parseInt(viewMatch[1].replace(/,/g, ''));
                    }
                    return 0;
                }
            """)
        except:
            return 0

    async def _extract_reply_count(self, page: Page) -> int:
        """Extract thread reply count"""
        try:
            return await page.evaluate("""
                () => {
                    const posts = document.querySelectorAll('.post, .message, .comment, [class*="post-content"]');
                    return posts.length - 1;  // Subtract original post
                }
            """)
        except:
            return 0

    async def _check_if_solved(self, page: Page) -> bool:
        """Check if thread is marked as solved"""
        try:
            return await page.evaluate("""
                () => {
                    const solved = document.querySelector('.solved, .resolved, [class*="solution"]');
                    const titleSolved = document.title.toLowerCase().includes('solved');
                    const contentSolved = document.body.textContent.toLowerCase().includes('[solved]');
                    
                    return !!(solved || titleSolved || contentSolved);
                }
            """)
        except:
            return False

    async def _extract_author(self, page: Page) -> str:
        """Extract thread author"""
        try:
            return await page.evaluate("""
                () => {
                    const author = document.querySelector('.author-name, .username, .post-author, [class*="author"]');
                    if (author) return author.textContent.trim();
                    return 'Anonymous';
                }
            """)
        except:
            return "Anonymous"

    async def _extract_date(self, page: Page) -> datetime:
        """Extract thread creation date"""
        try:
            date_str = await page.evaluate("""
                () => {
                    const time = document.querySelector('time[datetime]');
                    if (time) return time.getAttribute('datetime');
                    
                    const dateElement = document.querySelector('.post-date, .date, [class*="time"]');
                    if (dateElement) return dateElement.textContent.trim();
                    
                    return null;
                }
            """)
            
            if date_str:
                # Try to parse the date (simplified)
                from dateutil import parser
                return parser.parse(date_str)
            
        except:
            pass
        
        return datetime.now()

    async def _store_forum_info(self, forum_info: Dict):
        """Store forum information in BigQuery"""
        try:
            table_id = f"{self.project_id}.scraped_data.forums"
            errors = self.bq_client.insert_rows_json(table_id, [forum_info])
            
            if errors:
                logger.error(f"Failed to store forum info: {errors}")
            else:
                logger.info(f"✅ Stored forum info: {forum_info['name']}")
        except Exception as e:
            logger.error(f"Failed to store forum info: {e}")

    async def _store_thread_data(self, thread_data: Dict):
        """Store thread data in BigQuery"""
        try:
            table_id = f"{self.project_id}.scraped_data.forum_threads"
            
            # Convert datetime to ISO format for BigQuery
            if isinstance(thread_data.get('created_date'), datetime):
                thread_data['created_date'] = thread_data['created_date'].isoformat()
            if isinstance(thread_data.get('scraped_at'), datetime):
                thread_data['scraped_at'] = thread_data['scraped_at'].isoformat()
            
            errors = self.bq_client.insert_rows_json(table_id, [thread_data])
            
            if errors:
                logger.error(f"Failed to store thread: {errors}")
            else:
                logger.debug(f"✅ Stored thread: {thread_data['title'][:50]}")
        except Exception as e:
            logger.error(f"Failed to store thread data: {e}")

    async def _extract_and_store_solution(self, thread_data: Dict):
        """Extract structured solution and store in repair_solutions table"""
        if not thread_data.get('solution'):
            return
        
        try:
            solution_data = {
                "solution_id": hashlib.md5(f"{thread_data['thread_id']}_solution".encode()).hexdigest(),
                "problem_category": self._categorize_problem(thread_data.get('problem_description', '')),
                "problem": thread_data.get('problem_description', '')[:500],
                "solution": thread_data.get('solution', '')[:1000],
                "equipment_type": thread_data.get('equipment_mentioned', ['Unknown'])[0] if thread_data.get('equipment_mentioned') else 'Unknown',
                "parts_needed": self._extract_parts(thread_data.get('solution', '')),
                "tools_required": self._extract_tools(thread_data.get('solution', '')),
                "difficulty_level": self._assess_difficulty(thread_data.get('solution', '')),
                "time_estimate": self._extract_time_estimate(thread_data.get('solution', '')),
                "cost_estimate": self._extract_cost_estimate(thread_data.get('solution', '')),
                "source_url": thread_data['url'],
                "confidence_score": 0.8 if thread_data.get('solved') else 0.5,
                "extracted_at": datetime.now().isoformat(),
            }
            
            table_id = f"{self.project_id}.scraped_data.repair_solutions"
            errors = self.bq_client.insert_rows_json(table_id, [solution_data])
            
            if not errors:
                logger.debug(f"✅ Stored repair solution from thread")
                
        except Exception as e:
            logger.error(f"Failed to extract/store solution: {e}")

    def _categorize_problem(self, description: str) -> str:
        """Categorize problem based on description"""
        description_lower = description.lower()
        
        categories = {
            "electrical": ["electrical", "battery", "alternator", "starter", "lights"],
            "engine": ["engine", "motor", "cylinder", "piston", "valve"],
            "transmission": ["transmission", "gear", "clutch", "shifting"],
            "brake": ["brake", "pad", "rotor", "caliper", "abs"],
            "cooling": ["cooling", "radiator", "coolant", "overheating"],
            "fuel": ["fuel", "gas", "pump", "injector"],
        }
        
        for category, keywords in categories.items():
            if any(keyword in description_lower for keyword in keywords):
                return category
        
        return "general"

    def _extract_parts(self, solution_text: str) -> List[str]:
        """Extract parts mentioned in solution"""
        parts_patterns = [
            r'(?:replace|install|need|buy)\s+(?:a\s+)?(\w+\s+\w+)',
            r'(\w+\s+(?:filter|pump|valve|belt|hose|bearing|seal))',
        ]
        
        parts = set()
        for pattern in parts_patterns:
            matches = re.findall(pattern, solution_text, re.IGNORECASE)
            parts.update(matches[:5])
        
        return list(parts)[:10]

    def _extract_tools(self, solution_text: str) -> List[str]:
        """Extract tools mentioned in solution"""
        tools_keywords = [
            "wrench", "socket", "screwdriver", "pliers", "hammer",
            "jack", "multimeter", "scanner", "gauge", "torque"
        ]
        
        tools = []
        solution_lower = solution_text.lower()
        for tool in tools_keywords:
            if tool in solution_lower:
                tools.append(tool)
        
        return tools[:5]

    def _assess_difficulty(self, solution_text: str) -> str:
        """Assess repair difficulty"""
        solution_lower = solution_text.lower()
        
        if any(word in solution_lower for word in ["easy", "simple", "basic", "diy"]):
            return "easy"
        elif any(word in solution_lower for word in ["moderate", "intermediate", "some experience"]):
            return "moderate"
        elif any(word in solution_lower for word in ["difficult", "advanced", "professional", "dealer"]):
            return "hard"
        
        return "moderate"

    def _extract_time_estimate(self, solution_text: str) -> str:
        """Extract time estimate from solution"""
        time_pattern = r'(\d+)\s*(hours?|minutes?|mins?|hrs?|days?)'
        match = re.search(time_pattern, solution_text, re.IGNORECASE)
        
        if match:
            return f"{match.group(1)} {match.group(2)}"
        
        return "unknown"

    def _extract_cost_estimate(self, solution_text: str) -> str:
        """Extract cost estimate from solution"""
        cost_pattern = r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)'
        match = re.search(cost_pattern, solution_text)
        
        if match:
            return match.group(0)
        
        return "unknown"

    async def run_comprehensive_scrape(self, search_queries: List[str] = None) -> Dict:
        """
        Run comprehensive forum scraping operation
        """
        if not search_queries:
            search_queries = [
                "car repair",
                "auto maintenance",
                "motorcycle repair",
                "boat maintenance",
                "diesel repair",
                "equipment repair",
                "small engine repair",
                "hvac repair",
            ]
        
        logger.info("🚀 Starting comprehensive forum scraping operation")
        
        try:
            # Initialize browser
            await self.initialize_browser()
            
            # Phase 1: Discover forums
            logger.info("📡 Phase 1: Discovering forums...")
            forums = await self.discover_forums(search_queries)
            
            # Phase 2: Scrape threads from each forum
            logger.info("📚 Phase 2: Scraping forum threads...")
            total_threads = 0
            total_solutions = 0
            
            for forum in forums:
                logger.info(f"Scraping {forum['name']}...")
                threads = await self.scrape_forum_threads(forum, max_threads=50)
                total_threads += len(threads)
                total_solutions += sum(1 for t in threads if t.get('solution'))
                
                # Update forum status
                forum['scrape_status'] = 'completed'
                forum['thread_count'] = len(threads)
                await self._store_forum_info(forum)
            
            # Phase 3: Generate summary report
            report = {
                "scrape_id": hashlib.md5(f"scrape_{datetime.now().isoformat()}".encode()).hexdigest(),
                "timestamp": datetime.now().isoformat(),
                "forums_discovered": len(forums),
                "threads_scraped": total_threads,
                "solutions_found": total_solutions,
                "forums": [
                    {
                        "name": f['name'],
                        "url": f['url'],
                        "platform": f['platform'],
                        "requires_login": f['requires_login'],
                        "threads_scraped": f.get('thread_count', 0)
                    }
                    for f in forums
                ],
                "status": "completed"
            }
            
            logger.info(f"""
            ✅ Scraping Operation Complete!
            ===========================
            Forums Discovered: {len(forums)}
            Threads Scraped: {total_threads}
            Solutions Found: {total_solutions}
            Data stored in BigQuery: scraped_data dataset
            """)
            
            return report
            
        except Exception as e:
            logger.error(f"Scraping operation failed: {e}")
            return {"status": "failed", "error": str(e)}
        
        finally:
            await self.close_browser()


async def main():
    """Main function for testing"""
    scraper = ForumIntelligenceScraper()
    
    # Run comprehensive scrape
    report = await scraper.run_comprehensive_scrape()
    
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())