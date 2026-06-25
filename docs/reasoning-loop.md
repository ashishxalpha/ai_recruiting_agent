# Cognitive Pipeline (Reasoning Loop)

## Overview
Every iteration of an agent's execution is governed by the `CognitivePipeline`. It forces a strict procedural reasoning state machine, yielding a complete `ReasoningTrace`.

## Sequence Diagram
```mermaid
sequenceDiagram
    participant Pipeline as CognitivePipeline
    participant ME as MemoryEngine
    participant P as Planner
    participant AE as AgentExecutor
    participant RE as ReflectionEngine

    Pipeline->>Pipeline: Observe (Environment/Events)
    Pipeline->>ME: Retrieve (AgentMemoryScope)
    ME-->>Pipeline: Memory Context
    Pipeline->>Pipeline: Reason (Synthesize context)
    Pipeline->>P: Plan (Observation, Context)
    P-->>Pipeline: AgentDecision / AgentPlan
    Pipeline->>AE: Execute (Action/Tool)
    AE-->>Pipeline: AgentObservation (Result)
    Pipeline->>RE: Reflect (Trace)
    RE-->>Pipeline: AgentReflection
    Pipeline->>ME: Learn (Store Episodic/Working Memory)
```

## Explanation of Stages
1. **Observe**: Intake environmental events, active tasks, or workflow statuses.
2. **Retrieve**: Ask `MemoryEngine` for semantic/procedural memory restricted by `AgentMemoryScope`.
3. **Reason**: Assemble internal thoughts.
4. **Plan**: Planner dictates the next sequence.
5. **Execute**: `AgentExecutor` fires the tool or triggers a state update.
6. **Reflect**: Evaluate if the executed action achieved the goal.
7. **Learn**: Update `WorkingMemory` and persist `SessionSnapshots`.
