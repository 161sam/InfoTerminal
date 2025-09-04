// apps/frontend/pages/graphx.tsx

import { useEffect, useMemo, useRef, useState } from "react"
import CytoscapeComponent from "react-cytoscapejs"
import { config } from '../lib/config'

type Edge = { from: any; to: any; rel: string }
type Elem = { data: any; position?: any; locked?: boolean }

const STORAGE_KEY = "infoterminal.graph.view"

// Use configuration instead of hardcoded URLs
const GRAPH_API = config.GRAPH_API
const VIEWS_API = config.VIEWS_API
if (!GRAPH_API) {
  console.warn("GRAPH_API missing; falling back to http://localhost:8612")
}

// Mock data for when APIs are not available
const MOCK_EDGES: Edge[] = [
  { from: { id: "P:alice", name: "Alice" }, to: { id: "O:acme", name: "ACME Corp" }, rel: "works_at" },
  { from: { id: "O:acme", name: "ACME Corp" }, to: { id: "L:london", name: "London" }, rel: "located_in" },
  { from: { id: "P:alice", name: "Alice" }, to: { id: "P:bob", name: "Bob" }, rel: "knows" },
]

async function saveServer(name: string, elems: any[], pos: any) {
  try {
    const nodes = elems.filter((e: any) => e.data && !e.data.source).map((e: any) => e.data)
    const edges = elems.filter((e: any) => e.data && e.data.source).map((e: any) => e.data)
    const r = await fetch(`${VIEWS_API}/views`, {
      method: "POST", 
      headers: { "content-type": "application/json", "x-user": "dev" }, 
      body: JSON.stringify({ name, nodes, edges, positions: pos })
    })
    if (!r.ok) throw new Error(`HTTP ${r.status}`)
    return r.json()
  } catch (error) {
    console.error('Save to server failed:', error)
    // Fallback: save to localStorage
    const data = { name, elements: elems, positions: pos }
    localStorage.setItem(`${STORAGE_KEY}.${name}`, JSON.stringify(data))
    return { id: Date.now(), saved_locally: true }
  }
}

async function listServer() { 
  try {
    const r = await fetch(`${VIEWS_API}/views`, { headers: { "x-user": "dev" } })
    if (!r.ok) throw new Error(`HTTP ${r.status}`)
    return r.json()
  } catch (error) {
    console.error('List views failed:', error)
    // Fallback: return local saves
    const localViews = []
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i)
      if (key?.startsWith(`${STORAGE_KEY}.`)) {
        const name = key.replace(`${STORAGE_KEY}.`, '')
        localViews.push({ id: i, name, local: true })
      }
    }
    return localViews
  }
}

async function loadServer(id: number) {
  try {
    const r = await fetch(`${VIEWS_API}/views/${id}`, { headers: { "x-user": "dev" } })
    if (!r.ok) throw new Error(`HTTP ${r.status}`)
    return r.json()
  } catch (error) {
    console.error('Load view failed:', error)
    throw error
  }
}

export default function GraphX() {
  const cyRef = useRef<any>(null)
  const [elements, setElements] = useState<Elem[]>([])
  const [seed, setSeed] = useState("P:alice")
  const [loading, setLoading] = useState(false)
  const [views, setViews] = useState<any[]>([])
  const [viewName, setViewName] = useState("My View")
  const [error, setError] = useState<string>("")

  useEffect(() => {
    // Try load saved
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      try {
        const obj = JSON.parse(saved)
        setElements(obj.elements || [])
        setTimeout(() => applyPositions(obj.positions || {}), 0)
      } catch (e) {
        console.error('Failed to load saved graph:', e)
        expand(seed)
      }
    } else {
      expand(seed)
    }
    // eslint-disable-next-line
  }, [])

  const applyPositions = (pos: Record<string, { x: number, y: number }>) => {
    const cy = cyRef.current
    if (!cy) return
    Object.entries(pos).forEach(([id, p]) => {
      const n = cy.getElementById(id)
      if (n.length > 0) { 
        n.position(p) 
        n.lock() 
      }
    })
  }

  const getPositions = () => {
    const cy = cyRef.current
    if (!cy) return {}
    const pos: Record<string, { x: number, y: number }> = {}
    cy.nodes().forEach((n: any) => { 
      pos[n.id()] = n.position() 
    })
    return pos
  }

  const ensureNode = (arr: Elem[], id: string, label?: string) => {
    if (arr.find(e => e.data?.id === id)) return
    arr.push({ data: { id, label: label || id } })
  }

  const ensureEdge = (arr: Elem[], a: string, b: string, rel: string) => {
    const eid = `${a}-${rel}-${b}`
    if (arr.find(e => e.data?.id === eid)) return
    arr.push({ data: { id: eid, source: a, target: b, label: rel } })
  }

  const expand = async (nodeId: string) => {
    setLoading(true)
    setError("")
    
    try {
      const url = `${GRAPH_API}/neighbors?node_id=${encodeURIComponent(nodeId)}&limit=200`
      const r = await fetch(url)
      
      let edges: Edge[] = []
      
      if (!r.ok) {
        console.warn(`Graph API not available (${r.status}), using mock data`)
        // Use mock data when API is not available
        edges = MOCK_EDGES.filter(e => 
          e.from.id === nodeId || e.to.id === nodeId
        )
      } else {
        edges = await r.json()
      }

      const next = elements.slice()
      
      for (const e of edges) {
        const a = e.from.id || e.from.name
        const b = e.to.id || e.to.name
        ensureNode(next, a, e.from.name)
        ensureNode(next, b, e.to.name)
        ensureEdge(next, a, b, e.rel)
      }
      
      setElements(next)
      setTimeout(() => layout(), 0)
      
    } catch (error) {
      console.error('Expand failed:', error)
      setError(error instanceof Error ? error.message : 'Failed to expand graph')
      
      // Fallback to mock data
      const next = elements.slice()
      for (const e of MOCK_EDGES) {
        const a = e.from.id || e.from.name
        const b = e.to.id || e.to.name
        ensureNode(next, a, e.from.name)
        ensureNode(next, b, e.to.name)
        ensureEdge(next, a, b, e.rel)
      }
      setElements(next)
      setTimeout(() => layout(), 0)
      
    } finally { 
      setLoading(false) 
    }
  }

  const layout = () => {
    const cy = cyRef.current
    if (cy) {
      cy.layout({ 
        name: "cose", 
        fit: true, 
        animate: false, 
        padding: 20,
        nodeRepulsion: 10000,
        edgeElasticity: 100
      }).run()
    }
  }

  const togglePin = (id: string) => {
    const cy = cyRef.current
    if (!cy) return
    const n = cy.getElementById(id)
    if (!n.length) return
    if (n.locked()) n.unlock()
    else n.lock()
  }

  const saveView = async () => {
    try {
      const obj = { elements, positions: getPositions() }
      localStorage.setItem(STORAGE_KEY, JSON.stringify(obj))
      
      const result = await saveServer(viewName, elements, getPositions())
      if (result.saved_locally) {
        alert(`Saved locally as "${viewName}"`)
      } else {
        alert(`Saved on server with ID: ${result.id}`)
      }
      
      loadViewsList()
    } catch (error) {
      console.error('Save failed:', error)
      alert('Save failed')
    }
  }

  const loadView = () => {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (!saved) {
      alert('No saved view found')
      return
    }
    try {
      const obj = JSON.parse(saved)
      setElements(obj.elements || [])
      setTimeout(() => applyPositions(obj.positions || {}), 0)
    } catch (e) {
      console.error('Failed to load view:', e)
      alert('Failed to load view')
    }
  }

  const loadViewsList = async () => {
    try {
      const viewsList = await listServer()
      setViews(viewsList)
    } catch (error) {
      console.error('Failed to load views list:', error)
    }
  }

  const reset = () => { 
    setElements([])
    setError("")
    setTimeout(() => expand(seed), 0) 
  }

  return (
    <main style={{ maxWidth: 1200, margin: "30px auto", fontFamily: "ui-sans-serif" }}>
      <h1 className="text-2xl font-semibold">Graph Viewer (expand / pin / save)</h1>
      
      {error && (
        <div style={{ 
          background: "#fef2f2", 
          border: "1px solid #fecaca", 
          color: "#dc2626", 
          padding: "12px", 
          borderRadius: "8px", 
          marginBottom: "16px" 
        }}>
          {error}
        </div>
      )}
      
      <div style={{ display: "flex", gap: 8, marginBottom: 10, flexWrap: "wrap" }}>
        <input 
          value={seed} 
          onChange={e => setSeed(e.target.value)} 
          placeholder="Seed node id" 
          style={{ flex: 1, padding: 8, minWidth: 200 }}
        />
        <button onClick={() => expand(seed)} disabled={loading}>
          {loading ? "Loading..." : "Expand"}
        </button>
        <button onClick={layout}>Relayout</button>
        <button onClick={saveView}>Save</button>
        <button onClick={loadView}>Load</button>
        <button onClick={saveView}>Save Server</button>
        <button onClick={loadViewsList}>List Views</button>
        <select onChange={async (e) => {
          if (!e.target.value) return
          try {
            const j = await loadServer(parseInt(e.target.value, 10))
            setElements([
              ...j.nodes.map((n: any) => ({ data: n })), 
              ...j.edges.map((e: any) => ({ data: e }))
            ])
            setTimeout(() => applyPositions(j.positions || {}), 0)
          } catch (error) {
            alert('Failed to load view')
          }
        }}>
          <option value="">-- choose view --</option>
          {views.map(v => (
            <option key={v.id} value={v.id}>
              {v.name} #{v.id} {v.local ? '(local)' : ''}
            </option>
          ))}
        </select>
        <input 
          value={viewName} 
          onChange={e => setViewName(e.target.value)} 
          style={{ width: 180 }}
          placeholder="View name"
        />
        <button onClick={reset}>Reset</button>
      </div>
      
      <p style={{ opacity: .7, marginTop: -6 }}>
        Tip: double-click a node to pin/unpin.
      </p>
      
      <div 
        data-testid="graph-view" 
        style={{ 
          width: '100%', 
          height: '72vh', 
          border: "1px solid #ddd", 
          borderRadius: 8 
        }}
      >
        <CytoscapeComponent
          cy={(cy: any) => { 
            cyRef.current = cy
            cy.on("dbltap", "node", (evt: any) => togglePin(evt.target.id())) 
          }}
          elements={elements as any}
          style={{ width: '100%', height: '100%' }}
          layout={{ name: "cose", fit: true, padding: 20, animate: false }}
          stylesheet={[
            { 
              selector: "node", 
              style: { 
                "background-color": "#666", 
                "label": "data(label)", 
                "font-size": "12px",
                "text-outline-width": "2px",
                "text-outline-color": "#fff",
                "width": "30px",
                "height": "30px"
              } 
            },
            { 
              selector: "edge", 
              style: { 
                "curve-style": "bezier", 
                "target-arrow-shape": "vee", 
                "label": "data(label)", 
                "font-size": "10px",
                "line-color": "#999",
                "target-arrow-color": "#999"
              } 
            },
            { 
              selector: "node:locked", 
              style: { 
                "border-width": 3, 
                "border-color": "#333",
                "background-color": "#ff6b6b"
              } 
            }
          ]}
        />
      </div>
    </main>
  )
}
