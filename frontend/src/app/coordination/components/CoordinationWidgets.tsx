import { Users, History, CheckSquare, ArrowRightLeft, ShieldAlert } from "lucide-react";
import { 
  useCoordinationOverview, 
  useCoordinationSessions, 
  useCoordinationConsensus, 
  useCoordinationHandoffs, 
  useCoordinationConflicts 
} from "@/hooks/useCoordination";
import { CoordinationWidgetWrapper } from "./CoordinationWidgetWrapper";

export function CoordinationOverviewWidget() {
  const { data, isLoading, isError } = useCoordinationOverview();
  return (
    <CoordinationWidgetWrapper
      title="Coordination Overview"
      description="Active multi-agent coordination sessions."
      icon={<Users className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(overview) => <pre>{JSON.stringify(overview, null, 2)}</pre>}
    </CoordinationWidgetWrapper>
  );
}

export function CoordinationSessionsWidget() {
  const { data, isLoading, isError } = useCoordinationSessions();
  return (
    <CoordinationWidgetWrapper
      title="Sessions"
      description="History of coordination sessions."
      icon={<History className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(sessions) => <pre>{JSON.stringify(sessions, null, 2)}</pre>}
    </CoordinationWidgetWrapper>
  );
}

export function CoordinationConsensusWidget() {
  const { data, isLoading, isError } = useCoordinationConsensus();
  return (
    <CoordinationWidgetWrapper
      title="Consensus"
      description="Decisions reached via multi-agent consensus."
      icon={<CheckSquare className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(consensus) => <pre>{JSON.stringify(consensus, null, 2)}</pre>}
    </CoordinationWidgetWrapper>
  );
}

export function CoordinationHandoffsWidget() {
  const { data, isLoading, isError } = useCoordinationHandoffs();
  return (
    <CoordinationWidgetWrapper
      title="Handoffs"
      description="Work item handoffs between specialized agents."
      icon={<ArrowRightLeft className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(handoffs) => <pre>{JSON.stringify(handoffs, null, 2)}</pre>}
    </CoordinationWidgetWrapper>
  );
}

export function CoordinationConflictsWidget() {
  const { data, isLoading, isError } = useCoordinationConflicts();
  return (
    <CoordinationWidgetWrapper
      title="Conflicts"
      description="Detected conflicts and resolution status."
      icon={<ShieldAlert className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(conflicts) => <pre>{JSON.stringify(conflicts, null, 2)}</pre>}
    </CoordinationWidgetWrapper>
  );
}
