# Utilizing the X (Twitter) API: Code Examples and Best Practices

**Created:** 2025-10-04
**Purpose:** Reference guide for X API integration with slash commands

---

## Authentication Setup

The X API v2 requires developer account at [developer.x.com](https://developer.x.com) with **read + write permissions**. Free tier allows up to 1,500 posts/month.

### OAuth 1.0a User Context (Required for Write Operations)

```python
import os
import tweepy

# Load credentials from environment variables
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# Create the client
client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)
```

**Best Practice:** Use environment variables or secrets manager (e.g., `python-dotenv`) to store keys. Never hardcode credentials!

---

## Creating a Simple Post (Tweet)

```python
try:
    response = client.create_tweet(
        text="Hello, world! This is a test tweet from X API v2. #Python #Automation"
    )
    print(f"Tweet posted successfully! ID: {response.data['id']}")
except tweepy.TweepyException as e:
    print(f"Error posting tweet: {e}")
```

### Best Practices for Creating Posts

- **Character Limit:** Tweets limited to 280 characters. Always check `len(text) <= 280`
- **Rate Limits:**
  - Free tier: 50 posts/24 hours (app-level)
  - 1,500/month (user-level)
  - Use `wait_on_rate_limit=True` in client for automatic retries
- **Error Handling:** Wrap calls in try-except blocks to catch `TweepyException`
- **Content Guidelines:**
  - Follow X's automation rules
  - No spam
  - Disclose bots if automated
  - Avoid repetitive posts
- **Validation:** Sanitize user input (strip HTML, escape quotes)

---

## Creating a Post with Media (Image)

Media uploads use legacy v1.1 API, then attach to v2 tweet.

```python
# Step 1: Upload media using v1.1 API
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret,
    access_token, access_token_secret
)
api_v1 = tweepy.API(auth)

try:
    # Upload image
    media = api_v1.media_upload('path/to/image.jpg')
    media_id = media.media_id

    # Step 2: Create tweet with media using v2
    response = client.create_tweet(
        text="Check out this cool image! #XAPI",
        media_ids=[media_id]
    )
    print(f"Tweet with image posted! ID: {response.data['id']}")
except tweepy.TweepyException as e:
    print(f"Error: {e}")
```

### Best Practices for Media

- **File Specs:**
  - Images: JPG/PNG/GIF, <5MB
  - Videos: MP4/MOV, <512MB, ≤2:20 duration
- **Upload First:** Always upload media separately and get `media_id` before attaching
- **Multiple Media:** Up to 4 images per tweet; use `media_ids=[id1, id2, ...]`
- **Cleanup:** Delete unused media IDs via API to free quota

---

## Creating a Thread (Multi-Post Sequence)

Threads created by posting sequentially and replying to previous tweet's ID.

```python
def create_thread(client, texts):
    thread_id = None
    for i, text in enumerate(texts):
        try:
            if i == 0:
                # First tweet
                response = client.create_tweet(text=text)
            else:
                # Reply to previous
                response = client.create_tweet(
                    text=text,
                    in_reply_to_tweet_id=thread_id
                )
            thread_id = response.data['id']
            print(f"Tweet {i+1} posted! ID: {thread_id}")
        except tweepy.TweepyException as e:
            print(f"Error in thread: {e}")
            break

# Example usage
thread_texts = [
    "Thread starter: This is tweet 1/3. #Thread",
    "Tweet 2/3: More details here.",
    "Tweet 3/3: End of thread!"
]
create_thread(client, thread_texts)
```

### Best Practices for Threads

- **Sequential Posting:** Post one-by-one to build the chain
- **Numbering:** Include "1/3", "2/3" in text for clarity
- **Limits:** Same as single posts; space them out to avoid rate limits
- **Delay Between Posts:** Add 2-second delay to avoid rate limits

---

## Editing a Post

Use `create_tweet` with `edit_options` to update existing tweet (within 1 hour, up to 5 edits).

```python
try:
    response = client.create_tweet(
        text="Updated tweet: I fixed a typo!",
        edit_options={
            'previous_post_id': '1234567890123456789'
        }
    )
    print(f"Tweet edited! New ID: {response.data['id']}")
except tweepy.TweepyException as e:
    print(f"Edit failed: {e}")
```

### Best Practices for Edits

- **Time Window:** Only editable within 60 minutes of original post
- **Visibility:** Edits show a badge; original text viewable via API
- **Avoid Overuse:** Edits count toward rate limits

---

## Draft Functionality

**IMPORTANT:** X API v2 **does NOT support creating or saving drafts programmatically**. The `POST /2/tweets` endpoint only creates published posts.

Drafts are a UI-only feature in X app/web composer.

### Workarounds for Draft-Like Functionality

#### 1. Local Storage
Save draft text in your app's database/file and post later via scheduled job.

```python
import json

def save_draft(text, filename='drafts.json'):
    try:
        with open(filename, 'r+') as f:
            drafts = json.load(f)
    except FileNotFoundError:
        drafts = []

    drafts.append({
        'text': text,
        'timestamp': '2025-10-05T12:00:00Z'
    })

    with open(filename, 'w') as f:
        json.dump(drafts, f)

# Usage
save_draft("This is my draft tweet.")
```

#### 2. Third-Party Tools
Use services like Buffer or Typefully (integrate via their APIs) for scheduling/drafts.

#### 3. File-Based Draft System
Store drafts as markdown files in organized directory structure.

```
x-threads/drafts/
├── YYYY-MM-DD-topic-DRAFT.md
├── YYYY-MM-DD-another-topic-DRAFT.md
└── ready-to-post/
    └── YYYY-MM-DD-approved.txt
```

---

## Rate Limits & Error Handling

### Rate Limit Structure
- **App-level:** 50 posts/24 hours
- **User-level:** 1,500 posts/month
- **Thread posting:** 2-second delay recommended between tweets

### Error Handling Pattern

```python
import time
from tweepy.errors import TweepyException, TooManyRequests

def post_with_retry(client, text, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.create_tweet(text=text)
            return response.data['id']
        except TooManyRequests:
            wait_time = 60 * (attempt + 1)
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
        except TweepyException as e:
            print(f"Error: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(5)
    return None
```

---

## API References

- **Create Tweet Endpoint:** [Official Docs](https://developer.x.com/en/docs/twitter-api/tweets/manage-tweets/api-reference/post-tweets)
- **Developer Portal:** [developer.x.com](https://developer.x.com)
- **Tweepy Documentation:** [docs.tweepy.org](https://docs.tweepy.org)

---

**Last Updated:** October 4, 2025
**Status:** Reference Document
