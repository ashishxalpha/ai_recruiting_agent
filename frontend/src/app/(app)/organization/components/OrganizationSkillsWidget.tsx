import { Lightbulb } from "lucide-react";
import { useOrganizationSkills } from "@/hooks/useOrganization";
import { OrganizationWidgetWrapper } from "./OrganizationWidgetWrapper";

export function OrganizationSkillsWidget() {
  const { data, isLoading, isError } = useOrganizationSkills();

  return (
    <OrganizationWidgetWrapper
      title="Skills"
      description="Capabilities available within the agent workforce."
      icon={<Lightbulb className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(skills) => <pre>{JSON.stringify(skills, null, 2)}</pre>}
    </OrganizationWidgetWrapper>
  );
}
