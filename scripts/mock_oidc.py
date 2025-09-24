#!/usr/bin/env python3
"""Minimal mock OIDC provider for local smoke tests."""
from __future__ import annotations

import base64
import json
import os
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict

ISSUER = os.environ.get("MOCK_OIDC_ISSUER", "http://localhost:8089/realms/mock")
PORT = int(os.environ.get("MOCK_OIDC_PORT", "8089"))
CLIENT_ID = os.environ.get("MOCK_OIDC_CLIENT_ID", "infoterminal-frontend")
REALM_PATH = urllib.parse.urlparse(ISSUER).path or "/realms/mock"


def _build_url(path: str) -> str:
  return f"{ISSUER.rstrip('/')}/{path.lstrip('/')}"


def _encode_segment(data: Dict[str, object]) -> str:
  raw = json.dumps(data, separators=(",", ":")).encode("utf-8")
  return base64.urlsafe_b64encode(raw).decode("utf-8").rstrip("=")


def _id_token() -> str:
  now = int(time.time())
  header = _encode_segment({"alg": "none"})
  payload = _encode_segment(
    {
      "iss": ISSUER,
      "aud": CLIENT_ID,
      "sub": "mock-user-123",
      "email": "demo.user@example.com",
      "name": "Demo User",
      "preferred_username": "demo.user",
      "realm_access": {"roles": ["analyst", "admin"]},
      "auth_time": now,
      "iat": now,
      "exp": now + 600,
    }
  )
  return f"{header}.{payload}."


class MockOIDCHandler(BaseHTTPRequestHandler):
  server_version = "MockOIDC/1.0"

  def log_message(self, format: str, *args) -> None:  # noqa: A003 - keep quiet
    if os.environ.get("MOCK_OIDC_VERBOSE"):
      super().log_message(format, *args)

  def _send_json(self, payload: Dict[str, object], status: int = 200) -> None:
    body = json.dumps(payload).encode("utf-8")
    self.send_response(status)
    self.send_header("Content-Type", "application/json")
    self.send_header("Cache-Control", "no-store")
    self.send_header("Content-Length", str(len(body)))
    self.end_headers()
    self.wfile.write(body)

  def do_GET(self) -> None:  # noqa: N802 (http method name)
    parsed = urllib.parse.urlparse(self.path)
    if parsed.path == f"{REALM_PATH}/.well-known/openid-configuration":
      self._send_json(
        {
          "issuer": ISSUER,
          "authorization_endpoint": _build_url("protocol/openid-connect/auth"),
          "token_endpoint": _build_url("protocol/openid-connect/token"),
          "userinfo_endpoint": _build_url("protocol/openid-connect/userinfo"),
          "end_session_endpoint": _build_url("protocol/openid-connect/logout"),
          "jwks_uri": _build_url("protocol/openid-connect/certs"),
        }
      )
      return

    if parsed.path == f"{REALM_PATH}/protocol/openid-connect/auth":
      params = urllib.parse.parse_qs(parsed.query)
      redirect_uri = params.get("redirect_uri", [""])[0]
      state = params.get("state", [""])[0]
      response_params = {"code": "mock-code", "state": state}
      location = redirect_uri
      separator = "&" if "?" in redirect_uri else "?"
      location = f"{redirect_uri}{separator}{urllib.parse.urlencode(response_params)}"
      self.send_response(302)
      self.send_header("Location", location)
      self.end_headers()
      return

    if parsed.path == f"{REALM_PATH}/protocol/openid-connect/userinfo":
      self._send_json(
        {
          "sub": "mock-user-123",
          "email": "demo.user@example.com",
          "name": "Demo User",
          "preferred_username": "demo.user",
          "roles": ["analyst", "admin"],
        }
      )
      return

    if parsed.path == f"{REALM_PATH}/protocol/openid-connect/logout":
      self.send_response(204)
      self.end_headers()
      return

    self.send_response(404)
    self.end_headers()

  def do_POST(self) -> None:  # noqa: N802 (http method name)
    parsed = urllib.parse.urlparse(self.path)
    if parsed.path != f"{REALM_PATH}/protocol/openid-connect/token":
      self.send_response(404)
      self.end_headers()
      return

    length = int(self.headers.get("Content-Length", "0"))
    body = self.rfile.read(length).decode("utf-8")
    params = urllib.parse.parse_qs(body)
    grant_type = params.get("grant_type", [""])[0]

    if grant_type not in {"authorization_code", "refresh_token"}:
      self._send_json({"error": "unsupported_grant_type"}, status=400)
      return

    response = {
      "access_token": "mock-access-token",
      "refresh_token": "mock-refresh-token",
      "token_type": "Bearer",
      "expires_in": 300,
      "refresh_expires_in": 3600,
      "scope": "openid profile email",
      "id_token": _id_token(),
    }
    self._send_json(response)


def main() -> None:
  server = HTTPServer(("", PORT), MockOIDCHandler)
  print(f"Mock OIDC server running at http://localhost:{PORT} (issuer: {ISSUER})")
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    print("\nStopping mock OIDC server")
    server.server_close()


if __name__ == "__main__":
  main()
