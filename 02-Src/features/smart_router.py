"""
Smart Router with Complexity Estimation
Routes questions to optimal LLM provider based on complexity
Integrates: Local Ollama + Groq (free) + Google Gemini + Anthropic Claude
"""

import logging
import os
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class SmartRouter:
    """
    Estimates question complexity and routes to optimal provider.

    Routing strategy:
    - Complexity < 0.2: Local Ollama (TinyLlama) - Free, ultra-fast
    - Complexity 0.2-0.7: Groq (Llama 3.1 70B) - Free tier, excellent quality
    - Complexity > 0.7: Google Gemini or Claude - Best quality
    """

    def __init__(self):
        self.ollama_available = self._check_ollama()
        self.groq_available = bool(os.getenv("GROQ_API_KEY"))
        self.cost_tracker = []

    def _check_ollama(self) -> bool:
        """Check if Ollama is running locally"""
        try:
            import requests
            base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            response = requests.get(f"{base}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False

    def estimate_complexity(self, prompt: str) -> float:
        """
        Estimate prompt complexity (0-1 scale)

        Based on:
        - Length: Longer prompts more complex
        - Keywords: Technical/complex words increase score
        - Code presence: Code snippets increase complexity
        - Task type: Questions vs creative vs analysis

        Returns: Float between 0.0 and 1.0
        """
        score = 0.0
        prompt_lower = prompt.lower()

        # 1. Length factor (0-0.5)
        length = len(prompt)
        if length < 100:
            score += 0.1
        elif length < 500:
            score += 0.3
        else:
            score += 0.5

        # 2. Complex keywords (+0.05 each, max 0.3)
        complex_words = [
            'analyze', 'design', 'implement', 'refactor', 'architect',
            'optimize', 'debug', 'complex', 'algorithm', 'architecture',
            'compare', 'evaluate', 'critique', 'synthesize'
        ]
        complex_count = sum(1 for word in complex_words if word in prompt_lower)
        score += min(complex_count * 0.05, 0.3)

        # 3. Simple keywords (-0.05 each, max -0.2)
        simple_words = ['what is', 'who is', 'define', 'list', 'summarize', 'tell me']
        simple_count = sum(1 for word in simple_words if word in prompt_lower)
        score -= min(simple_count * 0.05, 0.2)

        # 4. Code detection (0-0.3)
        if '```' in prompt or 'def ' in prompt or 'function ' in prompt or 'class ' in prompt:
            score += 0.3
        elif 'code' in prompt_lower or 'script' in prompt_lower:
            score += 0.1

        # 5. Task type adjustment
        if '?' in prompt:
            score -= 0.1  # Questions are typically simpler
        if any(word in prompt_lower for word in ['create', 'generate', 'write', 'build']):
            score += 0.2  # Creative/generation tasks harder

        # Normalize to 0-1
        return max(0.0, min(1.0, score))

    def select_provider(self, complexity: float, force_provider: Optional[str] = None) -> Dict:
        """
        Select optimal provider based on complexity.

        Args:
            complexity: Estimated complexity (0-1)
            force_provider: Override automatic selection

        Returns:
            Dict with provider, model, reasoning, estimated_cost
        """
        if force_provider:
            return self._get_provider_config(force_provider, complexity)

        # Route based on complexity
        if complexity < 0.2 and self.ollama_available:
            # Ultra-simple: Local TinyLlama (free, fast)
            return {
                'provider': 'ollama',
                'model': 'tinyllama',
                'reasoning': f'Simple question (complexity {complexity:.2f}) - using free local TinyLlama',
                'estimated_cost': 0.0
            }

        elif complexity < 0.7 and self.groq_available:
            # Most questions: Groq Llama 3.1 70B (free tier, excellent)
            return {
                'provider': 'groq',
                'model': 'llama-3.1-70b-versatile',
                'reasoning': f'Medium complexity (complexity {complexity:.2f}) - using Groq (free tier)',
                'estimated_cost': 0.0
            }

        elif complexity < 0.8:
            # Complex: Google Gemini (cheap, excellent)
            return {
                'provider': 'google',
                'model': os.getenv('MODEL', 'gemini-2.0-flash'),
                'reasoning': f'Complex task (complexity {complexity:.2f}) - using Gemini ($0.01/1M)',
                'estimated_cost': 0.00001  # ~$0.01 per 1M tokens
            }

        else:
            # Ultra-complex: Claude (expensive, best)
            return {
                'provider': 'anthropic',
                'model': 'claude-3-5-sonnet-20240620',
                'reasoning': f'Very complex (complexity {complexity:.2f}) - using Claude ($3/1M)',
                'estimated_cost': 0.00003  # ~$3 per 1M tokens
            }

    def _get_provider_config(self, provider: str, complexity: float) -> Dict:
        """Get configuration for a specific provider"""
        configs = {
            'ollama': {
                'provider': 'ollama',
                'model': 'tinyllama',
                'reasoning': f'Forced local Ollama (complexity {complexity:.2f})',
                'estimated_cost': 0.0
            },
            'groq': {
                'provider': 'groq',
                'model': 'llama-3.1-70b-versatile',
                'reasoning': f'Forced Groq (complexity {complexity:.2f})',
                'estimated_cost': 0.0
            },
            'google': {
                'provider': 'google',
                'model': os.getenv('MODEL', 'gemini-2.0-flash'),
                'reasoning': f'Forced Google Gemini (complexity {complexity:.2f})',
                'estimated_cost': 0.00001
            },
            'anthropic': {
                'provider': 'anthropic',
                'model': 'claude-3-5-sonnet-20240620',
                'reasoning': f'Forced Anthropic Claude (complexity {complexity:.2f})',
                'estimated_cost': 0.00003
            }
        }
        return configs.get(provider, configs['google'])

    def route(self, prompt: str, force_provider: Optional[str] = None) -> Dict:
        """
        Main routing method: estimate complexity and select provider.

        Args:
            prompt: User's question/prompt
            force_provider: Optional provider override

        Returns:
            Dict with provider, model, complexity, reasoning, estimated_cost
        """
        complexity = self.estimate_complexity(prompt)
        provider_config = self.select_provider(complexity, force_provider)

        result = {
            'complexity': complexity,
            **provider_config
        }

        logger.info(f"Routed request: complexity={complexity:.2f}, provider={provider_config['provider']}")
        return result

    def get_status(self) -> Dict:
        """Get router status and available providers"""
        return {
            'ollama_available': self.ollama_available,
            'groq_available': self.groq_available,
            'google_available': bool(os.getenv('GOOGLE_API_KEY')),
            'anthropic_available': bool(os.getenv('ANTHROPIC_API_KEY')),
            'total_requests': len(self.cost_tracker),
            'total_cost': sum(self.cost_tracker)
        }

    def track_cost(self, cost: float):
        """Track actual request cost"""
        self.cost_tracker.append(cost)
