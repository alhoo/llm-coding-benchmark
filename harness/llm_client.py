"""
LLM client for generating code solutions.
"""

import os
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage


class LLMClient:
    """Client for interacting with LLM APIs."""
    
    def __init__(self, model: str, temperature: float = 0.1):
        """
        Initialize LLM client.
        
        Args:
            model: Model name (e.g., "gpt-4-turbo", "claude-3-sonnet-20240229", "gemini-1.5-pro")
            temperature: Sampling temperature
        """
        self.model = model
        self.temperature = temperature
        self.llm = self._create_llm()
    
    def _create_llm(self):
        """Create LLM instance based on model name."""
        if "gpt" in self.model:
            return ChatOpenAI(
                model=self.model,
                temperature=self.temperature,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif "claude" in self.model:
            return ChatAnthropic(
                model=self.model,
                temperature=self.temperature,
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        elif "gemini" in self.model:
            return ChatGoogleGenerativeAI(
                model=self.model,
                temperature=self.temperature,
                api_key=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
            )
        else:
            return ChatOpenAI(
                model=self.model,
                temperature=self.temperature,
                base_url=os.environ.get("OPENAI_BASEURL"),
                api_key=os.getenv("OPENAI_API_KEY")
            )
    
    def generate_solution(
        self,
        problem_statement: str,
        language: str = "python"
    ) -> str:
        """
        Generate code solution for a problem.
        
        Args:
            problem_statement: Complete problem description
            language: Target programming language
            
        Returns:
            Generated code solution
        """
        messages = [
            SystemMessage(content=self._get_system_prompt(language)),
            HumanMessage(content=problem_statement),
        ]

        response = self.llm.invoke(messages)
        
        return response.content
    
    def _get_system_prompt(self, language: str) -> str:
        """Get system prompt for code generation."""
        return f"""You are an expert {language} programmer solving coding problems.

Follow these guidelines:
1. **Read Carefully**: Understand ALL requirements and constraints
2. **Think First**: Consider the optimal algorithm and complexity
3. **Implement Correctly**: Write clean, bug-free code
4. **Handle Edge Cases**: Consider boundary conditions
5. **Optimize**: Prefer efficient algorithms over brute force
6. **Test Mentally**: Trace through examples to verify correctness

Return ONLY the code implementation. No explanations unless requested.
Use clear variable names and follow {language} best practices."""


# Singleton instance
_client: Optional[LLMClient] = None


def get_client(model: str) -> LLMClient:
    """Get or create LLM client singleton."""
    global _client
    if _client is None or _client.model != model:
        _client = LLMClient(model=model)
    return _client
