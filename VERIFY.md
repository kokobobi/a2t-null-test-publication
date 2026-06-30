# Verify The A2T Mode B Remote Bundle

This page gives the minimal external verification path for the public A2T
Mode B content-publication bundle.

## What This Verifies

The verifier checks that the remote GitHub raw manifest and chunk files
reconstruct the same local publication git bundle recorded by the project.

It verifies:

- the manifest can be read from GitHub raw URLs;
- every base64 chunk decodes successfully;
- every encoded and raw chunk SHA-256 matches the manifest;
- the reconstructed bundle size matches the manifest;
- the reconstructed bundle SHA-256 is:

```text
375a97bc4fcf3930d8f1505f5388de71d21d44ee4c26c5c86afd2a9bb3b6ac4c
```

- `git bundle verify` succeeds on the reconstructed bundle.

## What This Does Not Verify

This is not a physics-discovery verification and not an H1 hardware result.
It also does not prove a full remote Git mirror or a GPG-signed artifact.

The correct claim is:

```text
Mode B content-publication verifies checksum-preserving remote transport of the
local publication git bundle.
```

## Requirements

- Python 3.10 or newer
- Git available on `PATH`
- Network access to `raw.githubusercontent.com`

The verifier uses only the Python standard library plus the `git` executable.

## One-Command Verification

From a checkout of this repository:

```bash
python3 scripts/verify_remote_bundle.py
```

Expected output:

```text
A2T remote content-publication verification: PASS
chunk_count_ok: True
all_chunks_ok: True
bundle_sha256_ok: True
bundle_size_ok: True
git_bundle_verify_ok: True
```

For a full JSON report:

```bash
python3 scripts/verify_remote_bundle.py --json
```

## Verified Remote Inputs

Manifest:

```text
https://raw.githubusercontent.com/kokobobi/hello-world/main/data/content_publication_bundle_20260630/a2t_content_publication_bundle_manifest_20260630.json
```

Chunks root:

```text
https://raw.githubusercontent.com/kokobobi/hello-world/main/data/content_publication_bundle_20260630/
```

## Current Audit Boundary

The project status remains:

```text
completed_item_count = 6
total_item_count = 7
goal_complete = false
remaining = real H1 apparatus data, measured calibration artifacts, and blind custody
```
