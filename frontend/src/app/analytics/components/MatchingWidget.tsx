import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from "recharts";
import { Cpu } from "lucide-react";
import { useAnalyticsMatching } from "@/hooks/useAnalytics";
import { AnalyticsWidgetWrapper } from "./AnalyticsWidgetWrapper";

const COLORS = ['#22c55e', '#ef4444'];

export function MatchingWidget() {
  const { data, isLoading, isError } = useAnalyticsMatching();

  return (
    <AnalyticsWidgetWrapper
      title="AI Agreement Rate"
      description="How often recruiters agree with the semantic ranking."
      icon={<Cpu className="w-5 h-5 text-muted-foreground" />}
      isLoading={isLoading}
      isError={isError}
      data={data}
    >
      {(matching) => {
        const approved = matching.approval_rate;
        const rejected = 100 - matching.approval_rate;
        
        const chartData = [
          { name: 'Agreed', value: approved },
          { name: 'Disagreed', value: rejected },
        ];

        return (
          <div className="h-full w-full flex flex-col">
            <ResponsiveContainer width="100%" height="80%">
              <PieChart>
                <Pie
                  data={chartData}
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => `${Number(value).toFixed(1)}%`} />
              </PieChart>
            </ResponsiveContainer>
            <div className="flex justify-center space-x-4 mt-2 text-sm h-[20%]">
              <div className="flex items-center"><div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div> Agreed ({approved.toFixed(1)}%)</div>
              <div className="flex items-center"><div className="w-3 h-3 bg-red-500 rounded-full mr-2"></div> Disagreed ({rejected.toFixed(1)}%)</div>
            </div>
          </div>
        );
      }}
    </AnalyticsWidgetWrapper>
  );
}
