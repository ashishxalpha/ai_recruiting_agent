# Engineering Decisions (Narrative Companion to ADRs)

## The Philosophy of the Platform
Building an AI platform is distinct from building a standard SaaS application. LLMs are non-deterministic, hallucinatory, and expensive. Every major engineering decision in this platform revolves around **containment, observability, and modularity**.

### Why Dependency Inversion? (Sprints 1-3)
We strictly separated the Domain from Application and Infrastructure. If a specific embedding provider or Vector DB (e.g. Pinecone vs pgvector) goes offline or deprecates their API, we only rewrite the specific adapter in `/infrastructure`. The core domain rules never change.

### Why Avoid LangChain/LlamaIndex for Core Logic? (Sprint 5-8)
We deliberately avoided tightly coupling the core business logic to heavy orchestration frameworks like LangChain. We treated LangGraph as an *implementation detail* of the `WorkflowPlatform` interface. This allows us to upgrade or replace the underlying graph engine without rewriting the entire application.

### Why No Multi-Agent Frameworks (AutoGen/CrewAI)? (Sprint 12)
Frameworks like CrewAI and AutoGen enforce rigid conversational paradigms. We needed a highly robust, event-driven, distributed system. Therefore, we built a bespoke `CoordinationPlatform` utilizing an `AgentCommunicationBus`. Agents never call each other directly; they push messages to a broker. This means we can deploy Agent A in AWS and Agent B in GCP, and they will coordinate seamlessly.

### Why Plugins for the Recruiting Logic? (Sprint 13)
By abstracting the recruiting functionality into an `OrganizationPlugin`, we built a generic Multi-Agent Operating System. You can clone this codebase, swap out the `RecruitingOrganization` for a `SalesOrganization`, and the entire `ToolPlatform`, `MemoryEngine`, and `CoordinationPlatform` will run identically.

### Why Time-Travel Debugging? (Sprint 11)
Observing a swarm of agents is impossible if you only look at the final output. We enforce the creation of `SessionSnapshots` at every iteration of the `CognitivePipeline`. The `ReplayEngine` allows developers to natively time-travel through an agent's reasoning trace frame-by-frame, perfectly reconstructing errors without re-executing expensive tools.
