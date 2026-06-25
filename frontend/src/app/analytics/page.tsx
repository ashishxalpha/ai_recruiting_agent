"use client";

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, PieChart, Pie, Cell } from "recharts";

export default function AnalyticsPage() {
  const funnelData = [
    { name: 'Matches', value: 1000 },
    { name: 'Shortlisted', value: 300 },
    { name: 'Interviewed', value: 150 },
    { name: 'Offers', value: 45 },
    { name: 'Hires', value: 30 },
  ];

  const agreementData = [
    { name: 'Agreed', value: 820 },
    { name: 'Disagreed', value: 180 },
  ];
  const COLORS = ['#22c55e', '#ef4444'];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Analytics</h1>
        <p className="text-muted-foreground mt-2">
          Monitor recruiting performance and AI metrics.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Recruiting Metrics */}
        <Card>
          <CardHeader>
            <CardTitle>Recruiting Funnel</CardTitle>
            <CardDescription>Conversion rates from AI match to Hire.</CardDescription>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={funnelData}>
                <XAxis dataKey="name" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip cursor={{fill: 'transparent'}} />
                <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* AI Metrics */}
        <Card>
          <CardHeader>
            <CardTitle>AI Agreement Rate</CardTitle>
            <CardDescription>How often recruiters agree with the semantic ranking.</CardDescription>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={agreementData}
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {agreementData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
            <div className="flex justify-center space-x-4 mt-4 text-sm">
              <div className="flex items-center"><div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div> Agreed (82%)</div>
              <div className="flex items-center"><div className="w-3 h-3 bg-red-500 rounded-full mr-2"></div> Disagreed (18%)</div>
            </div>
          </CardContent>
        </Card>
        
        {/* Infrastructure Metrics */}
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>Infrastructure Latency</CardTitle>
            <CardDescription>Average latency for embeddings and extractions over 24h.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[200px] flex items-center justify-center text-muted-foreground border rounded-md">
              Latency Time Series Chart Placeholder
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
