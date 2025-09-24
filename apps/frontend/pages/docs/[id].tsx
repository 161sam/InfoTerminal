import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import EntityHighlighter from "@/components/docs/EntityHighlighter";
import DocCard from "@/components/docs/DocCard";
import { DocRecord } from "@/types/docs";
import EntityBadgeList, { BadgeItem } from "@/components/entities/EntityBadgeList";
import { uniqueEntities } from "@/lib/entities";
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";

export default function DocPage() {
  const router = useRouter();
  const { query } = router;
  const id = (query.id as string) || "";
  const [doc, setDoc] = useState<DocRecord | null>(null);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    if (!id) return;
    fetch(`${process.env.NEXT_PUBLIC_DOC_ENTITIES_URL}/docs/${encodeURIComponent(id)}`)
      .then(async (r) => {
        if (!r.ok) throw new Error("not found");
        return r.json();
      })
      .then(setDoc)
      .catch(() => setError("Dokument nicht gefunden"));
  }, [id]);

  if (error)
    return (
      <DashboardLayout title="Document">
        <div className="max-w-5xl text-red-600 dark:text-red-400">{error}</div>
      </DashboardLayout>
    );
  if (!doc)
    return (
      <DashboardLayout title="Document">
        <div className="max-w-5xl">Lade...</div>
      </DashboardLayout>
    );

  const badges: BadgeItem[] = uniqueEntities(
    doc.entities.map((e) => ({ label: e.label, value: e.text || "" })),
  );

  const handleBadgeClick = (item: BadgeItem) => {
    if (item.value) router.push(`/search?value=${encodeURIComponent(item.value)}`);
    else router.push(`/search?entity=${encodeURIComponent(item.label)}`);
  };

  return (
    <DashboardLayout title="Document">
      <div className="max-w-6xl grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-3 space-y-6">
          <Panel>
            <DocCard doc={doc} />
          </Panel>
          <Panel title="Content">
            <EntityHighlighter text={doc.text} entities={doc.entities} />
          </Panel>
        </div>
        <aside className="lg:col-span-1 space-y-4">
          <Panel title="Entitäten">
            <EntityBadgeList items={badges} onBadgeClick={handleBadgeClick} />
          </Panel>
        </aside>
      </div>
    </DashboardLayout>
  );
}
