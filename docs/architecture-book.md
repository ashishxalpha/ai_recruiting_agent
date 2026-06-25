# Architecture Book: AI Recruiting Platform

## Introduction
The AI Recruiting Platform (v1.0.0) is an enterprise-grade AI automation platform designed specifically for recruiting workflows. It replaces traditional manual applicant tracking tasks with an intelligent swarm of specialized agents.

## Subsystem Architecture
The system is built on a layered architecture enforcing Dependency Inversion:

1. **Frontend (Next.js):** The operational Studio (Workflow, Coordinator, Organization, Tools).
2. **Organization Plugin:** The Recruiting Domain mapping Goals to Agent Skills.
3. **AI Kernel:** The execution-scoped context bridging infrastructure and agents.
4. **Coordination Platform:** Goal decomposition, delegation, and consensus via the `AgentCommunicationBus`.
5. **Agent Runtime:** The cognitive reasoning loop (`Observe -> Reason -> Plan -> Execute -> Reflect`).
6. **Tool Platform:** Securely broker and execute tools (Local, Remote, MCP).
7. **Memory Platform:** Hybrid SQL/Vector storage for Semantic, Episodic, Procedural, and Working memory.
8. **Workflow Engine:** LangGraph orchestration orchestrating state machines.

## Key Design Decisions
- **Decoupled Business Logic:** The base platform is completely generic. The "Recruiting" logic is injected purely as an `OrganizationPlugin`.
- **Zero Direct Agent Communication:** Agents never call each other. They communicate via `AgentMessage`s enqueued in `AgentMailbox`es.
- **Deterministic Learning:** The models are never trained online. "Learning" is defined as creating and retrieving Insights from the `MemoryEngine`.
- **Safety First:** The `OrganizationPolicy` acts as a strict pre-execution firewall.

For more details, consult the `ENGINEERING_DECISIONS.md`.
