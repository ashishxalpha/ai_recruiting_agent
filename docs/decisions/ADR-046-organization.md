# ADR 046: Organization Plugins

## Context
If we hardcode the logic for "Recruiting" into the root AI Platform, we will not be able to reuse the platform for HR, Compliance, or Sales teams in the future.

## Decision
We introduce the `OrganizationPlugin` abstraction. The AI Platform is completely agnostic to business logic. The `RecruitingOrganization` is strictly implemented as a plugin configuring roles, skills, and templates.

## Consequences
- **Pros:** Massive extensibility. We can swap entire business logic layers cleanly.
- **Cons:** Added indirection layer before starting a coordination session.
