import { Building } from "lucide-react";
import { useAnalyticsOrganization } from "@/hooks/useAnalytics";
import { AnalyticsWidgetWrapper } from "./AnalyticsWidgetWrapper";

export function OrganizationWidget() {
  const { data, isLoading, isError } = useAnalyticsOrganization();

  return (
    <AnalyticsWidgetWrapper
      title="Organization Analytics"
      description="Goals and role utilization."
      icon={<Building className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(_) => <></>}
    </AnalyticsWidgetWrapper>
  );
}
