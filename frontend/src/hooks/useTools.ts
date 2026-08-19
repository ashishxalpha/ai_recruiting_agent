import { useQuery } from '@tanstack/react-query';
import { ToolsService } from '@/services/tools.service';

export function useToolsCapabilities() {
  return useQuery({
    queryKey: ['tools', 'capabilities'],
    queryFn: () => ToolsService.getCapabilities(),
  });
}
