#!/usr/bin/env python3
"""
Multi-AI Consultant System
Bob routes queries to the best AI expert: Claude, Gemini, or Local models
"""

import subprocess
from typing import Dict, Any


class MultiAIConsultant:
    def __init__(self):
        self.claude_cli = "claude-code"
        self.gemini_cli = "gemini"

    def route_query(self, query: str, context: Dict[str, Any]) -> str:
        """Intelligently route queries to the best AI system"""

        query_lower = query.lower()

        # CLAUDE EXPERT - Complex reasoning, architecture, business strategy
        if any(
            keyword in query_lower
            for keyword in [
                "architecture",
                "strategy",
                "business model",
                "scaling",
                "should i",
                "recommend",
                "analyze",
                "optimize",
                "complex",
                "planning",
                "decision",
            ]
        ):
            return self.consult_claude(query, context)

        # GEMINI EXPERT - Multimodal, research, Google services, math
        elif any(
            keyword in query_lower
            for keyword in [
                "image",
                "photo",
                "document",
                "pdf",
                "research",
                "google",
                "sheets",
                "drive",
                "search web",
                "calculate",
                "math",
                "data analysis",
                "chart",
            ]
        ):
            return self.consult_gemini(query, context)

        # CODE GENERATION - Local qwen2.5-coder (fast & free)
        elif any(
            keyword in query_lower
            for keyword in [
                "code",
                "script",
                "python",
                "javascript",
                "write",
                "function",
                "class",
                "debug",
                "fix",
            ]
        ):
            return self.local_coding_response(query)

        # QUICK QUESTIONS - Local gemma:2b (instant)
        elif len(query.split()) < 10:
            return self.quick_local_response(query)

        # DEFAULT - Local reasoning
        else:
            return self.local_reasoning_response(query)

    def consult_claude(self, query: str, context: Dict[str, Any]) -> str:
        """Expert consultation with Claude"""

        prompt = f"""
        Hi Claude! This is Bob, Jeremy's AI assistant.

        Project Context:
        - DiagnosticPro: 90% complete repair industry platform
        - Goal: Global repair and maintenance institution
        - Live URL: https://diagnosticpro-mvp-970547573997.us-central1.run.app
        - Jeremy: Non-coder, project manager, needs technical guidance

        Current Project Status: {context.get('current_projects', {})}

        Jeremy's Expert Consultation: {query}

        Please provide strategic technical guidance as Jeremy's senior advisor.
        """

        try:
            result = subprocess.run(
                [self.claude_cli, "--message", prompt],
                capture_output=True,
                text=True,
                timeout=180,
            )

            if result.returncode == 0:
                return f"🧠 Claude Expert Analysis:\n\n{result.stdout.strip()}"
            else:
                return f"Claude consultation error: {result.stderr}"

        except Exception as e:
            return f"Could not reach Claude: {e}"

    def consult_gemini(self, query: str, context: Dict[str, Any]) -> str:
        """Gemini consultation for multimodal & research tasks"""

        prompt = f"""
        Context: You're helping Jeremy with his DiagnosticPro project.
        Project: Global repair and maintenance platform (90% complete)
        Jeremy's role: Non-technical project manager

        Task: {query}

        Please provide practical guidance for Jeremy's business needs.
        """

        try:
            result = subprocess.run(
                [self.gemini_cli, "--prompt", prompt],
                capture_output=True,
                text=True,
                timeout=120,
            )

            if result.returncode == 0:
                return f"🤖 Gemini Analysis:\n\n{result.stdout.strip()}"
            else:
                return f"Gemini consultation error: {result.stderr}"

        except Exception as e:
            return f"Could not reach Gemini: {e}"

    def local_coding_response(self, query: str) -> str:
        """Local coding model response"""
        # Implementation for qwen2.5-coder local model
        return (
            f"💻 Code Generation (Local qwen2.5-coder):\n\n[Code response for: {query}]"
        )

    def quick_local_response(self, query: str) -> str:
        """Quick local response using gemma:2b"""
        # Implementation for gemma:2b local model
        return f"⚡ Quick Response: [Fast answer for: {query}]"

    def local_reasoning_response(self, query: str) -> str:
        """Local reasoning using mistral:7b"""
        # Implementation for mistral:7b local model
        return f"🤔 Local Analysis: [Reasoning for: {query}]"


# Example usage
if __name__ == "__main__":
    consultant = MultiAIConsultant()

    # Test queries
    test_queries = [
        "Should I expand DiagnosticPro internationally?",  # → Claude
        "Analyze this screenshot of my analytics",  # → Gemini
        "Write a Python health check script",  # → Local qwen2.5-coder
        "What's 2+2?",  # → Local gemma:2b
        "Explain quantum computing",  # → Local mistral:7b
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        response = consultant.route_query(query, {})
        print(f"Response: {response[:100]}...")
