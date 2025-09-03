// TODO: consolidate with pages/graphx.tsx; graphx.tsx should be the canonical view.
import { useEffect, useMemo, useState } from "react"
import CytoscapeComponent from "react-cytoscapejs"

type Edge = { from: any; to: any; rel: string }
export default function GraphPage() {
  const [nodeId, setNodeId] = useState("P:alice")
  const [edges, setEdges] = useState<Edge[]>([])
  const fetchNeighbors = async () => {
    const r = await fetch(`http://127.0.0.1:8002/neighbors?node_id=${encodeURIComponent(nodeId)}&limit=50`)
    const j = await r.json()
    setEdges(j)
  }
  useEffect(() => { fetchNeighbors() }, [])
  const elements = useMemo(() => {
    const nset = new Map<string, any>()
    const es: any[] = []
    for (const e of edges) {
      const a = e.from.id || e.from.name, b = e.to.id || e.to.name
      if (!nset.has(a)) nset.set(a, { data: { id: a, label: e.from.name || a } })
      if (!nset.has(b)) nset.set(b, { data: { id: b, label: e.to.name || b } })
      es.push({ data: { id: `${a}-${e.rel}-${b}`, source: a, target: b, label: e.rel } })
    }
    return [...nset.values(), ...es]
  }, [edges])
  return (
    <main data-testid="graph-view" style={{maxWidth:1100, margin:"30px auto", fontFamily:"ui-sans-serif"}}>
      <h1>Graph Viewer</h1>
      <form onSubmit={e=>{e.preventDefault(); fetchNeighbors()}} style={{display:"flex", gap:8, marginBottom:12}}>
        <input value={nodeId} onChange={e=>setNodeId(e.target.value)} placeholder="Node-ID (z.B. P:alice)" style={{flex:1, padding:8}}/>
        <button>Load</button>
      </form>
      <CytoscapeComponent
        elements={elements as any}
        style={{ width: '100%', height: '70vh', border:"1px solid #ddd", borderRadius:8 }}
        layout={{ name: "cose", fit: true, padding: 20, animate: false }}
        stylesheet={[
          { selector: "node", style: { "background-color": "#888", label: "data(label)", "font-size":"10px" } },
          { selector: "edge", style: { "curve-style":"bezier", "target-arrow-shape":"vee", label:"data(label)", "font-size":"8px" } },
        ]}
      />
    </main>
  )
}
