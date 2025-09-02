import json
import urllib.parse
from typing import List, Dict

def superset_url(base: str, slug: str, filters: List[Dict]):
    state = {"native_filters": [], "time_range": "No filter"}
    for i, f in enumerate(filters):
        state["native_filters"].append({
            "id": f.get("id", f"auto-{i}"),
            "filterState": {"value": f.get("values"), "validateMessage": None},
            "targets": [{"column": f["column"], "datasetId": f["datasetId"]}],
            "type": "select",
        })
        if f.get("timeRange"):
            state["time_range"] = f["timeRange"]
    frag = urllib.parse.quote(json.dumps(state))
    return f"{base}/superset/dashboard/{slug}/?standalone=0#{frag}"
