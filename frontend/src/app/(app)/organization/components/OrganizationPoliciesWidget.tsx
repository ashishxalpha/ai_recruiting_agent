import { Shield } from "lucide-react";
import { useOrganizationPolicies } from "@/hooks/useOrganization";
import { OrganizationWidgetWrapper } from "./OrganizationWidgetWrapper";

export function OrganizationPoliciesWidget() {
  const { data, isLoading, isError } = useOrganizationPolicies();

  return (
    <OrganizationWidgetWrapper
      title="Policies"
      description="Operational constraints and organizational rules."
      icon={<Shield className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(policies) => <pre>{JSON.stringify(policies, null, 2)}</pre>}
    </OrganizationWidgetWrapper>
  );
}
