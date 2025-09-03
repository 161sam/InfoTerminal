import { useEffect, useState } from 'react';
type Health = { web?:{ok:boolean}; searchApi?:{ok:boolean}; graphApi?:{ok:boolean} };
export function useHealth(){
  const [health,setHealth]=useState<Health>({}); const [loading,setLoading]=useState(true); const [error,setError]=useState<string|null>(null);
  useEffect(()=>{ let alive=true; (async()=>{
    try{
      const [web,searchApi,graphApi]=await Promise.all([
        fetch('/api/health').then(r=>({ok:r.ok})).catch(()=>({ok:false})),
        fetch(process.env.NEXT_PUBLIC_SEARCH_API_URL||'http://localhost:8081/health').then(r=>({ok:r.ok})).catch(()=>({ok:false})),
        fetch(process.env.NEXT_PUBLIC_GRAPH_API_URL||'http://localhost:8082/health').then(r=>({ok:r.ok})).catch(()=>({ok:false})),
      ]);
      if(!alive) return; setHealth({web,searchApi,graphApi}); setLoading(false);
    }catch(e:any){ if(!alive) return; setError(e?.message||'health failed'); setLoading(false); }
  })(); return ()=>{alive=false}; },[]);
  return {health,loading,error};
}
