import { Activity } from "lucide-react";
import { useOrganizationActivity } from "@/hooks/useOrganization";
import { OrganizationWidgetWrapper } from "./OrganizationWidgetWrapper";

export function OrganizationActivityWidget() {
  const { data, isLoading, isError } = useOrganizationActivity();

  return (
    <OrganizationWidgetWrapper
      title="Recent Activity"
      description="Timeline of organizational events and operations."
      icon={<Activity className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(activity) => <pre>{JSON.stringify(activity, null, 2)}</pre>}
    </OrganizationWidgetWrapper>
  );
}
