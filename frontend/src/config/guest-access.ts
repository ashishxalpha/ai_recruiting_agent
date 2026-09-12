export interface GuestCapabilities {
  canUploadCandidate: boolean;
  canTriggerWorkflow: boolean;
  canSubmitFeedback: boolean;
  canRunToolMutations: boolean;
  canManageJobs: boolean;
  canManageAgents: boolean;
}

export interface GuestAccessConfig {
  // Routes permitted for guests
  allowedRoutes: string[];
  
  // Routes explicitly restricted in guest mode
  restrictedRoutes: string[];
  
  // Feature flags / capabilities
  capabilities: GuestCapabilities;

  // UI styling and messaging for Guest Mode
  ui: {
    showGuestBanner: boolean;
    bannerMessage: string;
    lockRestrictedNavItems: boolean;
  };
}

/**
 * Configurable Guest Mode Access Policy
 * Adjust allowedRoutes, restrictedRoutes, or capabilities as needed.
 */
export const GUEST_ACCESS_CONFIG: GuestAccessConfig = {
  allowedRoutes: [
    "/",            // AI Platform Dashboard
    "/candidates",  // Candidate List & Profiles
    "/jobs",        // Job Requisitions & Matches
    "/analytics",   // Analytics & Funnel Overview
    "/activity",    // Real-Time System Stream
    "/tools",       // Tool Registry & Documentation
    "/playground",  // AI Playground (Read/Query)
  ],

  restrictedRoutes: [
    "/upload",      // Candidate Resume Ingestion
    "/feedback",    // Recruiter Evaluation Feedback
    "/workflow",    // Workflow Execution Engine
    "/agents",      // Autonomous Agent Orchestration
    "/coordination",// Multi-Agent Swarm
    "/memory",      // Agent Memory Stores
    "/organization" // Tenant & Settings
  ],

  capabilities: {
    canUploadCandidate: false,
    canTriggerWorkflow: false,
    canSubmitFeedback: false,
    canRunToolMutations: false,
    canManageJobs: false,
    canManageAgents: false,
  },

  ui: {
    showGuestBanner: true,
    bannerMessage: "You are currently exploring in Guest Mode (Read-Only). Sign in with a recruiter account to unlock uploads, workflows, and feedback.",
    lockRestrictedNavItems: true,
  }
};

/**
 * Checks if a given pathname is allowed for guest sessions.
 */
export function isRouteAllowedForGuest(pathname: string): boolean {
  // Check if explicitly restricted
  const isRestricted = GUEST_ACCESS_CONFIG.restrictedRoutes.some(route => 
    pathname === route || pathname.startsWith(`${route}/`)
  );
  if (isRestricted) return false;

  // Check if in allowed routes list
  return GUEST_ACCESS_CONFIG.allowedRoutes.some(route => 
    route === "/" ? pathname === "/" : (pathname === route || pathname.startsWith(`${route}/`))
  );
}

/**
 * Returns a human-friendly explanation for why a route is locked in guest mode.
 */
export function getGuestRestrictionDetails(pathname: string): { title: string; description: string } {
  if (pathname.startsWith("/upload")) {
    return {
      title: "Resume Ingestion Locked",
      description: "Uploading and processing candidate resumes with OCR and embeddings requires an authenticated recruiter profile."
    };
  }
  if (pathname.startsWith("/feedback")) {
    return {
      title: "Recruiter Feedback Locked",
      description: "Submitting candidate evaluations and decision logs requires an authorized recruiter identity."
    };
  }
  if (pathname.startsWith("/workflow")) {
    return {
      title: "Workflow Engine Locked",
      description: "Executing automated candidate screening and matching workflows requires an active user session."
    };
  }
  if (pathname.startsWith("/agents") || pathname.startsWith("/coordination") || pathname.startsWith("/memory")) {
    return {
      title: "Autonomous Agent Orchestration Locked",
      description: "Triggering LangGraph agent swarms and modifying memory states is restricted to authorized engineers and recruiters."
    };
  }
  return {
    title: "Resource Locked in Guest Mode",
    description: "This enterprise resource requires an authenticated recruiter or administrator account."
  };
}
