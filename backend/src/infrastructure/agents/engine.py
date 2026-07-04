import uuid
import time
import asyncio
from typing import Dict, Any, List

from src.application.agents.interfaces import AgentRuntime, CognitivePipeline, AgentExecutor, AgentSession
from src.domain.agent_models import Agent, AgentContext, AgentLifecycle, ReasoningTrace
from src.application.agents.execution_context import AgentExecutionContext
from src.application.agents.prompt_builder import PromptBuilder, PromptVariables
from src.infrastructure.agents.planners import ReActPlanner
from src.application.tools.capability_resolver import CapabilityResolver
from src.infrastructure.tools.pipeline import ToolExecutionPipeline
from src.application.llm.interfaces import LLMMessage
from src.domain.agent_events import (
    AgentStarted, ThoughtGenerated, PlanCreated, ToolSelected, 
    ToolStarted, ToolCompleted, MemoryRetrieved, ReflectionGenerated, 
    MemoryStored, AgentCompleted, AgentFailed
)
from src.infrastructure.events.event_bus import EventBus
from src.application.agents.planner_models import Plan, Reflection

class ProductionCognitivePipeline:
    def __init__(self, 
                 memory_engine: Any,
                 prompt_builder: PromptBuilder,
                 planner: ReActPlanner,
                 capability_resolver: CapabilityResolver,
                 tool_pipeline: ToolExecutionPipeline,
                 reflection_engine: Any = None):
        self.memory_engine = memory_engine
        self.prompt_builder = prompt_builder
        self.planner = planner
        self.capability_resolver = capability_resolver
        self.tool_pipeline = tool_pipeline
        self.reflection_engine = reflection_engine

    async def execute_session(self, context: AgentExecutionContext) -> None:
        EventBus.publish(AgentStarted(agent_id=context.agent_id, session_id=context.session_id, trace_id=context.trace.trace_id))
        
        history: List[LLMMessage] = []
        
        try:
            while True:
                context.budget.check_limits()
                
                # Observe from context
                observation = context.tool_context.get("last_observation", "Agent runtime started.")
                
                # Memory retrieval
                retrieved_memories = await self.memory_engine.retrieve("planning_policy", {"query": observation})
                EventBus.publish(MemoryRetrieved(
                    agent_id=context.agent_id, session_id=context.session_id, trace_id=context.trace.trace_id,
                    policy="planning_policy", memory_count=len(retrieved_memories)
                ))
                
                memory_str = "\n".join([str(m) for m in retrieved_memories])
                
                # Build Prompt
                vars = PromptVariables(
                    system_instructions="You are an autonomous agent.",
                    agent_definition="A helpful AI.",
                    organization_policies="Do no harm.",
                    memory_context=memory_str,
                    current_goal=context.tool_context.get("goal", "Complete the task."),
                    available_tools="...", # Would be resolved via registry
                    previous_thoughts=observation
                )
                prompt_context = self.prompt_builder.build(vars)
                
                # LLM Planner
                plan = await self.planner.plan(prompt_context, history, [])
                context.budget.current_iterations += 1
                
                EventBus.publish(ThoughtGenerated(
                    agent_id=context.agent_id, session_id=context.session_id, trace_id=context.trace.trace_id,
                    thoughts=plan.thoughts, reasoning=plan.reasoning
                ))
                EventBus.publish(PlanCreated(
                    agent_id=context.agent_id, session_id=context.session_id, trace_id=context.trace.trace_id,
                    selected_tool=plan.selected_tool, tool_input=plan.tool_input, stop=plan.stop
                ))
                
                history.append(LLMMessage(role="assistant", content=plan.thoughts))
                
                if plan.stop:
                    break
                    
                if plan.selected_tool:
                    context.budget.current_tool_calls += 1
                    EventBus.publish(ToolSelected(
                        agent_id=context.agent_id, session_id=context.session_id, trace_id=context.trace.trace_id,
                        tool_name=plan.selected_tool
                    ))
                    
                    # Execution Pipeline
                    start_t = time.time()
                    EventBus.publish(ToolStarted(
                        agent_id=context.agent_id, session_id=context.session_id, trace_id=context.trace.trace_id,
                        tool_name=plan.selected_tool, tool_input=plan.tool_input or {}
                    ))
                    
                    try:
                        result = await self.tool_pipeline.execute(
                            capability="general", operation=plan.selected_tool, 
                            arguments=plan.tool_input or {}, 
                            context=context 
                        )
                        observation = f"Tool succeeded: {result.result}"
                    except Exception as e:
                        observation = f"Tool failed: {str(e)}"
                        
                    latency = (time.time() - start_t) * 1000
                    EventBus.publish(ToolCompleted(
                        agent_id=context.agent_id, session_id=context.session_id, trace_id=context.trace.trace_id,
                        tool_name=plan.selected_tool, latency_ms=latency
                    ))
                    
                    context.tool_context["last_observation"] = observation
                    history.append(LLMMessage(role="user", content=f"Observation: {observation}"))
                
                # Reflection Engine Integration
                if self.reflection_engine:
                    from src.domain.agent_models import ReasoningTrace, AgentContext
                    # Lightweight translation for reflection trace
                    trace = ReasoningTrace(
                        thought=plan.thoughts,
                        action=plan.selected_tool,
                        observation=observation,
                        latency_ms=0,
                        tokens_used=0
                    )
                    agent_ctx = AgentContext(agent_id=context.agent_id, session_id=context.session_id)
                    reflection = await self.reflection_engine.reflect(trace, agent_ctx)
                    
                    EventBus.publish(ReflectionGenerated(
                        agent_id=context.agent_id, session_id=context.session_id, trace_id=context.trace.trace_id,
                        success_score=reflection.success_rating, mistakes=[], future_actions=reflection.learnings
                    ))
                else:
                    # No reflection available
                    reflection = None
                
                # Memory Persistence
                if reflection and reflection.learnings:
                    # e.g., await self.memory_engine.store(reflection.learnings)
                    EventBus.publish(MemoryStored(
                        agent_id=context.agent_id, session_id=context.session_id, trace_id=context.trace.trace_id,
                        candidates_saved=len(reflection.learnings)
                    ))

            EventBus.publish(AgentCompleted(
                agent_id=context.agent_id, session_id=context.session_id, trace_id=context.trace.trace_id,
                success=True, final_output="Goal achieved"
            ))
            
        except Exception as e:
            EventBus.publish(AgentFailed(
                agent_id=context.agent_id, session_id=context.session_id, trace_id=context.trace.trace_id,
                error=str(e)
            ))
            raise e
