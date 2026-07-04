from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class Plan(BaseModel):
    thoughts: str = Field(description="The agent's internal monologue and observations.")
    reasoning: str = Field(description="The logical steps leading to the current decision.")
    selected_tool: Optional[str] = Field(default=None, description="The name of the tool to execute next, if any.")
    tool_input: Optional[Dict[str, Any]] = Field(default=None, description="The arguments to pass to the selected tool.")
    stop: bool = Field(default=False, description="True if the agent has achieved its goal and should stop.")
    confidence: float = Field(default=1.0, description="The agent's confidence in this plan (0.0 to 1.0).")
    
class Reflection(BaseModel):
    success_score: float = Field(description="Score from 0.0 to 1.0 evaluating the overall success of the session.")
    mistakes: List[str] = Field(description="Mistakes made during the execution.", default_factory=list)
    tool_effectiveness: Dict[str, float] = Field(description="Rating of how effective each tool was.", default_factory=dict)
    knowledge_candidates: List[str] = Field(description="Extracted generalized knowledge to be saved.", default_factory=list)
    memory_candidates: List[str] = Field(description="Specific episodic or semantic memory candidates to persist.", default_factory=list)
    future_actions: List[str] = Field(description="Recommendations for future executions.", default_factory=list)
