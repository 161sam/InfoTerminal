import { useState } from "react";
import UploadBox from "@/components/upload/UploadBox";
import DashboardLayout from "@/components/layout/DashboardLayout";
import Panel from "@/components/layout/Panel";

export default function DocumentsPage() {
  const [lastResults, setLastResults] = useState<any[]>([]);
  return (
    <DashboardLayout title="Documents">
      <div className="space-y-6 max-w-3xl">
        <h1 className="text-2xl font-semibold mb-6">Upload neue Dokumente</h1>
        <Panel>
          <UploadBox multiple onComplete={setLastResults} />
          <p className="mt-4 text-sm text-gray-600 dark:text-slate-300">
            PDF ohne extrahierbaren Text erfordern OCR via NiFi (später verfügbar)
          </p>
        </Panel>
        {lastResults.length > 0 && (
          <Panel>
            <h2 className="font-semibold">Letzte Uploads</h2>
            <ul className="list-disc list-inside">
              {lastResults.map((r) => (
                <li key={r.file}>
                  {r.file} – {r.status}
                </li>
              ))}
            </ul>
          </Panel>
        )}
      </div>
    </DashboardLayout>
  );
}
