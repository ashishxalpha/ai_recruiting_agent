import json
from typing import List, Dict, Any, Optional

from src.application.llm.interfaces import LLMProvider, LLMRequest, LLMMessage
from src.application.agents.planner_models import Plan
from src.application.agents.prompt_builder import PromptContext

class ReActPlanner:
    """Production ReAct planner that uses LLM function calling to select tools."""
    
    def __init__(self, llm_provider: LLMProvider):
        self.llm = llm_provider
        
    async def plan(self, prompt_context: PromptContext, history: List[LLMMessage], available_tools: List[Dict[str, Any]]) -> Plan:
        """
        Executes a planning step and returns a Plan object.
        Uses OpenAI-style function calling for structured output.
        """
        
        # We define the 'submit_plan' function that the LLM must call
        plan_schema = {
            "type": "function",
            "function": {
                "name": "submit_plan",
                "description": "Submit your plan of action.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "thoughts": {"type": "string", "description": "Internal monologue"},
                        "reasoning": {"type": "string", "description": "Logical steps"},
                        "selected_tool": {"type": "string", "description": "Tool name to execute next"},
                        "tool_input": {"type": "object", "description": "Arguments for the tool"},
                        "stop": {"type": "boolean", "description": "True if goal achieved"},
                        "confidence": {"type": "number", "description": "Confidence score 0.0-1.0"}
                    },
                    "required": ["thoughts", "reasoning", "stop", "confidence"]
                }
            }
        }
        
        # All available tools are passed to the LLM so it knows what it can select,
        # but the LLM MUST use 'submit_plan' to actually return its decision.
        tools_for_llm = [plan_schema]
        
        # We can also add actual tools to `tools_for_llm` if we want the LLM to call them directly,
        # but following the ReAct pattern where the LLM just returns a plan with `selected_tool`,
        # providing the tool descriptions in the prompt or as schema is sufficient.
        # For structured tool selection, we just let the LLM return the name in submit_plan.
        
        messages = [
            LLMMessage(role="system", content=prompt_context.rendered_prompt),
            *history
        ]
        
        request = LLMRequest(
            messages=messages,
            model=prompt_context.model,
            temperature=prompt_context.temperature,
            top_p=prompt_context.top_p,
            seed=prompt_context.seed,
            tools=tools_for_llm,
            tool_choice={"type": "function", "function": {"name": "submit_plan"}}
        )
        
        response = await self.llm.generate(request)
        
        if response.tool_calls:
            tc = response.tool_calls[0]
            if tc.function_name == "submit_plan":
                args = json.loads(tc.function_arguments)
                return Plan(
                    thoughts=args.get("thoughts", ""),
                    reasoning=args.get("reasoning", ""),
                    selected_tool=args.get("selected_tool"),
                    tool_input=args.get("tool_input"),
                    stop=args.get("stop", False),
                    confidence=args.get("confidence", 1.0)
                )
                
        # Fallback if the LLM didn't use the tool properly
        return Plan(
            thoughts="Failed to parse LLM structured output.",
            reasoning="Fallback due to parsing error.",
            stop=True,
            confidence=0.0
        )

class TreeOfThoughtPlanner:
    """Tree of Thoughts planner is a future capability."""
    def __init__(self, llm_provider: LLMProvider):
        pass

    async def plan(self, *args, **kwargs):
        raise NotImplementedError("feature_available: false")

class GraphOfThoughtPlanner:
    """Graph of Thoughts planner is a future capability."""
    def __init__(self, llm_provider: LLMProvider):
        pass

    async def plan(self, *args, **kwargs):
        raise NotImplementedError("feature_available: false")

