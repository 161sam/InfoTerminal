import { useState } from "react"

export default function NLPPage() {
  const [text, setText] = useState("")
  const [ner, setNer] = useState<any | null>(null)
  const [summary, setSummary] = useState<string>("")
  const [error, setError] = useState<string>("")

  const callNer = async () => {
    setError("")
    setSummary("")
    try {
      const r = await fetch("http://127.0.0.1:8003/ner", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      })
      if (!r.ok) throw new Error("bad")
      const j = await r.json()
      setNer(j)
    } catch (e) {
      setError("NLP-Service nicht verfügbar")
    }
  }

  const callSummarize = async () => {
    setError("")
    setNer(null)
    try {
      const r = await fetch("http://127.0.0.1:8003/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      })
      if (!r.ok) throw new Error("bad")
      const j = await r.json()
      setSummary(j.summary)
    } catch (e) {
      setError("NLP-Service nicht verfügbar")
    }
  }

  return (
    <main style={{maxWidth:800, margin:"40px auto", fontFamily:"ui-sans-serif"}}>
      <h1>NLP</h1>
      <textarea value={text} onChange={e=>setText(e.target.value)} rows={5} style={{width:"100%", padding:8}} placeholder="Text eingeben…" />
      <div style={{display:"flex", gap:8, marginTop:8}}>
        <button onClick={callNer}>Entitäten extrahieren</button>
        <button onClick={callSummarize}>Zusammenfassen</button>
      </div>
      {error && <div style={{color:"red", marginTop:8}}>{error}</div>}
      {ner && (
        <pre style={{background:"#f7f7f7", padding:8, marginTop:8}}>{JSON.stringify(ner, null, 2)}</pre>
      )}
      {summary && (
        <div style={{marginTop:8}}>
          <b>Zusammenfassung:</b>
          <p>{summary}</p>
        </div>
      )}
    </main>
  )
}
