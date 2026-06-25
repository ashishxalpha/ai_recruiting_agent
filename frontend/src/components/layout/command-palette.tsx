"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { Command } from "cmdk";
import { Users, Briefcase, Activity, MessageSquareHeart } from "lucide-react";
import { Dialog, DialogContent } from "@/components/ui/dialog";

export function CommandPalette() {
  const [open, setOpen] = React.useState(false);
  const router = useRouter();

  React.useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };

    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  const runCommand = React.useCallback((command: () => void) => {
    setOpen(false);
    command();
  }, []);

  // Using simple Dialog wrapper for cmdk to avoid complex shadcn command setup issues
  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="overflow-hidden p-0 shadow-lg">
        <Command className="[&_[cmdk-root]]:min-h-[300px] [&_[cmdk-root]]:w-full [&_[cmdk-root]]:bg-background [&_[cmdk-root]]:text-foreground">
          <Command.Input 
            className="flex h-11 w-full rounded-md bg-transparent py-3 px-4 text-sm outline-none placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50 border-b"
            placeholder="Type a command or search..." 
          />
          <Command.List className="max-h-[300px] overflow-y-auto overflow-x-hidden py-2 px-2">
            <Command.Empty className="py-6 text-center text-sm">No results found.</Command.Empty>
            <Command.Group heading="Navigation">
              <Command.Item
                className="relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none aria-selected:bg-accent aria-selected:text-accent-foreground data-[disabled=true]:pointer-events-none data-[disabled=true]:opacity-50 mb-1"
                onSelect={() => runCommand(() => router.push("/candidates"))}
              >
                <Users className="mr-2 h-4 w-4" />
                Candidates
              </Command.Item>
              <Command.Item
                className="relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none aria-selected:bg-accent aria-selected:text-accent-foreground data-[disabled=true]:pointer-events-none data-[disabled=true]:opacity-50 mb-1"
                onSelect={() => runCommand(() => router.push("/jobs"))}
              >
                <Briefcase className="mr-2 h-4 w-4" />
                Jobs
              </Command.Item>
              <Command.Item
                className="relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none aria-selected:bg-accent aria-selected:text-accent-foreground data-[disabled=true]:pointer-events-none data-[disabled=true]:opacity-50 mb-1"
                onSelect={() => runCommand(() => router.push("/feedback"))}
              >
                <MessageSquareHeart className="mr-2 h-4 w-4" />
                Feedback
              </Command.Item>
              <Command.Item
                className="relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none aria-selected:bg-accent aria-selected:text-accent-foreground data-[disabled=true]:pointer-events-none data-[disabled=true]:opacity-50"
                onSelect={() => runCommand(() => router.push("/analytics"))}
              >
                <Activity className="mr-2 h-4 w-4" />
                Analytics
              </Command.Item>
            </Command.Group>
          </Command.List>
        </Command>
      </DialogContent>
    </Dialog>
  );
}
