import json, os, time
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT=int(os.getenv("PORT","9108"))
DIR=os.getenv("DBT_DIR","etl/dbt/target")

def load_metrics():
    m=[]
    try:
        rr=json.load(open(f"{DIR}/run_results.json"))
        failed=sum(1 for r in rr.get("results",[]) if r.get("status") not in ("success","skipped"))
        total=len(rr.get("results",[]))
        m.append(("dbt_tests_total", total))
        m.append(("dbt_tests_failed", failed))
    except: pass
    try:
        src=json.load(open(f"{DIR}/sources.json"))
        for ts in src.get("sources",[]):
            n=ts["unique_id"].replace(".","_")
            stale=1 if ts.get("max_loaded_at_time_ago_in_s",0) > ts.get("freshness",{}).get("warn_after",{}).get("count", 86400) else 0
            m.append((f"dbt_source_stale{{source=\"{n}\"}}", stale))
    except: pass
    return m

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path!="/metrics":
            self.send_response(404); self.end_headers(); return
        ms=load_metrics()
        out="\n".join([f"# HELP {k} .\n# TYPE {k} gauge\n{k} {v}" for k,v in ms])+"\n"
        self.send_response(200); self.send_header("Content-Type","text/plain"); self.end_headers()
        self.wfile.write(out.encode())

if __name__=="__main__":
    HTTPServer(("0.0.0.0", PORT), H).serve_forever()

