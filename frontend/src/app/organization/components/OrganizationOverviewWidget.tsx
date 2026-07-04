import { Building } from "lucide-react";
import { useOrganizationOverview } from "@/hooks/useOrganization";
import { OrganizationWidgetWrapper } from "./OrganizationWidgetWrapper";

export function OrganizationOverviewWidget() {
  const { data, isLoading, isError } = useOrganizationOverview();

  return (
    <OrganizationWidgetWrapper
      title="Organization Overview"
      description="Top-level view of your AI organization."
      icon={<Building className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(overview) => <pre>{JSON.stringify(overview, null, 2)}</pre>}
    </OrganizationWidgetWrapper>
  );
}
