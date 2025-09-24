import { useState } from "react";
import { useRouter } from "next/router";

export default function DocumentUploader() {
  const [tab, setTab] = useState<"file" | "text">("file");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleFileSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    setLoading(true);
    try {
      const res = await fetch("/api/docs/upload", { method: "POST", body: formData });
      if (!res.ok) throw new Error("Upload failed");
      const data = await res.json();
      router.push(`/docs/${data.id}`);
    } catch (err) {
      alert("Upload fehlgeschlagen");
    } finally {
      setLoading(false);
    }
  }

  async function handleTextSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const text = (form.elements.namedItem("text") as HTMLTextAreaElement).value;
    const title = (form.elements.namedItem("title") as HTMLInputElement).value;
    setLoading(true);
    try {
      const res = await fetch("/api/docs/annotate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, title }),
      });
      if (!res.ok) throw new Error("Annotate failed");
      const data = await res.json();
      router.push(`/docs/${data.id}`);
    } catch (err) {
      alert("Annotation fehlgeschlagen");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <div style={{ marginBottom: "1rem" }}>
        <button onClick={() => setTab("file")} disabled={tab === "file"}>
          Datei hochladen
        </button>
        <button onClick={() => setTab("text")} disabled={tab === "text"}>
          Text einfügen
        </button>
      </div>
      {tab === "file" ? (
        <form onSubmit={handleFileSubmit}>
          <input type="file" name="file" accept=".pdf,.txt" required />
          <input type="text" name="title" placeholder="Titel" />
          <button type="submit" disabled={loading}>
            {loading ? "Lade..." : "Upload"}
          </button>
        </form>
      ) : (
        <form onSubmit={handleTextSubmit}>
          <input type="text" name="title" placeholder="Titel" />
          <textarea name="text" rows={6} required />
          <button type="submit" disabled={loading}>
            {loading ? "Lade..." : "Annotieren"}
          </button>
        </form>
      )}
    </div>
  );
}
