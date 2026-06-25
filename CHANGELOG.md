# Changelog

## [1.0.0] - 2026-06-25

### Added
- **AI Recruiting Organization:** Complete business logic encapsulation mapping 5 core roles (Resume Intelligence, Candidate Intelligence, Recruiter Assistant, Interview Operations, Communication) to reusable `AgentSkills`.
- **Multi-Agent Coordination Platform:** Distributed orchestration via `GoalEngine`, `DelegationPlanner`, `AgentMailbox`, and `ConsensusEngine`.
- **Agent Runtime Platform:** Observe -> Reason -> Execute -> Reflect Cognitive Pipeline with Replay Engine.
- **Enterprise Tool Platform:** Secure MCP tool brokering with granular `ExecutionBudget` firewalls.
- **Hybrid Memory Platform:** Semantic (Vector), Episodic, Procedural, and Working (SQL) memory namespaces.
- **Workflow Engine:** LangGraph-based state machine orchestration.
- **Frontend Studio:** Full Next.js enterprise portals spanning Data, Candidate, Workflow, Tools, Agent, Coordination, and Organization dashboards.

### Changed
- Refactored entire codebase to strict Clean Architecture (Domain, Application, Infrastructure isolation).
- Transitioned generic application state into `SharedContextSnapshots` scoped dynamically to prevent MemoryEngine pollution.
- Replaced monolithic `RecruiterAgent` abstractions with decoupled `AgentSkills` mapped to `OrganizationRoles`.

### Fixed
- Eliminated circular dependencies across domains.
- Enforced strict dependency inversion ensuring zero Application layers import Infrastructure layers.
