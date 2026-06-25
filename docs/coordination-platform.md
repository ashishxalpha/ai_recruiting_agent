# Multi-Agent Coordination Platform

## High-Level Architecture
The Coordination Platform handles distributed orchestration of multiple agents. `Supervisor` operates strictly on `Goals`, mapping them via the `GoalEngine` into dependency graphs. The `DelegationPlanner` and `DelegationEngine` construct tasks and route them to agents via the `AgentCommunicationBus`. Agents never execute code against each other—they only interact by modifying `SharedContext` and sending `AgentMessage`s over the bus.

```mermaid
graph TD
    Supervisor --> GoalEngine
    GoalEngine --> DelegationPlanner
    DelegationPlanner --> DelegationEngine
    DelegationEngine --> CoordinationStrategy
    CoordinationStrategy --> AgentCommunicationBus
    AgentCommunicationBus --> AgentMailbox
    AgentMailbox --> AgentRuntime
    AgentRuntime --> AgentCommunicationBus
    AgentRuntime --> SharedContext
    Supervisor --> ConsensusEngine
    ConsensusEngine --> ConflictResolver
```

## Entity Relationship Diagram
```mermaid
erDiagram
    Goal {
        uuid id
        string status
    }
    GoalDependency {
        uuid parent_id
        uuid child_id
    }
    DelegationPlan {
        uuid id
        uuid goal_id
    }
    DelegationTask {
        uuid id
        uuid assigned_agent_id
    }
    AgentMessage {
        uuid id
        string type
        uuid sender_id
        uuid recipient_id
        json payload
    }
    SharedContextSnapshot {
        uuid id
        uuid session_id
        string scope
        json state
    }
    AgentContract {
        uuid agent_id
        string availability
        json capabilities
    }

    Goal ||--o{ GoalDependency : defines
    Goal ||--|| DelegationPlan : fulfilled_by
    DelegationPlan ||--o{ DelegationTask : contains
    AgentMessage ||--o{ AgentMailbox : queued_in
```

## Sequence Diagram: Coordination Loop
```mermaid
sequenceDiagram
    participant SUP as Supervisor
    participant GE as GoalEngine
    participant DP as DelegationPlanner
    participant BUS as CommunicationBus
    participant AR as AgentRuntime
    participant CE as ConsensusEngine

    SUP->>GE: Submit Goal
    GE->>DP: Generate Dependency Graph
    DP-->>SUP: DelegationPlan
    SUP->>BUS: Broadcast DelegationTask (Type: COMMAND)
    BUS->>AR: Receive Task via Mailbox
    AR->>AR: Execute Reasoning Loop
    AR->>BUS: Broadcast Result (Type: EVENT)
    BUS->>SUP: Aggregate Results
    SUP->>CE: Evaluate Consensus
    CE-->>SUP: Consensus Achieved
    SUP->>GE: Mark Goal Completed
```

## API Contracts
- `POST /api/v1/coordinator/start`
- `GET /api/v1/coordinator/status`
- `GET /api/v1/coordinator/messages`
- `GET /api/v1/agents/contracts`
