import { Activity } from "lucide-react";
import { useRecentActivity } from "@/hooks/useDashboard";
import { DashboardWidgetWrapper } from "@/components/DashboardWidgetWrapper";

export function DashboardActivityWidget() {
  const { data, isLoading, isError } = useRecentActivity();

  return (
    <DashboardWidgetWrapper
      title="Recent Activity"
      description="Unified event stream from all sub-systems."
      icon={<Activity className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(activity) => (
        <div className="space-y-4">
          {activity.activities.map((item) => (
            <div key={item.event_id} className="flex gap-4 p-3 border rounded-lg">
              <div className="flex-1">
                <p className="text-sm font-medium">{item.description}</p>
                <div className="flex items-center gap-2 mt-1 text-xs text-muted-foreground">
                  <span className="uppercase font-semibold tracking-wider">{item.source}</span>
                  <span>•</span>
                  <span>{new Date(item.timestamp).toLocaleString()}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </DashboardWidgetWrapper>
  );
}
