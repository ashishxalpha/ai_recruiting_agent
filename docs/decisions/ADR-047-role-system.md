# ADR 047: Role System

## Context
Building monolithic agents (e.g. "RecruiterAgent") results in unmanageable prompt bloat and spaghetti logic as responsibilities grow.

## Decision
We decompose monolithic agents into `OrganizationRoles` (e.g., `ResumeIntelligenceLead`). Roles contain ZERO execution logic. They merely define the subset of `AgentSkills` they are permitted to invoke. The execution engine dynamically builds context based on the assigned role.

## Consequences
- **Pros:** Sharp separation of concerns. Prompts are hyper-focused.
- **Cons:** A single complex workflow might require jumping between multiple roles via the Coordination Platform.
