import { Target } from "lucide-react";
import { useOrganizationGoals } from "@/hooks/useOrganization";
import { OrganizationWidgetWrapper } from "./OrganizationWidgetWrapper";

export function OrganizationGoalsWidget() {
  const { data, isLoading, isError } = useOrganizationGoals();

  return (
    <OrganizationWidgetWrapper
      title="Goals"
      description="Strategic objectives assigned to the organization."
      icon={<Target className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(goals) => <pre>{JSON.stringify(goals, null, 2)}</pre>}
    </OrganizationWidgetWrapper>
  );
}
