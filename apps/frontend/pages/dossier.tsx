import { useState } from 'react';

export default function DossierPage() {
  const [title, setTitle] = useState('');
  const [docs, setDocs] = useState('');
  const [nodes, setNodes] = useState('');
  const [edges, setEdges] = useState('');
  const [markdown, setMarkdown] = useState('');
  const [pdf, setPdf] = useState('');

  const generate = async () => {
    const payload = {
      title,
      items: {
        docs: docs.split(',').map((s) => s.trim()).filter(Boolean),
        nodes: nodes.split(',').map((s) => s.trim()).filter(Boolean),
        edges: edges.split(',').map((s) => s.trim()).filter(Boolean),
      },
      options: { summary: false },
    };
    const res = await fetch('/dossier', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    setMarkdown(data.markdown || '');
    setPdf(data.pdfUrl || '');
  };

  return (
    <div className="p-4 space-y-2">
      <h1>Dossier Builder</h1>
      <input
        className="border p-1 block w-full"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Title"
      />
      <textarea
        className="border p-1 block w-full"
        value={docs}
        onChange={(e) => setDocs(e.target.value)}
        placeholder="Docs (comma separated)"
      />
      <textarea
        className="border p-1 block w-full"
        value={nodes}
        onChange={(e) => setNodes(e.target.value)}
        placeholder="Nodes (comma separated)"
      />
      <textarea
        className="border p-1 block w-full"
        value={edges}
        onChange={(e) => setEdges(e.target.value)}
        placeholder="Edges (comma separated)"
      />
      <button
        className="bg-blue-600 text-white px-2 py-1"
        onClick={generate}
        type="button"
      >
        Generate
      </button>
      {markdown && (
        <div className="mt-4">
          <h2>Markdown</h2>
          <pre
            data-testid="markdown-preview"
            className="border p-2 overflow-auto"
          >
            {markdown}
          </pre>
          {pdf && (
            <a href={pdf} download className="underline">
              Download PDF
            </a>
          )}
        </div>
      )}
    </div>
  );
}
