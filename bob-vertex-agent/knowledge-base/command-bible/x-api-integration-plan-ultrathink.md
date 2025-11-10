# 🧠 ULTRATHINK: X API Integration Implementation Plan
**Complete Architecture for Slash Command X Posting System**

**Created:** October 4, 2025
**Status:** Strategic Planning Document

---

## 🎯 GOAL

Implement enterprise-grade X posting system for slash commands with:
1. ✅ Proper draft workflow (X API doesn't support drafts natively)
2. ✅ Best practices from X API documentation
3. ✅ Integration with existing 5 slash commands
4. ✅ Automated token refresh system
5. ✅ Comprehensive error handling
6. ✅ Rate limit management
7. ✅ Thread posting capabilities

---

## 📊 CURRENT STATE ANALYSIS

### Existing Slash Commands That Post to X

| Command | Current Method | Token Type | Issues |
|---------|---------------|------------|--------|
| `/content-nuke` | post_x_thread.py | OAuth 2.0 | Token expires every 2hrs |
| `/blog-single-startai` | post_x_thread.py | OAuth 2.0 | Token expires every 2hrs |
| `/blog-both-x` | Direct API calls | OAuth 2.0 | Token expires every 2hrs |
| `/blog-jeremy-x` | Direct API calls | OAuth 2.0 | Token expires every 2hrs |
| `/post-x` | post_x_thread.py | OAuth 2.0 | Token expires every 2hrs |

### Current System Components

```
Existing System:
├── /home/jeremy/projects/content-nuke/scripts/post_x_thread.py
│   └── Uses requests library (not tweepy)
│   └── OAuth 2.0 only (no OAuth 1.0a support)
│   └── Parses "TWEET X/Y:" format
├── /home/jeremy/waygate-mcp/.env
│   └── Stores OAuth 2.0 tokens
│   └── Auto-refreshed every 90 min (NEW!)
└── /home/jeremy/x-token-automation/
    └── Automated token refresh system (NEW!)
```

---

## 🏗️ PROPOSED ARCHITECTURE

### Phase 1: Draft Management System

**Problem:** X API doesn't support drafts natively.

**Solution:** File-based draft workflow with validation pipeline.

```
Draft Workflow:
┌─────────────────────────────────────────────────┐
│ 1. Content Generation (Slash Command)          │
│    → Claude generates thread content           │
│    → Saves to drafts/ directory                │
└────────────────┬────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────┐
│ 2. Draft Storage & Validation                   │
│    Location: x-threads/drafts/                  │
│    Format: YYYY-MM-DD-topic-DRAFT.md           │
│    Contains:                                     │
│      - Raw thread content                       │
│      - Character counts                         │
│      - Metadata (hashtags, links)              │
│      - Review notes                             │
└────────────────┬────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────┐
│ 3. User Review & Approval                       │
│    User edits draft manually or via command     │
│    Validates:                                   │
│      - Character limits (280 per tweet)        │
│      - Hashtag count (max 2)                   │
│      - Thread coherence                         │
│      - Link formatting                          │
└────────────────┬────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────┐
│ 4. Conversion to Posting Format                 │
│    Convert draft → TWEET X/Y format            │
│    Move to ready-to-post/                      │
│    File: YYYY-MM-DD-topic-x7.txt              │
└────────────────┬────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────────┐
│ 5. Automated Posting via post_x_thread.py      │
│    Reads TWEET X/Y format                      │
│    Posts sequentially with 2s delay            │
│    Handles threading (in_reply_to_tweet_id)   │
└─────────────────────────────────────────────────┘
```

### Phase 2: Enhanced post_x_thread.py

**Current Issues:**
- ❌ Uses `requests` library (not tweepy - best practice)
- ❌ No OAuth 1.0a support (permanent tokens)
- ❌ Limited error handling
- ❌ No rate limit detection
- ❌ No retry logic

**Proposed Enhancement:**

```python
#!/usr/bin/env python3
"""
Enhanced X Thread Posting with Best Practices
Implements tweepy, OAuth 1.0a, rate limiting, error handling
"""
import os
import sys
import time
import json
from pathlib import Path
import tweepy
from tweepy.errors import TweepyException, TooManyRequests

class XThreadPoster:
    """
    Enterprise-grade X thread posting system
    """

    def __init__(self):
        self.client = self._initialize_client()
        self.api_v1 = self._initialize_v1_api()  # For media uploads

    def _initialize_client(self):
        """
        Initialize tweepy client with OAuth 1.0a (permanent tokens)
        Falls back to OAuth 2.0 if 1.0a not available
        """
        # Try OAuth 1.0a first (PERMANENT - never expires)
        consumer_key = os.getenv('X_API_KEY')
        consumer_secret = os.getenv('X_API_SECRET')
        access_token = os.getenv('X_ACCESS_TOKEN')
        access_token_secret = os.getenv('X_ACCESS_SECRET')

        if all([consumer_key, consumer_secret, access_token, access_token_secret]):
            print("🔑 Using OAuth 1.0a (permanent tokens)")
            return tweepy.Client(
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
                wait_on_rate_limit=True  # Auto-handle rate limits
            )

        # Fallback to OAuth 2.0 (expires every 2 hours)
        bearer_token = self._load_oauth2_token()
        if bearer_token:
            print("⚠️  Using OAuth 2.0 (expires every 2 hours)")
            return tweepy.Client(
                bearer_token=bearer_token,
                wait_on_rate_limit=True
            )

        raise ValueError("No valid X API credentials found")

    def _load_oauth2_token(self):
        """Load OAuth 2.0 token from waygate-mcp or pass"""
        # Try waygate-mcp first
        waygate_env = Path.home() / "waygate-mcp" / ".env"
        if waygate_env.exists():
            with open(waygate_env) as f:
                for line in f:
                    if line.startswith('X_OAUTH2_ACCESS_TOKEN='):
                        return line.split('=', 1)[1].strip()

        # Try pass
        try:
            import subprocess
            result = subprocess.run(
                ["pass", "x/oauth2/access_token"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass

        return None

    def post_tweet(self, text, reply_to_id=None, max_retries=3):
        """
        Post a single tweet with retry logic and error handling
        """
        # Validate character limit
        if len(text) > 280:
            raise ValueError(f"Tweet exceeds 280 characters: {len(text)}")

        for attempt in range(max_retries):
            try:
                response = self.client.create_tweet(
                    text=text,
                    in_reply_to_tweet_id=reply_to_id
                )
                tweet_id = response.data['id']
                return tweet_id

            except TooManyRequests as e:
                wait_time = 60 * (attempt + 1)
                print(f"⚠️  Rate limited. Waiting {wait_time}s... (attempt {attempt+1}/{max_retries})")
                time.sleep(wait_time)

            except TweepyException as e:
                print(f"❌ Error posting tweet: {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(5)

        return None

    def post_thread_from_file(self, file_path):
        """
        Post thread from TWEET X/Y formatted file
        """
        tweets = self._parse_thread_file(file_path)

        if not tweets:
            raise ValueError("No tweets found in file")

        print(f"📝 Found {len(tweets)} tweets in thread")

        # Post thread sequentially
        thread_ids = []
        for i, tweet_text in enumerate(tweets):
            print(f"📤 Posting tweet {i+1}/{len(tweets)}...")

            # First tweet has no reply_to, subsequent tweets reply to previous
            reply_to = thread_ids[-1] if thread_ids else None

            tweet_id = self.post_tweet(tweet_text, reply_to_id=reply_to)

            if tweet_id:
                thread_ids.append(tweet_id)
                print(f"✅ Tweet {i+1} posted: https://twitter.com/i/web/status/{tweet_id}")

                # Delay between tweets to avoid rate limits
                if i < len(tweets) - 1:
                    time.sleep(2)
            else:
                print(f"❌ Failed to post tweet {i+1}")
                return False

        if thread_ids:
            print(f"🎉 Thread posted successfully!")
            print(f"Thread URL: https://twitter.com/i/web/status/{thread_ids[0]}")
            return True

        return False

    def _parse_thread_file(self, file_path):
        """
        Parse TWEET X/Y format from file
        """
        with open(file_path) as f:
            content = f.read()

        import re
        pattern = r'TWEET (\d+)/(\d+):\s*(.*?)(?=TWEET \d+/\d+:|===|$)'
        matches = re.findall(pattern, content, re.DOTALL)

        tweets = []
        for match in matches:
            tweet_num, total, text = match
            clean_text = text.strip()
            if clean_text:
                tweets.append(clean_text)

        return tweets

    def post_with_media(self, text, image_path):
        """
        Post tweet with image using v1.1 API for media upload
        """
        # Upload media using v1.1
        media = self.api_v1.media_upload(image_path)
        media_id = media.media_id

        # Post tweet with media using v2
        response = self.client.create_tweet(
            text=text,
            media_ids=[media_id]
        )

        return response.data['id']
```

### Phase 3: Draft Creation Commands

**New Slash Commands:**

#### `/x-draft` - Create draft from session
```bash
User: /x-draft
Claude:
1. Analyzes current session
2. Generates thread content
3. Saves to x-threads/drafts/YYYY-MM-DD-topic-DRAFT.md
4. Shows draft for review
5. Asks: "Ready to approve? (yes/edit/cancel)"
```

#### `/x-approve` - Convert draft to posting format
```bash
User: /x-approve drafts/2025-10-04-topic-DRAFT.md
Claude:
1. Validates all tweets <280 chars
2. Checks hashtag count
3. Converts to TWEET X/Y format
4. Moves to ready-to-post/
5. Asks: "Ready to post now? (yes/schedule/cancel)"
```

#### `/x-post-draft` - Post approved draft
```bash
User: /x-post-draft ready-to-post/2025-10-04-topic-x7.txt
Claude:
1. Runs x-token-verify.py (ensure fresh tokens)
2. Posts thread via enhanced post_x_thread.py
3. Tracks analytics
4. Archives posted draft
```

### Phase 4: Integration with Existing Commands

**Modify existing commands to use draft workflow:**

```python
# Example: /content-nuke modification
def content_nuke_x_thread_generation():
    """
    Generate X thread for content nuke
    Now saves as DRAFT first
    """
    # 1. Generate thread content
    thread_content = generate_thread_from_session()

    # 2. Save as draft
    draft_path = save_as_draft(thread_content, "content-nuke")

    # 3. Show for review
    print(f"📝 Draft saved: {draft_path}")
    print("Review and approve with: /x-approve {draft_path}")

    # 4. Ask for immediate approval
    response = input("Approve and post now? (yes/review/cancel): ")

    if response == "yes":
        approved_path = approve_draft(draft_path)
        post_draft(approved_path)
    elif response == "review":
        print("Edit draft manually, then run /x-approve when ready")
    else:
        print("Draft saved for later")
```

---

## 🔧 IMPLEMENTATION STEPS

### Step 1: Install Dependencies

```bash
pip install tweepy python-dotenv
```

### Step 2: Migrate to OAuth 1.0a (Permanent Tokens)

**Why:** OAuth 1.0a tokens never expire (unlike OAuth 2.0's 2-hour limit)

**How:**
1. Go to X Developer Portal
2. Regenerate keys with **read + write** permissions
3. Get OAuth 1.0a credentials:
   - Consumer Key (API Key)
   - Consumer Secret (API Secret)
   - Access Token
   - Access Token Secret
4. Store in waygate-mcp/.env:
   ```bash
   X_API_KEY="your_consumer_key"
   X_API_SECRET="your_consumer_secret"
   X_ACCESS_TOKEN="your_access_token"
   X_ACCESS_SECRET="your_access_token_secret"
   ```

### Step 3: Create Enhanced post_x_thread.py

Replace existing with new implementation (see Phase 2 above).

**File:** `/home/jeremy/projects/content-nuke/scripts/post_x_thread_v2.py`

### Step 4: Create Draft Management Scripts

**4a. x-draft-create.py** - Generate drafts from sessions
**4b. x-draft-validate.py** - Validate character limits, formatting
**4c. x-draft-approve.py** - Convert to posting format
**4d. x-draft-post.py** - Post approved drafts

### Step 5: Create New Slash Commands

**Files to create:**
- `~/.claude/commands/x-draft.md`
- `~/.claude/commands/x-approve.md`
- `~/.claude/commands/x-post-draft.md`

### Step 6: Modify Existing Slash Commands

Update these to use draft workflow:
- `/content-nuke` - Save X thread as draft first
- `/blog-single-startai` - Save X thread as draft first
- `/blog-both-x` - Save X thread as draft first
- `/blog-jeremy-x` - Save X thread as draft first
- `/post-x` - Save as draft for single tweets too

### Step 7: Directory Structure

```
/home/jeremy/projects/content-nuke/
├── scripts/
│   ├── post_x_thread.py        # OLD - deprecated
│   ├── post_x_thread_v2.py     # NEW - tweepy based
│   ├── x-draft-create.py       # NEW
│   ├── x-draft-validate.py     # NEW
│   ├── x-draft-approve.py      # NEW
│   └── x-draft-post.py         # NEW
├── x-threads/
│   ├── drafts/                 # Unposted drafts
│   │   ├── YYYY-MM-DD-topic-DRAFT.md
│   │   └── ...
│   ├── ready-to-post/          # Approved, formatted
│   │   ├── YYYY-MM-DD-topic-x7.txt
│   │   └── ...
│   └── posted/                 # Archive
│       ├── YYYY-MM-DD-topic-x7-POSTED.txt
│       └── ...
└── x-posts/                    # Single tweets
    ├── drafts/
    ├── ready-to-post/
    └── posted/
```

---

## 📊 BENEFITS OF THIS ARCHITECTURE

### 1. Draft Workflow
✅ Review before posting (avoid mistakes)
✅ Edit content without re-generating
✅ Batch approval (approve multiple drafts)
✅ Scheduling capability (approve now, post later)

### 2. OAuth 1.0a Migration
✅ Tokens NEVER expire
✅ No more 2-hour refresh cycles
✅ Simpler authentication
✅ More reliable

### 3. Tweepy Integration
✅ Industry-standard library
✅ Built-in rate limit handling
✅ Better error messages
✅ Automatic retries

### 4. Validation Pipeline
✅ Character count validation
✅ Hashtag count enforcement
✅ Thread coherence checking
✅ Format validation

### 5. Error Recovery
✅ Retry logic for failed posts
✅ Rate limit detection and waiting
✅ Clear error messages
✅ Draft preservation on failure

---

## 🚨 CRITICAL DECISIONS NEEDED

### Decision 1: OAuth Migration Strategy

**Option A: Full OAuth 1.0a Migration** (RECOMMENDED)
- Pros: Tokens never expire, simpler
- Cons: Need to regenerate all credentials
- Action: Get new OAuth 1.0a keys from X Developer Portal

**Option B: Keep OAuth 2.0 with auto-refresh**
- Pros: Already implemented, works
- Cons: 2-hour expiration, complexity
- Action: Continue using x-token-automation system

**RECOMMENDATION:** Option A - OAuth 1.0a is superior for automation.

### Decision 2: Tweepy vs Requests

**Option A: Migrate to Tweepy** (RECOMMENDED)
- Pros: Industry standard, better error handling, built-in rate limiting
- Cons: New dependency, need to rewrite post_x_thread.py
- Action: Install tweepy, create post_x_thread_v2.py

**Option B: Keep requests library**
- Pros: No changes needed, already works
- Cons: Manual rate limiting, less robust
- Action: Continue with current implementation

**RECOMMENDATION:** Option A - Tweepy is best practice.

### Decision 3: Draft Workflow Complexity

**Option A: Full Draft System** (RECOMMENDED)
- Pros: Review before posting, edit capability, batch approval
- Cons: More complexity, extra steps
- Action: Implement all 4 draft scripts

**Option B: Minimal Draft System**
- Pros: Simple, fast
- Cons: Less control, harder to edit
- Action: Just save markdown drafts, manual approval

**RECOMMENDATION:** Option A - Full system for production quality.

---

## 📅 IMPLEMENTATION TIMELINE

### Week 1: Foundation
- [ ] Install tweepy
- [ ] Get OAuth 1.0a credentials
- [ ] Create post_x_thread_v2.py
- [ ] Test single tweet posting
- [ ] Test thread posting

### Week 2: Draft System
- [ ] Create draft directory structure
- [ ] Build x-draft-create.py
- [ ] Build x-draft-validate.py
- [ ] Build x-draft-approve.py
- [ ] Build x-draft-post.py

### Week 3: Slash Command Integration
- [ ] Create /x-draft command
- [ ] Create /x-approve command
- [ ] Create /x-post-draft command
- [ ] Modify /content-nuke
- [ ] Modify /blog-single-startai
- [ ] Modify /blog-both-x
- [ ] Modify /blog-jeremy-x
- [ ] Modify /post-x

### Week 4: Testing & Documentation
- [ ] Test all commands end-to-end
- [ ] Document draft workflow
- [ ] Update command bible
- [ ] Create troubleshooting guide

---

## 🎯 SUCCESS METRICS

**System is successful when:**

1. ✅ All drafts validate before posting
2. ✅ Zero "invalid token" errors
3. ✅ Zero character limit violations
4. ✅ 100% thread coherence
5. ✅ <5% failed posts (rate limits)
6. ✅ Draft review time <5 minutes
7. ✅ Post success rate >95%

---

## 🔗 NEXT IMMEDIATE STEPS

1. **DECISION REQUIRED:** Choose OAuth 1.0a or keep OAuth 2.0?
2. **DECISION REQUIRED:** Migrate to tweepy or keep requests?
3. **DECISION REQUIRED:** Full draft system or minimal?

**Once decided, I will:**
1. Implement chosen architecture
2. Create all necessary scripts
3. Update slash commands
4. Test end-to-end
5. Document everything

---

**Ready to proceed? Tell me which options you want and I'll build it! 🚀**

**Last Updated:** October 4, 2025
**Status:** Awaiting Strategic Decisions
