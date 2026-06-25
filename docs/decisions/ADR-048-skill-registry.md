# ADR 048: Skill Registry & Contracts

## Context
Functions cannot be haphazardly executed. We need strict safety boundaries regarding cost, required permissions, memory contexts, and schemas.

## Decision
We introduce the `AgentSkill` as a strictly versioned execution block defining a `SkillContract`. The `SkillRegistry` validates this contract before execution, ensuring the role has access to the required memory namespaces, tool budgets, and input schemas.

## Consequences
- **Pros:** Safety and reusability. A `ParseResume` skill can be shared across multiple roles cleanly.
- **Cons:** Boilerplate overhead to register a simple skill.
