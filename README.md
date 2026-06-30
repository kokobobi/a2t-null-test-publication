# A2T Null-Test Publication

This repository is the public-facing review entry point for the A2T null-test publication package and reproducibility audit materials.

## Current Status

- Status date: 2026-06-30
- Seven-item audit: **6/7 complete**
- Overall goal complete: **false**
- Item 6 remote publication: **complete under Mode B content-publication**
- Item 7 real H1 hardware transition: **incomplete**

## Claim Boundary

This repository does **not** claim a physics discovery, a real H1 hardware result, or completion of the full seven-item objective. The current artifact is an engineering and reproducibility milestone.

The remote publication currently verifies transport of a **checksum-verified local git bundle**. It is **not** a full remote Git mirror.

## Remote Content-Publication Bundle

The verified content-publication bundle is currently hosted under the earlier transport repository:

- Manifest: `https://raw.githubusercontent.com/kokobobi/hello-world/main/data/content_publication_bundle_20260630/a2t_content_publication_bundle_manifest_20260630.json`
- Chunks root: `https://raw.githubusercontent.com/kokobobi/hello-world/main/data/content_publication_bundle_20260630/`
- Local publication head transported by the bundle: `66694666bb0b9f13aa7dca2ad62cba8fe36ad643`
- Bundle SHA-256: `375a97bc4fcf3930d8f1505f5388de71d21d44ee4c26c5c86afd2a9bb3b6ac4c`

All remote verification checks passed:

- chunk count OK
- all chunks OK
- bundle size OK
- bundle SHA-256 OK
- `git bundle verify` OK

## How To Verify

From the project workspace containing the verifier script:

```bash
python3 scripts/a2t_verify_content_publication_bundle.py \
  --manifest https://raw.githubusercontent.com/kokobobi/hello-world/main/data/content_publication_bundle_20260630/a2t_content_publication_bundle_manifest_20260630.json \
  --chunks-root https://raw.githubusercontent.com/kokobobi/hello-world/main/data/content_publication_bundle_20260630 \
  --verify-git-bundle \
  --out generated/content_publication_remote_verification_20260630.json
```

Expected result:

```text
content_publication_verified = true
reconstructed_sha256 = 375a97bc4fcf3930d8f1505f5388de71d21d44ee4c26c5c86afd2a9bb3b6ac4c
git_bundle_verify_ok = true
```

## Review Materials In This Repository

- [`AUDIT_SUMMARY.md`](AUDIT_SUMMARY.md): human-readable seven-item audit summary.
- [`docs/MODE_A_TO_MODE_B_RATIONALE.md`](docs/MODE_A_TO_MODE_B_RATIONALE.md): governance rationale for closing item 6 under Mode B rather than Mode A.
- [`data/a2t_remote_publication_status_after_upload_20260630.json`](data/a2t_remote_publication_status_after_upload_20260630.json): public-safe machine-readable status summary.

## Remaining Work

The only remaining item in the active seven-item goal is the real H1 hardware transition. Completion requires real apparatus event data, measured calibration artifacts, and blind custody validation. Template or simulated data is not accepted as H1 completion evidence.
