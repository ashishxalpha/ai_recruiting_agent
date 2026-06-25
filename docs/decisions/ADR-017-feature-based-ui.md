# ADR 017: Feature-Based UI Architecture

## Context
Standard Next.js applications often group all components in a single `src/components` folder and all hooks in `src/hooks`. As the application grows to encompass Candidates, Jobs, Workflows, Analytics, and Feedback, this "type-based" grouping becomes unmanageable.

## Decision
We will use a **Feature-Based Architecture**. 
Under `src/features/`, we will create domain-specific folders (e.g., `candidate/`, `matching/`, `jobs/`). Each feature folder will contain its own `components/`, `hooks/`, `services/`, and `types/` relevant *only* to that feature. 
Global shared UI components (like Buttons or Cards) will remain in `src/components/ui/`.

## Consequences
- **Pros**: High cohesion. Developers working on the "Candidate" feature have all relevant code isolated in one directory.
- **Cons**: Deciding where a shared business component lives can sometimes be ambiguous. Rule of thumb: If it's used by two features, move it to a shared `src/lib` or `src/components/shared` folder.
