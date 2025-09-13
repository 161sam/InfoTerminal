import { useState } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";

export default function NLPPage() {
  const [text, setText] = useState("");
  const [ner, setNer] = useState<any | null>(null);
  const [summary, setSummary] = useState<string>("");
  const [error, setError] = useState<string>("");

  const callNer = async () => {
    setError("");
    setSummary("");
    try {
      const r = await fetch("http://127.0.0.1:8003/ner", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });
      if (!r.ok) throw new Error("bad");
      const j = await r.json();
      setNer(j);
    } catch (e) {
      setError("NLP-Service nicht verfügbar");
    }
  };

  const callSummarize = async () => {
    setError("");
    setNer(null);
    try {
      const r = await fetch("http://127.0.0.1:8003/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });
      if (!r.ok) throw new Error("bad");
      const j = await r.json();
      setSummary(j.summary);
    } catch (e) {
      setError("NLP-Service nicht verfügbar");
    }
  };

  return (
    <DashboardLayout title="NLP">
      <div className="max-w-3xl space-y-6">
        <h1 className="text-2xl font-semibold">NLP</h1>
        <Panel>
          <div className="space-y-4">
            <textarea
              value={text}
              onChange={e=>setText(e.target.value)}
              rows={6}
              className="w-full p-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              placeholder="Text eingeben…"
            />
            <div className="flex gap-2">
              <button className="btn btn-primary" onClick={callNer}>Entitäten extrahieren</button>
              <button className="btn btn-secondary" onClick={callSummarize}>Zusammenfassen</button>
            </div>
            {error && <div className="text-red-600 dark:text-red-400">{error}</div>}
            {ner && (
              <pre className="bg-gray-50 dark:bg-gray-800 p-3 rounded-lg overflow-auto text-sm">{JSON.stringify(ner, null, 2)}</pre>
            )}
            {summary && (
              <div>
                <b>Zusammenfassung:</b>
                <p className="text-sm text-gray-700 dark:text-gray-300">{summary}</p>
              </div>
            )}
          </div>
        </Panel>
      </div>
    </DashboardLayout>
  );
}
