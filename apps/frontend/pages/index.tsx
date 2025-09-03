import { useState, useMemo } from "react"
import { signIn, signOut, useSession } from "next-auth/react"

type FacetBucket = { key: string; count: number }
export default function Home() {
  const { data: session } = useSession()
  const [q, setQ] = useState("InfoTerminal")
  const [entityTypes, setEntityTypes] = useState<string[]>([])
  const [res, setRes] = useState<any[]>([])
  const [facets, setFacets] = useState<{entity_types:FacetBucket[]}>({entity_types:[]})

  const token = useMemo(() => (session as any)?.accessToken || (session as any)?.user?.token, [session])

  const search = async (e?: any) => {
    e?.preventDefault()
    const params = new URLSearchParams({ q })
    if (entityTypes.length) params.set("entity_type", entityTypes.join(","))
    const r = await fetch(`http://127.0.0.1:8001/search?${params.toString()}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {}
    })
    const j = await r.json()
    setRes(j.results || [])
    setFacets(j.facets || {entity_types:[]})
  }

  const toggleType = (t: string) => {
    setEntityTypes(prev => prev.includes(t) ? prev.filter(x=>x!==t) : [...prev, t])
  }

  return (
    <main style={{maxWidth:1100, margin:"40px auto", fontFamily:"ui-sans-serif"}}>
      <h1>InfoTerminal</h1>
      <div style={{display:"flex", gap:8, marginBottom:12}}>
        {!session ? <button onClick={()=>signIn()}>Login</button> : <button onClick={()=>signOut()}>Logout</button>}
        <span>{session?.user?.name || session?.user?.email}</span>
        <a href="/nlp">NLP</a>
      </div>

      <form onSubmit={search} style={{display:"flex", gap:8, marginBottom:10}}>
        <input value={q} onChange={e=>setQ(e.target.value)} placeholder="Search…" style={{flex:1, padding:8}}/>
        <button>Search</button>
      </form>

      <div style={{display:"grid", gridTemplateColumns:"250px 1fr", gap:16}}>
        <aside style={{border:"1px solid #eee", padding:10, borderRadius:8}}>
          <b>Facetten</b>
          <div style={{marginTop:8}}>
            <div style={{fontSize:12, opacity:.7}}>Entity Types</div>
            {facets.entity_types.map(b=>(
              <label key={b.key} style={{display:"flex", alignItems:"center", gap:6}}>
                <input type="checkbox" checked={entityTypes.includes(b.key)} onChange={()=>toggleType(b.key)}/>
                <span>{b.key} <small style={{opacity:.6}}>({b.count})</small></span>
              </label>
            ))}
          </div>
          <button style={{marginTop:10}} onClick={()=>search()}>Filter anwenden</button>
        </aside>

        <section>
          <ul data-testid="search-results" style={{marginTop:0}}>
            {res.map((r,i)=>(
              <li key={i} style={{marginBottom:12, paddingBottom:12, borderBottom:"1px solid #eee"}}>
                <b>{r.title}</b><br/>
                <small>{r.score?.toFixed?.(2)}</small>
                <div>{r.body}</div>
                <div style={{marginTop:4}}>
                  <a href={`http://127.0.0.1:8002/neighbors?node_id=${encodeURIComponent(r.id || r.title)}`} target="_blank">Graph neighbors</a>
                </div>
              </li>
            ))}
          </ul>
        </section>
      </div>
    </main>
  )
}
