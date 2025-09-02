import { useState } from "react"
import { signIn, signOut, useSession } from "next-auth/react"

export default function Home() {
  const { data: session } = useSession()
  const [q, setQ] = useState("")
  const [res, setRes] = useState<any[]>([])

  const search = async (e: any) => {
    e.preventDefault()
    const token = (session as any)?.accessToken || (session as any)?.user?.token
    const r = await fetch(`http://127.0.0.1:8001/search?q=${encodeURIComponent(q)}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {}
    })
    const j = await r.json()
    setRes(j)
  }

  return (
    <main style={{maxWidth:860, margin:"40px auto", fontFamily:"ui-sans-serif"}}>
      <h1>InfoTerminal</h1>
      <div style={{display:"flex", gap:8, marginBottom:12}}>
        {!session ? <button onClick={()=>signIn()}>Login</button> : <button onClick={()=>signOut()}>Logout</button>}
        <span>{session?.user?.name || session?.user?.email}</span>
      </div>
      <form onSubmit={search} style={{display:"flex", gap:8}}>
        <input value={q} onChange={e=>setQ(e.target.value)} placeholder="Search docs…" style={{flex:1, padding:8}}/>
        <button>Search</button>
      </form>
      <ul style={{marginTop:20}}>
        {res.map((r,i)=>(
          <li key={i} style={{marginBottom:12}}>
            <b>{r.title}</b><br/>
            <small>{r.score?.toFixed?.(2)}</small>
            <div>{r.body}</div>
            <div style={{marginTop:4}}>
              <a href={`http://127.0.0.1:8002/neighbors?node_id=${encodeURIComponent(r.id || r.title)}`} target="_blank">Graph neighbors</a>
            </div>
          </li>
        ))}
      </ul>
    </main>
  )
}
