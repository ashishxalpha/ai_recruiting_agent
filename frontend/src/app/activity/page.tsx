"use client";

import { useSSE } from "@/lib/hooks/use-sse";
import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function ActivityPage() {
  const { lastEvent, isConnected } = useSSE("http://localhost:8000/api/v1/stream");
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
            Real-time platform event stream.
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Badge variant={isConnected ? "default" : "destructive"}>
            {isConnected ? "Connected (Live)" : "Disconnected"}
          </Badge>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Event Log</CardTitle>
          <CardDescription>Streaming directly from the Domain Event Bus.</CardDescription>
        </CardHeader>
        <CardContent>
          {events.length === 0 ? (
            <div className="text-center py-10 text-muted-foreground">
              Waiting for events...
            </div>
          ) : (
            <div className="space-y-4">
              {events.map((evt, i) => (
                <div key={i} className="flex flex-col space-y-1 pb-4 border-b last:border-0">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold">{evt.type}</span>
                    <span className="text-xs text-muted-foreground">Just now</span>
                  </div>
                  <pre className="text-xs bg-muted p-2 rounded-md overflow-x-auto">
                    {JSON.stringify(evt.data, null, 2)}
                  </pre>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
