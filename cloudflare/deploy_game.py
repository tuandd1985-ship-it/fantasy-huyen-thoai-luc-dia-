#!/usr/bin/env python3
"""Nap file game mot-file (ban xuat day du anh) vao KV FANTASY_GAME, key index_html.

Dung lai co che xac thuc cua cf.py (import call) — token khong bao gio in ra.
Chay: python3 deploy_game.py <duong-dan-file-html>
"""
import importlib.util
import sys

CF = "/home/hatch/workspace/custom-connectors/custom.cloudflare/bin/cf.py"
ACCOUNT = "7c67c2f7ba8966e7c54262681911d9aa"
NAMESPACE = "9d04805c4d5943a5bad996bc4d1d5058"  # FANTASY_GAME

spec = importlib.util.spec_from_file_location("cf", CF)
cf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cf)


def main():
    path = sys.argv[1]
    with open(path, "rb") as fh:
        data = fh.read()
    print(f"Uploading {len(data)} bytes -> KV key index_html ...")
    status, attached, payload = cf.call(
        "PUT",
        f"/accounts/{ACCOUNT}/storage/kv/namespaces/{NAMESPACE}/values/index_html",
        raw_body=data,
        content_type="text/html; charset=utf-8",
    )
    print("http_status:", status, "credential_attached:", attached,
          "success:", payload.get("success"), "errors:", payload.get("errors"))
    return 0 if payload.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
