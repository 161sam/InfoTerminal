import { NavLink } from "react-router-dom";
import { appRoutes, getExternalUrl } from "../../routes/appRoutes";

export default function Sidebar() {
  return (
    <aside className="h-screen w-64 shrink-0 border-r bg-white/70 backdrop-blur px-3 py-4 sticky top-0">
      <div className="mb-6 px-2">
        <h1 className="text-xl font-semibold tracking-tight">InfoTerminal</h1>
        <p className="text-xs text-neutral-500">Unified Analyst Workspace</p>
      </div>

      <nav className="space-y-1">
        {appRoutes.filter(r => r.enabled !== false).map((r) => {
          const to = r.path;
          const isExt = r.kind === "external";
          const disabled = isExt && !getExternalUrl(r); // kein URL in env
          return (
            <NavLink
              key={r.key}
              to={to}
              className={({ isActive }) =>
                [
                  "block rounded-lg px-3 py-2 text-sm",
                  disabled ? "opacity-40 pointer-events-none" : "hover:bg-neutral-100",
                  isActive ? "bg-neutral-900 text-white hover:bg-neutral-900" : "text-neutral-800"
                ].join(" ")
              }
              title={disabled ? "URL not configured (.env)" : undefined}
              end={r.path === "/"}
            >
              {r.label}
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}
