import { useState } from 'react';
import UploadBox from '../../src/components/upload/UploadBox';

export default function DocumentsPage() {
  const [lastResults, setLastResults] = useState<any[]>([]);
  return (
    <main className="max-w-2xl mx-auto p-4">
      <h1 className="text-2xl mb-4">Upload neue Dokumente</h1>
      <UploadBox multiple onComplete={setLastResults} />
      <p className="mt-4 text-sm text-gray-600">
        PDF ohne extrahierbaren Text erfordern OCR via NiFi (später verfügbar)
      </p>
      {lastResults.length > 0 && (
        <div className="mt-4">
          <h2 className="font-semibold">Letzte Uploads</h2>
          <ul className="list-disc list-inside">
            {lastResults.map(r => (
              <li key={r.file}>{r.file} – {r.status}</li>
            ))}
          </ul>
        </div>
      )}
    </main>
  );
}
