import { LineChart } from "lucide-react";
import { useOrganizationMetrics } from "@/hooks/useOrganization";
import { OrganizationWidgetWrapper } from "./OrganizationWidgetWrapper";

export function OrganizationMetricsWidget() {
  const { data, isLoading, isError } = useOrganizationMetrics();

  return (
    <OrganizationWidgetWrapper
      title="Metrics"
      description="Organizational performance and health metrics."
      icon={<LineChart className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(metrics) => <pre>{JSON.stringify(metrics, null, 2)}</pre>}
    </OrganizationWidgetWrapper>
  );
}
