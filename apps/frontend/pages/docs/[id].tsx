import { useRouter } from "next/router"
import { useEffect, useState } from "react"

export default function DocPage(){
  const { query } = useRouter()
  const id = (query.id as string) || ""
  const [html,setHtml] = useState<string>("")
  useEffect(()=>{
    if(!id) return
    fetch(`http://127.0.0.1:8006/docs/${encodeURIComponent(id)}/html`)
      .then(r=>r.text()).then(setHtml)
  },[id])
  return (
    <main style={{maxWidth:920, margin:"24px auto"}}>
      <div dangerouslySetInnerHTML={{__html: html}} />
    </main>
  )
}
