"use client";

import { useSSE } from "@/lib/hooks/use-sse";
import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function ActivityPage() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const { lastEvent, isConnected } = useSSE(`${apiUrl}/api/v1/stream`);
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    if (lastEvent) {
      setEvents((prev) => [lastEvent, ...prev].slice(0, 50)); // keep last 50
    }
  }, [lastEvent]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Global Activity</h1>
          <p className="text-muted-foreground mt-2">
            Real-time platform event stream from domain EventBus.
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Badge variant={isConnected ? "default" : "destructive"} className="px-3 py-1 text-xs">
            <span className={`w-2 h-2 rounded-full mr-2 ${isConnected ? "bg-emerald-400 animate-pulse" : "bg-red-400"}`} />
            {isConnected ? "Connected (Live)" : "Disconnected"}
          </Badge>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Live Event Log</CardTitle>
          <CardDescription>Streaming domain events and background worker notifications.</CardDescription>
        </CardHeader>
        <CardContent>
          {events.length === 0 ? (
            <div className="text-center py-16 text-muted-foreground flex flex-col items-center justify-center space-y-2">
              <span className="inline-block w-3 h-3 rounded-full bg-primary/40 animate-ping" />
              <p className="font-medium text-sm">Listening for real-time domain events...</p>
              <p className="text-xs text-muted-foreground">Upload a resume or trigger candidate matching to observe events live.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {events.map((evt, i) => (
                <div key={i} className="flex flex-col space-y-2 p-3.5 border rounded-lg bg-card/50 hover:bg-accent/10 transition-colors">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Badge variant="outline" className="font-mono text-[11px] uppercase tracking-wider">
                        {evt.type || "DOMAIN_EVENT"}
                      </Badge>
                      <span className="text-xs font-semibold text-foreground">
                        {evt.data?.message || evt.data?.action || "Domain Event Emitted"}
                      </span>
                    </div>
                    <span className="text-[11px] text-muted-foreground">
                      {evt.timestamp ? new Date(evt.timestamp).toLocaleTimeString() : "Just now"}
                    </span>
                  </div>
                  {evt.data && (
                    <pre className="text-[11px] bg-muted/60 p-2.5 rounded text-muted-foreground overflow-x-auto font-mono">
                      {JSON.stringify(evt.data, null, 2)}
                    </pre>
                  )}
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
