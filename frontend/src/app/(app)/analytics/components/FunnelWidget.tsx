import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts";
import { Filter } from "lucide-react";
import { useAnalyticsFunnel } from "@/hooks/useAnalytics";
import { AnalyticsWidgetWrapper } from "./AnalyticsWidgetWrapper";

export function FunnelWidget() {
  const { data, isLoading, isError } = useAnalyticsFunnel();

  return (
    <AnalyticsWidgetWrapper
      title="Recruiting Funnel"
      description="Conversion rates from AI match to Hire."
      icon={<Filter className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(funnel) => {
        const chartData = [
          { name: 'Applications', value: funnel.applications },
          { name: 'Processing', value: funnel.processing },
          { name: 'Review', value: funnel.review },
          { name: 'Shortlisted', value: funnel.shortlisted },
          { name: 'Interviewed', value: funnel.interview },
          { name: 'Offers', value: funnel.offer },
          { name: 'Hires', value: funnel.hired },
        ];

        return (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <XAxis dataKey="name" fontSize={12} tickLine={false} axisLine={false} />
              <YAxis fontSize={12} tickLine={false} axisLine={false} />
              <Tooltip cursor={{fill: 'transparent'}} />
              <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        );
      }}
    </AnalyticsWidgetWrapper>
  );
}
