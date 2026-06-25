# Organization Architecture

## High-Level Architecture
The `RecruitingOrganization` is an implementation of an `OrganizationPlugin`. It sits atop the execution-scoped `AIKernel`, mapping high-level HR goals into discrete `AgentSkills` assigned to `OrganizationRoles`. 

```mermaid
graph TD
    Client --> OrganizationFacade
    OrganizationFacade --> OrganizationPlugin
    OrganizationPlugin --> OrganizationPolicyEngine
    OrganizationPlugin --> GoalEngine
    GoalEngine --> SkillDependencyGraph
    SkillDependencyGraph --> SkillPipeline
    SkillPipeline --> LocalExecution
    SkillPipeline --> CoordinationPlatform
    LocalExecution --> AIKernel
    CoordinationPlatform --> AIKernel
    AIKernel --> MemoryEngine
    AIKernel --> ToolPlatform
    AIKernel --> WorkflowEngine
```

## Entity Relationship Diagram
```mermaid
erDiagram
    OrganizationPlugin {
        uuid id
        string name
    }
    OrganizationConfiguration {
        json enabled_roles
        json enabled_skills
        json execution_budgets
    }
    GoalTemplate {
        uuid id
        string name
        json workflow_structure
    }
    OrganizationRole {
        uuid id
        string title
        json assigned_skills
    }
    AgentSkill {
        uuid id
        string name
    }
    SkillContract {
        json input_schema
        json output_schema
        json dependencies
        json required_tools
        json required_memory
    }
    SkillDependencyGraph {
        uuid graph_id
        json execution_order
    }

    OrganizationPlugin ||--|| OrganizationConfiguration : configured_by
    OrganizationRole ||--o{ AgentSkill : performs
    AgentSkill ||--|| SkillContract : exposes
    AgentSkill ||--o{ SkillDependencyGraph : mapped_in
    GoalTemplate ||--o{ SkillDependencyGraph : utilizes
```

## Sequence Diagram: Goal Execution
```mermaid
sequenceDiagram
    participant User
    participant OF as OrganizationFacade
    participant GE as GoalEngine
    participant SP as SkillPipeline
    participant CP as CoordinationPlatform
    participant AIK as AIKernel(Local Execution)
    participant LL as LearningLoop

    User->>OF: Submit OrganizationGoal
    OF->>GE: Parse against GoalTemplate
    GE->>SP: Resolve SkillDependencyGraph
    SP->>SP: Determine Execution Mode
    
    alt Local (Sequential)
        SP->>AIK: Execute Skill (ParseResume)
        AIK-->>SP: Result
    else Distributed / Parallel
        SP->>CP: Delegate Tasks across Roles
        CP-->>SP: Aggregated Result
    end
    
    SP->>LL: Trigger Reflection & Metrics
    LL->>LL: Update Memory & Skill Metrics
    LL-->>User: Goal Completed
```

## API Contracts
- `POST /api/v1/organization/goals`
- `GET /api/v1/organization/skills`
- `GET /api/v1/organization/metrics`
