# Frontend Architecture
The frontend is a Next.js App Router application built with a Feature-Based Architecture.

## Layers
- **UI Components**: shadcn/ui and custom `.tsx` elements.
- **State/Caching**: TanStack Query (`@tanstack/react-query`).
- **Services**: Pure data transformers.
- **API Clients**: Axios-based or fetch wrappers.

# Design System
Inspired by Vercel and Linear, we utilize:
- Sleek dark modes.
- Micro-animations via `framer-motion`.
- `lucide-react` iconography.

# Realtime Updates
Realtime state is managed via an EventSource SSE connection mapped to TanStack Query invalidations or optimistic updates.
