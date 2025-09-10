import Link from "next/link";
import { useRouter } from "next/router";
import { sidebar } from "@/lib/routes";

export default function Sidebar() {
  const { pathname } = useRouter();
  return (
    <aside className="h-screen w-64 shrink-0 border-r border-neutral-800 bg-neutral-950/60 backdrop-blur px-3 py-4 sticky top-0">
      <div className="mb-6 px-2">
        <h1 className="text-lg font-semibold tracking-tight">InfoTerminal</h1>
        <p className="text-xs text-neutral-400">Unified Analyst Workspace</p>
      </div>
      <nav className="space-y-1">
        {sidebar.map(item => {
          if (item.label === "—") return <div key={"div-" + Math.random()} className="my-2 border-t border-neutral-800" />;
          const active = item.href && pathname === item.href;
          const disabled = item.externalKey && !process.env[item.externalKey as any];
          const cls = [
            "block rounded-md px-3 py-2 text-sm",
            active ? "bg-neutral-800 text-white" : "text-neutral-300 hover:bg-neutral-800/60",
            disabled ? "opacity-40 pointer-events-none" : "",
          ].join(" ");
          return (
            <Link key={item.label} href={item.href} className={cls} title={disabled ? `.env fehlt: ${item.externalKey}` : undefined}>
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
