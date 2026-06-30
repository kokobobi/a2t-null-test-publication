#!/usr/bin/env python3
"""Verify the public A2T Mode B content-publication bundle.

This verifier is intentionally self-contained: it uses only the Python standard
library plus the local `git` executable for `git bundle verify`. It downloads
the remote manifest and base64 chunk files, reconstructs the git bundle in a
temporary directory, checks all recorded SHA-256 values and sizes, and then asks
Git to verify the reconstructed bundle.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import urljoin
from urllib.request import urlopen


DEFAULT_MANIFEST = (
    "https://raw.githubusercontent.com/kokobobi/hello-world/main/"
    "data/content_publication_bundle_20260630/"
    "a2t_content_publication_bundle_manifest_20260630.json"
)
DEFAULT_CHUNKS_ROOT = (
    "https://raw.githubusercontent.com/kokobobi/hello-world/main/"
    "data/content_publication_bundle_20260630"
)


def read_url(url: str) -> bytes:
    with urlopen(url, timeout=90) as response:  # nosec: public verifier URL
        return response.read()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_git_bundle(bundle_path: Path) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="a2t_bundle_verify_repo_") as tmp:
        repo = Path(tmp)
        init = subprocess.run(
            ["git", "init"],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if init.returncode != 0:
            return {
                "ok": False,
                "command": "git init",
                "stdout": init.stdout.strip(),
                "stderr": init.stderr.strip(),
                "returncode": init.returncode,
            }
        proc = subprocess.run(
            ["git", "bundle", "verify", str(bundle_path)],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    return {
        "ok": proc.returncode == 0,
        "command": f"git bundle verify {bundle_path}",
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "returncode": proc.returncode,
    }


def verify(args: argparse.Namespace) -> dict[str, Any]:
    manifest = json.loads(read_url(args.manifest).decode("utf-8"))
    chunks = manifest.get("chunks") or []
    with tempfile.TemporaryDirectory(prefix="a2t_remote_bundle_") as tmp:
        bundle_path = Path(tmp) / "a2t-publication.bundle"
        rows = []
        all_chunks_ok = True
        with bundle_path.open("wb") as out:
            for chunk in chunks:
                filename = str(chunk["filename"])
                location = urljoin(args.chunks_root.rstrip("/") + "/", "chunks/" + filename)
                encoded = read_url(location).strip()
                encoded_sha = sha256_bytes(encoded)
                try:
                    raw = base64.b64decode(encoded, validate=True)
                    decode_error = None
                except Exception as exc:  # pragma: no cover - diagnostic path
                    raw = b""
                    decode_error = str(exc)
                raw_sha = sha256_bytes(raw)
                row = {
                    "index": chunk.get("index"),
                    "filename": filename,
                    "location": location,
                    "base64_sha256_ok": encoded_sha == chunk.get("base64_sha256"),
                    "raw_sha256_ok": raw_sha == chunk.get("raw_sha256"),
                    "raw_size_ok": len(raw) == chunk.get("raw_size_bytes"),
                    "decode_error": decode_error,
                }
                row["ok"] = bool(
                    row["base64_sha256_ok"]
                    and row["raw_sha256_ok"]
                    and row["raw_size_ok"]
                    and decode_error is None
                )
                all_chunks_ok = all_chunks_ok and row["ok"]
                rows.append(row)
                out.write(raw)

        reconstructed_sha = sha256_file(bundle_path)
        reconstructed_size = bundle_path.stat().st_size
        git_bundle_verify = verify_git_bundle(bundle_path)

    report = {
        "schema": "a2t_public_remote_bundle_verification_v1",
        "manifest": args.manifest,
        "chunks_root": args.chunks_root,
        "expected_bundle_sha256": manifest.get("bundle_sha256"),
        "reconstructed_sha256": reconstructed_sha,
        "expected_bundle_size_bytes": manifest.get("bundle_size_bytes"),
        "reconstructed_size_bytes": reconstructed_size,
        "expected_chunk_count": manifest.get("chunk_count"),
        "observed_chunk_count": len(rows),
        "chunk_count_ok": len(rows) == manifest.get("chunk_count"),
        "all_chunks_ok": bool(all_chunks_ok),
        "bundle_sha256_ok": reconstructed_sha == manifest.get("bundle_sha256"),
        "bundle_size_ok": reconstructed_size == manifest.get("bundle_size_bytes"),
        "git_bundle_verify_ok": bool(git_bundle_verify["ok"]),
        "git_bundle_verify": git_bundle_verify,
        "chunk_rows": rows if args.verbose else None,
    }
    report["content_publication_verified"] = bool(
        report["chunk_count_ok"]
        and report["all_chunks_ok"]
        and report["bundle_sha256_ok"]
        and report["bundle_size_ok"]
        and report["git_bundle_verify_ok"]
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    parser.add_argument("--chunks-root", default=DEFAULT_CHUNKS_ROOT)
    parser.add_argument("--json", action="store_true", help="Print the full JSON report.")
    parser.add_argument("--verbose", action="store_true", help="Include per-chunk rows in JSON output.")
    args = parser.parse_args()

    report = verify(args)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        status = "PASS" if report["content_publication_verified"] else "FAIL"
        print(f"A2T remote content-publication verification: {status}")
        print(f"manifest: {report['manifest']}")
        print(f"chunks_root: {report['chunks_root']}")
        print(f"expected_sha256: {report['expected_bundle_sha256']}")
        print(f"reconstructed_sha256: {report['reconstructed_sha256']}")
        print(f"chunk_count_ok: {report['chunk_count_ok']}")
        print(f"all_chunks_ok: {report['all_chunks_ok']}")
        print(f"bundle_sha256_ok: {report['bundle_sha256_ok']}")
        print(f"bundle_size_ok: {report['bundle_size_ok']}")
        print(f"git_bundle_verify_ok: {report['git_bundle_verify_ok']}")
    return 0 if report["content_publication_verified"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
