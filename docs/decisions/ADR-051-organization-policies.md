# ADR 051: Pre-execution Organization Policies

## Context
If a skill runs wild due to an LLM hallucination, it could burn through api budgets or execute unauthorized tools.

## Decision
The `OrganizationPolicy` acts as a strict firewall enforced *before* any skill or role invokes the underlying AIKernel. It validates the ExecutionBudget, memory access, and human-approval gates synchronously.

## Consequences
- **Pros:** Hard safety limits. Rogue behavior is impossible without breaching the kernel firewall.
- **Cons:** Added latency overhead to policy resolution per skill execution.
