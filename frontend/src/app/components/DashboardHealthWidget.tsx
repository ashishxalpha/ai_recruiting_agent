import { HeartPulse, CheckCircle2, AlertTriangle, AlertCircle } from "lucide-react";
import { useDashboardHealth } from "@/hooks/useDashboard";
import { DashboardWidgetWrapper } from "@/components/DashboardWidgetWrapper";

export function DashboardHealthWidget() {
  const { data, isLoading, isError } = useDashboardHealth();

  return (
    <DashboardWidgetWrapper
      title="Platform Health"
      description="Real-time status of backend infrastructure and orchestration engines."
      icon={<HeartPulse className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(health) => (
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
            <span className="font-semibold">Overall Status</span>
            {health.overall_status === 'healthy' ? (
              <span className="flex items-center text-green-600 font-medium"><CheckCircle2 className="w-4 h-4 mr-2" /> Healthy</span>
            ) : (
              <span className="flex items-center text-amber-600 font-medium"><AlertTriangle className="w-4 h-4 mr-2" /> Degraded</span>
            )}
          </div>
          
          <div className="space-y-3">
            {[
              { label: 'PostgreSQL Database', data: health.database },
              { label: 'Redis Cache', data: health.redis },
              { label: 'Workflow Engine', data: health.workflow_engine },
              { label: 'Agent Swarm', data: health.agent_swarm },
              { label: 'Memory Engine', data: health.memory_engine },
            ].map((system, idx) => (
              <div key={idx} className="flex items-center justify-between border-b pb-3 last:border-0 last:pb-0">
                <div>
                  <p className="font-medium text-sm">{system.label}</p>
                  <p className="text-xs text-muted-foreground">{system.data.message}</p>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-xs font-mono text-muted-foreground">{system.data.latency_ms}ms</span>
                  {system.data.status === 'healthy' ? (
                    <CheckCircle2 className="w-4 h-4 text-green-500" />
                  ) : system.data.status === 'degraded' ? (
                    <AlertTriangle className="w-4 h-4 text-amber-500" />
                  ) : (
                    <AlertCircle className="w-4 h-4 text-red-500" />
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </DashboardWidgetWrapper>
  );
}
