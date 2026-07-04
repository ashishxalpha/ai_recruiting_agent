from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import datetime

class PromptVariables(BaseModel):
    system_instructions: str
    agent_definition: str
    organization_policies: str
    memory_context: str
    current_goal: str
    available_tools: str
    previous_thoughts: str

class PromptContext(BaseModel):
    prompt_version: str
    template_version: str
    variables: PromptVariables
    rendered_prompt: str
    model: str
    temperature: float
    top_p: float
    seed: Optional[int]

class PromptTemplate(BaseModel):
    version: str
    template_text: str
    
    def render(self, variables: PromptVariables) -> str:
        # A simple string format or jinja2 replacement
        return self.template_text.format(
            system_instructions=variables.system_instructions,
            agent_definition=variables.agent_definition,
            organization_policies=variables.organization_policies,
            memory_context=variables.memory_context,
            current_goal=variables.current_goal,
            available_tools=variables.available_tools,
            previous_thoughts=variables.previous_thoughts
        )

class PromptBuilder:
    def __init__(self, default_template: PromptTemplate, model: str = "gpt-4o"):
        self.default_template = default_template
        self.model = model

    def build(self, variables: PromptVariables, overrides: Dict[str, Any] = None) -> PromptContext:
        template = self.default_template
        rendered = template.render(variables)
        
        return PromptContext(
            prompt_version=f"v{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            template_version=template.version,
            variables=variables,
            rendered_prompt=rendered,
            model=overrides.get("model", self.model) if overrides else self.model,
            temperature=overrides.get("temperature", 0.0) if overrides else 0.0,
            top_p=overrides.get("top_p", 1.0) if overrides else 1.0,
            seed=overrides.get("seed", None) if overrides else None
        )
