import os, time, random, string, json, requests

BASE = os.getenv("BASE","http://127.0.0.1")
SEARCH = os.getenv("SEARCH", f"{BASE}:8001")
GRAPH  = os.getenv("GRAPH",  f"{BASE}:8002")
EDGE_SEARCH = os.getenv("EDGE_SEARCH","http://search.127.0.0.1.nip.io")
USERS = [
  {"username":"alice","roles":["analyst"],"tenant":"A"},
  {"username":"bob","roles":["investigator"],"tenant":"A"},
  {"username":"carol","roles":["analyst"],"tenant":"B"},
  {"username":"root","roles":["admin"],"tenant":"*"}
]

def call_search_direct(q, user):
  payload = {"q": q}
  headers = {"X-Demo-User": json.dumps(user)}  # falls du das im Gateway in OPA input mappen willst
  return requests.get(f"{SEARCH}/search", params=payload, headers=headers, timeout=5)

def call_search_edge(q):
  # über Edge → OIDC/OPA; für Demo ggf. ohne Auth -> erwartet 401/302
  return requests.get(f"{EDGE_SEARCH}/search", params={"q":q}, timeout=5, allow_redirects=False)

def call_graph_neighbors(node_id, user):
  headers = {"X-Demo-User": json.dumps(user)}
  return requests.get(f"{GRAPH}/neighbors", params={"node_id":node_id,"limit":50}, headers=headers, timeout=5)

def rnd_word(n=5):
  import random, string
  return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))

def run_once():
  # 1) erlaubt/beleidigt über OPA → Denies erzeugen
  try:
    r = call_search_edge("info")
    print("edge search:", r.status_code)
  except Exception as e:
    print("edge error:", e)

  # 2) direkte API (mit X-Demo-User → OPA input mapper)
  u = random.choice(USERS)
  q = random.choice(["acme", "berlin", "sap", "investigation", rnd_word(6)])
  rs = call_search_direct(q, u)
  print("direct search", u["username"], q, rs.status_code)

  # 3) graph neighbors
  node = random.choice(["P:alice","O:acme","A:SAP.DE"])
  rg = call_graph_neighbors(node, u)
  print("graph", u["username"], node, rg.status_code)

def main():
  iters = int(os.getenv("ITERS","60"))
  delay = float(os.getenv("DELAY","1.5"))
  for i in range(iters):
    run_once()
    time.sleep(delay)

if __name__ == "__main__":
  main()
