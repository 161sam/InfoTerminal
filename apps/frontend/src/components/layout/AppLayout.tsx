import { PropsWithChildren } from "react";
import Sidebar from "./Sidebar";

export default function AppLayout({ children }: PropsWithChildren) {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 min-w-0">
        <div className="border-b border-neutral-800 px-4 py-2 flex items-center justify-between">
          <div className="text-sm text-neutral-400">InfoTerminal Frontend</div>
          <div className="flex items-center gap-3 text-xs text-neutral-500">
            {/* TODO: Health-Badges */}
          </div>
        </div>
        <div className="p-4">{children}</div>
      </main>
    </div>
  );
}
