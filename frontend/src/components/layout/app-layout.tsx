import { Sidebar } from "./sidebar";
import { Topbar } from "./topbar";
import { Toaster } from "sonner";
import { CommandPalette } from "./command-palette";

export function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <div className="pl-64 flex flex-col min-h-screen">
        <Topbar />
        <main className="flex-1 p-8 overflow-y-auto">
          {children}
        </main>
      </div>
      <Toaster theme="dark" position="bottom-right" />
      <CommandPalette />
    </div>
  );
}
