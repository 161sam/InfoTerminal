
def test_ego_view(app_client, mock_driver):
    r = app_client.get(
        "/graphs/view/ego?label=Person&key=id&value=alice&depth=2&limit=50"
    )
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["counts"]["nodes"] >= 1
    assert data["counts"]["relationships"] >= 0


def test_shortest_path(app_client, mock_driver):
    r = app_client.get(
        "/graphs/view/shortest-path?src_label=Person&src_key=id&src_value=alice&dst_label=Person&dst_key=id&dst_value=bob&max_len=5"
    )
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["data"]["found"] is True
    assert data["data"]["path"]["length"] == 1
