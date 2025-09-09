from response import ok, err, bool_qp, safe_counts


def test_ok_err_boolqp():
    o = ok({"x": 1}, {"nodes": 1})
    assert o["ok"] and o["data"]["x"] == 1 and o["counts"]["nodes"] == 1
    b, _ = err("bad_request", "x", 400)
    assert b["ok"] is False and b["error"]["code"] == "bad_request"
    assert bool_qp("1") and bool_qp("true") and not bool_qp("0")


class C:  # fake neo4j counters
    nodes_created = 2
    nodes_deleted = 0
    relationships_created = 3

def test_safe_counts():
    sc = safe_counts(C())
    assert sc["nodes"] == 2 and sc["relationships"] == 3
