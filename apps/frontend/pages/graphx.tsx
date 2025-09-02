import { useEffect, useMemo, useRef, useState } from "react"
import CytoscapeComponent from "react-cytoscapejs"

type Edge = { from: any; to: any; rel: string }
type Elem = { data: any; position?: any; locked?: boolean }

const STORAGE_KEY = "infoterminal.graph.view"
const API = "http://127.0.0.1:8004"
async function saveServer(name:string, elems:any[], pos:any) {
  const nodes = elems.filter((e:any)=>e.data && !e.data.source).map((e:any)=>e.data)
  const edges = elems.filter((e:any)=>e.data && e.data.source).map((e:any)=>e.data)
  const r = await fetch(`${API}/views`, {method:"POST", headers:{"content-type":"application/json","x-user":"dev"}, body: JSON.stringify({name, nodes, edges, positions: pos})})
  return r.json()
}
async function listServer(){ const r = await fetch(`${API}/views`, {headers:{"x-user":"dev"}}); return r.json() }
async function loadServer(id:number){ const r=await fetch(`${API}/views/${id}`, {headers:{"x-user":"dev"}}); return r.json() }

export default function GraphX() {
  const cyRef = useRef<any>(null)
  const [elements, setElements] = useState<Elem[]>([])
  const [seed, setSeed] = useState("P:alice")
  const [loading, setLoading] = useState(false)
  const [views, setViews] = useState<any[]>([])
  const [viewName, setViewName] = useState("My View")

  useEffect(()=> {
    // try load saved
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      const obj = JSON.parse(saved)
      setElements(obj.elements || [])
      setTimeout(()=>applyPositions(obj.positions||{}), 0)
    } else {
      expand(seed)
    }
    // eslint-disable-next-line
  }, [])

  const applyPositions = (pos: Record<string,{x:number,y:number}>) => {
    const cy = cyRef.current
    if (!cy) return
    Object.entries(pos).forEach(([id,p])=>{
      const n = cy.getElementById(id)
      if (n) { n.position(p); n.lock(); }
    })
  }

  const getPositions = () => {
    const cy = cyRef.current
    const pos: Record<string,{x:number,y:number}> = {}
    cy.nodes().forEach((n:any)=> { pos[n.id()] = n.position() })
    return pos
  }

  const ensureNode = (arr: Elem[], id: string, label?: string) => {
    if (arr.find(e => e.data?.id===id)) return
    arr.push({ data:{ id, label: label || id } })
  }

  const ensureEdge = (arr: Elem[], a: string, b: string, rel: string) => {
    const eid = `${a}-${rel}-${b}`
    if (arr.find(e => e.data?.id===eid)) return
    arr.push({ data:{ id: eid, source: a, target: b, label: rel } })
  }

  const expand = async (nodeId: string) => {
    setLoading(true)
    try {
      const r = await fetch(`http://127.0.0.1:8002/neighbors?node_id=${encodeURIComponent(nodeId)}&limit=200`)
      const edges: Edge[] = await r.json()
      const next = elements.slice()
      for (const e of edges) {
        const a = e.from.id || e.from.name, b = e.to.id || e.to.name
        ensureNode(next, a, e.from.name)
        ensureNode(next, b, e.to.name)
        ensureEdge(next, a, b, e.rel)
      }
      setElements(next)
      setTimeout(()=>layout(), 0)
    } finally { setLoading(false) }
  }

  const layout = () => {
    const cy = cyRef.current
    cy?.layout({ name: "cose", fit: true, animate: false, padding: 20 }).run()
  }

  const togglePin = (id: string) => {
    const cy = cyRef.current
    const n = cy.getElementById(id)
    if (!n) return
    if (n.locked()) n.unlock(); else n.lock()
  }

  const saveView = () => {
    const obj = { elements, positions: getPositions() }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(obj))
    alert("Saved.")
  }

  const loadView = () => {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (!saved) return
    const obj = JSON.parse(saved)
    setElements(obj.elements || [])
    setTimeout(()=>applyPositions(obj.positions||{}), 0)
  }

  const reset = () => { setElements([]); setTimeout(()=>expand(seed),0) }

  return (
    <main style={{maxWidth:1200, margin:"30px auto", fontFamily:"ui-sans-serif"}}>
      <h1>Graph Viewer (expand / pin / save)</h1>
      <div style={{display:"flex", gap:8, marginBottom:10}}>
        <input value={seed} onChange={e=>setSeed(e.target.value)} placeholder="Seed node id" style={{flex:1,padding:8}}/>
        <button onClick={()=>expand(seed)} disabled={loading}>{loading ? "…" : "Expand"}</button>
        <button onClick={layout}>Relayout</button>
        <button onClick={saveView}>Save</button>
        <button onClick={loadView}>Load</button>
        <button onClick={async ()=>{
          const res = await saveServer(viewName, elements, getPositions())
          alert(`Saved on server id=${res.id}`)
        }}>Save Server</button>
        <button onClick={async ()=>{
          const j = await listServer(); setViews(j)
        }}>List</button>
        <select onChange={async (e)=>{
          const j = await loadServer(parseInt(e.target.value,10))
          setElements([...j.nodes.map((n:any)=>({data:n})), ...j.edges.map((e:any)=>({data:e}))])
          setTimeout(()=>applyPositions(j.positions||{}),0)
        }}>
          <option>-- choose view --</option>
          {views.map(v=><option key={v.id} value={v.id}>{v.name} #{v.id}</option>)}
        </select>
        <input value={viewName} onChange={e=>setViewName(e.target.value)} style={{width:180}}/>
        <button onClick={reset}>Reset</button>
      </div>
      <p style={{opacity:.7, marginTop:-6}}>Tip: double-click a node to pin/unpin.</p>
      <CytoscapeComponent
        cy={(cy:any)=>{ cyRef.current = cy; cy.on("dbltap","node",(evt:any)=> togglePin(evt.target.id())) }}
        elements={elements as any}
        style={{ width: '100%', height: '72vh', border:"1px solid #ddd", borderRadius:8 }}
        layout={{ name: "cose", fit: true, padding: 20, animate: false }}
        stylesheet={[
          { selector: "node", style: { "background-color": "#999", "label":"data(label)", "font-size":"10px" } },
          { selector: "edge", style: { "curve-style":"bezier", "target-arrow-shape":"vee", "label":"data(label)", "font-size":"8px" } },
          { selector: "node:locked", style: { "border-width":2, "border-color":"#333" } }
        ]}
      />
    </main>
  )
}
