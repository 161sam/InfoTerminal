import { useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";

export default function ForensicsPage() {
  const [file, setFile] = useState<File | null>(null);
  const [sha, setSha] = useState("");
  const [result, setResult] = useState<any>(null);

  const upload = async () => {
    if (!file) return;
    const form = new FormData();
    form.append("file", file);
    const r = await fetch("/api/forensics/ingest", { method: "POST", body: form });
    setResult(await r.json());
  };
  const verify = async () => {
    const r = await fetch("/api/forensics/verify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sha256: sha }),
    });
    setResult(await r.json());
  };

  return (
    <DashboardLayout title="Forensics" subtitle="Chain-of-custody and hash verification">
      <div className="max-w-4xl mx-auto space-y-6 p-4">
        <Panel title="Ingest File">
          <div className="flex items-center gap-2">
            <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} />
            <button className="px-4 py-2 bg-primary-600 text-white rounded" onClick={upload}>
              Upload
            </button>
          </div>
        </Panel>
        <Panel title="Verify by SHA256">
          <div className="flex items-center gap-2">
            <input
              className="flex-1 border rounded p-2"
              value={sha}
              onChange={(e) => setSha(e.target.value)}
              placeholder="sha256..."
            />
            <button className="px-4 py-2 bg-gray-800 text-white rounded" onClick={verify}>
              Verify
            </button>
          </div>
        </Panel>
        {result && (
          <Panel title="Result">
            <pre className="text-sm">{JSON.stringify(result, null, 2)}</pre>
          </Panel>
        )}
      </div>
    </DashboardLayout>
  );
}
