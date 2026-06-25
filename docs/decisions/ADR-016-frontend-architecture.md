# ADR 016: Frontend Architecture and Data Flow

## Context
We are building a production-grade Enterprise Recruiter Portal. A major pain point in React apps is mixing UI logic with data fetching and API definitions.

## Decision
We enforce a strict 4-layer architecture:
**Component → Hook → Service → API Client**
1. **Component**: React components (`.tsx`). Purely concerned with UI, state binding, and rendering. They NEVER call `fetch` or `axios` directly.
2. **Hook**: Custom React Hooks (usually wrapping TanStack `useQuery` or `useMutation`). They handle caching, loading states, and React integration.
3. **Service**: Pure TypeScript classes or functions that orchestrate business logic or data transformation before handing it to the UI.
4. **API Client**: The lowest level wrapper around Axios/Fetch that handles headers, base URLs, and error interception.

## Consequences
- **Pros**: Highly testable. You can mock the Service layer when testing hooks, or mock the API client when testing services. Components remain clean.
- **Cons**: Requires more boilerplate files for simple API requests.
