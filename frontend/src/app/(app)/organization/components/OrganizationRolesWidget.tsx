import { Briefcase } from "lucide-react";
import { useOrganizationRoles } from "@/hooks/useOrganization";
import { OrganizationWidgetWrapper } from "./OrganizationWidgetWrapper";

export function OrganizationRolesWidget() {
  const { data, isLoading, isError } = useOrganizationRoles();

  return (
    <OrganizationWidgetWrapper
      title="Roles"
      description="Defined roles and permissions for agents."
      icon={<Briefcase className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(roles) => <pre>{JSON.stringify(roles, null, 2)}</pre>}
    </OrganizationWidgetWrapper>
  );
}
