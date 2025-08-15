#!/bin/bash

echo "=========================================="
echo "SETTING UP TRACING FOR BOB"
echo "=========================================="
echo ""
echo "Choose your setup:"
echo "1) Local Langfuse (Docker) - FREE"
echo "2) Cloud Langfuse - FREE tier available"
echo "3) Simple logging (no external service)"
echo ""
echo "Recommendation: Start with option 3 for immediate results"
echo ""

# For now, use simple logging
cat > traced_agent_simple.py << 'EOF'
#!/usr/bin/env python3
"""
TRACED AGENT - Simple logging version (no external dependencies)
"""

import time
import json
import os
from datetime import datetime
import google.generativeai as genai
from slack_sdk import WebClient

print("=" * 60)
print("TRACED AGENT - With Simple Logging")
print("=" * 60)

# Setup logging
TRACE_FILE = "agent_traces.jsonl"

class SimpleTracedAgent:
    def __init__(self):
        # Gemini
        genai.configure(api_key="AIzaSyDOEAIpqn7qN1LknylLPvTKWU5TnUHBzEo")
        self.model = genai.GenerativeModel('gemini-1.5-flash')

        # Slack
        self.slack = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
        self.bot_id = self.slack.auth_test()["user_id"]
        self.jeremy_id = "U099CBRE7CL"

        # Memory
        self.conversation_history = []
        self.processed = set()

        print(f"✅ Agent initialized with tracing to: {TRACE_FILE}")

        self.slack.chat_postMessage(
            channel="C099A4N4PSN",
            text="📊 Traced Agent Online - Logging all interactions for analysis"
        )

    def log_trace(self, event_type: str, data: dict):
        """Log trace to file"""
        trace = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data
        }

        with open(TRACE_FILE, "a") as f:
            f.write(json.dumps(trace) + "\n")

        # Also print key events
        if event_type in ["user_message", "bot_response", "error"]:
            print(f"[TRACE] {event_type}: {data.get('text', data.get('error', ''))[:100]}")

    def generate_response(self, user_message: str) -> str:
        """Generate response with tracing"""

        start_time = time.time()

        # Log input
        self.log_trace("user_message", {
            "text": user_message,
            "user": "jeremy"
        })

        # Build context
        context = ""
        if self.conversation_history:
            context = "Recent conversation:\\n"
            for hist in self.conversation_history[-3:]:
                context += f"Jeremy: {hist['user']}\\n"
                context += f"You: {hist['bot']}\\n"

        prompt = f"""You are Jeremy's AI assistant.

{context}

Jeremy said: {user_message}

Respond helpfully:"""

        try:
            # Generate
            response = self.model.generate_content(prompt)
            latency = time.time() - start_time

            if response and response.text:
                bot_response = response.text.strip()

                # Log output
                self.log_trace("bot_response", {
                    "text": bot_response,
                    "latency_seconds": latency,
                    "prompt_length": len(prompt),
                    "response_length": len(bot_response)
                })

                # Save to memory
                self.conversation_history.append({
                    'user': user_message[:200],
                    'bot': bot_response[:200],
                    'timestamp': datetime.now().isoformat()
                })

                if len(self.conversation_history) > 10:
                    self.conversation_history = self.conversation_history[-10:]

                return bot_response
            else:
                self.log_trace("error", {"error": "No response generated"})
                return "I couldn't generate a response."

        except Exception as e:
            self.log_trace("error", {"error": str(e)})
            return f"Error: {str(e)[:100]}"

    def run(self):
        """Main loop"""
        print("\\n📊 Agent running with trace logging...")
        print(f"📝 Traces saved to: {TRACE_FILE}")
        print("-" * 60)

        while True:
            try:
                msgs = self.slack.conversations_history(channel="C099A4N4PSN", limit=20)

                for msg in msgs['messages']:
                    ts = msg.get('ts')
                    user = msg.get('user')
                    text = msg.get('text', '')

                    # Only Jeremy's new messages
                    if ts in self.processed or user != self.jeremy_id or user == self.bot_id:
                        continue

                    print(f"\\n📨 Processing: {text[:50]}...")
                    self.processed.add(ts)

                    # Generate and send
                    response = self.generate_response(text)

                    self.slack.chat_postMessage(
                        channel="C099A4N4PSN",
                        text=response
                    )
                    print(f"✅ Responded")

                # Cleanup
                if len(self.processed) > 100:
                    self.processed = set(list(self.processed)[-50:])

                time.sleep(2)

            except KeyboardInterrupt:
                print("\\n👋 Shutting down...")
                self.log_trace("shutdown", {"reason": "user_interrupt"})
                break
            except Exception as e:
                print(f"Loop error: {e}")
                self.log_trace("error", {"error": f"Loop error: {str(e)}"})
                time.sleep(5)

if __name__ == "__main__":
    agent = SimpleTracedAgent()
    agent.run()
EOF

echo "✅ Created traced_agent_simple.py"
echo ""
echo "To run with tracing:"
echo "  python3 traced_agent_simple.py"
echo ""
echo "To view traces:"
echo "  tail -f agent_traces.jsonl | jq ."
echo ""
echo "For production tracing with Langfuse:"
echo "  docker run -d -p 3000:3000 langfuse/langfuse"
echo "  Then set LANGFUSE_HOST=http://localhost:3000"
