import { LayoutDashboard } from "lucide-react";
import { useDashboardSummary } from "@/hooks/useDashboard";
import { DashboardWidgetWrapper } from "@/components/DashboardWidgetWrapper";

export function DashboardOverviewWidget() {
  const { data, isLoading, isError } = useDashboardSummary();

  return (
    <DashboardWidgetWrapper
      title="Platform Summary"
      description="Top-level metrics across all operational scopes."
      icon={<LayoutDashboard className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
      contentClassName="p-0 border-t"
    >
      {(summary) => (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-0 divide-x divide-y border-b">
          <div className="p-6 flex flex-col items-center justify-center text-center">
            <span className="text-3xl font-bold text-primary">{summary.total_candidates}</span>
            <span className="text-xs text-muted-foreground mt-1 uppercase tracking-wider">Candidates</span>
          </div>
          <div className="p-6 flex flex-col items-center justify-center text-center">
            <span className="text-3xl font-bold text-primary">{summary.active_jobs}</span>
            <span className="text-xs text-muted-foreground mt-1 uppercase tracking-wider">Active Jobs</span>
          </div>
          <div className="p-6 flex flex-col items-center justify-center text-center bg-blue-50/50">
            <span className="text-3xl font-bold text-blue-600">{summary.running_agents}</span>
            <span className="text-xs text-muted-foreground mt-1 uppercase tracking-wider">Agents Running</span>
          </div>
          <div className="p-6 flex flex-col items-center justify-center text-center bg-green-50/50">
            <span className="text-3xl font-bold text-green-600">{summary.active_workflows}</span>
            <span className="text-xs text-muted-foreground mt-1 uppercase tracking-wider">Workflows</span>
          </div>
          <div className="p-6 flex flex-col items-center justify-center text-center">
            <span className="text-3xl font-bold text-primary">{summary.pending_feedback}</span>
            <span className="text-xs text-muted-foreground mt-1 uppercase tracking-wider">Pending Feedback</span>
          </div>
          <div className="p-6 flex flex-col items-center justify-center text-center">
            <span className="text-3xl font-bold text-primary">{summary.active_coordination_sessions}</span>
            <span className="text-xs text-muted-foreground mt-1 uppercase tracking-wider">Coord Sessions</span>
          </div>
          <div className="p-6 flex flex-col items-center justify-center text-center">
            <span className="text-3xl font-bold text-primary">{summary.memory_count}</span>
            <span className="text-xs text-muted-foreground mt-1 uppercase tracking-wider">Memories</span>
          </div>
          <div className="p-6 flex flex-col items-center justify-center text-center">
            <span className="text-3xl font-bold text-primary">{summary.todays_uploads}</span>
            <span className="text-xs text-muted-foreground mt-1 uppercase tracking-wider">Today's Uploads</span>
          </div>
        </div>
      )}
    </DashboardWidgetWrapper>
  );
}
