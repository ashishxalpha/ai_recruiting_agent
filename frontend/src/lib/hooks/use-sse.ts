import { useEffect, useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';

export function useSSE(url: string) {
  const [lastEvent, setLastEvent] = useState<any>(null);
  const [isConnected, setIsConnected] = useState(false);
  const queryClient = useQueryClient();

  useEffect(() => {
    // Only connect if we have a URL
    if (!url) return;

    const eventSource = new EventSource(url);

    eventSource.onopen = () => {
      setIsConnected(true);
      console.log(`SSE Connected to ${url}`);
    };

    eventSource.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data);
        setLastEvent(parsed);
        
        // Optimistically invalidate queries based on event types
        if (parsed.type === 'CandidateMatched') {
          queryClient.invalidateQueries({ queryKey: ['matches'] });
        } else if (parsed.type === 'RecruiterFeedbackSubmitted') {
          queryClient.invalidateQueries({ queryKey: ['feedback'] });
          queryClient.invalidateQueries({ queryKey: ['analytics'] });
        } else if (parsed.type === 'GroundTruthRecorded') {
          queryClient.invalidateQueries({ queryKey: ['outcomes'] });
          queryClient.invalidateQueries({ queryKey: ['analytics'] });
        }
      } catch (e) {
        console.error('Failed to parse SSE event data', e);
      }
    };

    eventSource.onerror = (error) => {
      console.error('SSE Error', error);
      setIsConnected(false);
      // EventSource auto-reconnects, but we can close and recreate if needed
    };

    return () => {
      eventSource.close();
      setIsConnected(false);
    };
  }, [url, queryClient]);

  return { lastEvent, isConnected };
}
