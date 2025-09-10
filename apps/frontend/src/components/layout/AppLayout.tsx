import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";

export default function AppLayout() {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 min-w-0">
        {/* Topbar optional */}
        <div className="border-b px-4 py-2 flex items-center justify-between">
          <div className="text-sm text-neutral-600">InfoTerminal Frontend</div>
          {/* Platz für User-Menu / Health-Badge */}
        </div>
        <div className="p-4">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
