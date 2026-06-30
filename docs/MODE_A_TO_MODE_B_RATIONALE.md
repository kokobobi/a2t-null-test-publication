# Mode A To Mode B Remote Publication Rationale

Date: 2026-06-30

## Purpose

This note records why item 6 is closed under **Mode B content-publication** instead of **Mode A full Git mirror**, and what this closure does and does not prove.

## Mode A: Full Git Mirror

Mode A remains the preferred publication form.

A Mode A publication would require:

```text
remote main == local publication head
remote tag local-publication-20260630 == local publication head
remote tree is directly browsable as the publication package
```

This gives reviewers the most convenient GitHub experience: direct browsing, commit history, tags, and normal cloning.

## Why Mode A Was Not Used In This Step

The authenticated path available during this milestone was suitable for GitHub contents publication and small status files, while the local publication package includes large generated artifacts and an existing local git bundle. A full authenticated `git push` mirror was not completed in this step.

To avoid falsely claiming a full mirror, the project adopted a separate content-publication closure mode rather than mixing the two standards.

## Mode B: Content-Publication Bundle

Mode B stores the local publication git bundle as:

```text
manifest JSON + base64 chunk files
```

The verifier reconstructs the bundle from remote raw GitHub URLs and checks:

```text
chunk count
chunk SHA-256 values
raw chunk sizes
reconstructed bundle size
reconstructed bundle SHA-256
git bundle verify
```

Current remote evidence:

- Manifest: `https://raw.githubusercontent.com/kokobobi/hello-world/main/data/content_publication_bundle_20260630/a2t_content_publication_bundle_manifest_20260630.json`
- Chunks root: `https://raw.githubusercontent.com/kokobobi/hello-world/main/data/content_publication_bundle_20260630/`
- Bundle SHA-256: `375a97bc4fcf3930d8f1505f5388de71d21d44ee4c26c5c86afd2a9bb3b6ac4c`
- Local publication head: `66694666bb0b9f13aa7dca2ad62cba8fe36ad643`

## What Mode B Proves

Mode B proves that the local publication bundle was transported to GitHub without checksum drift and remains reconstructable from remote raw URLs.

It is valid evidence for item 6 under the project audit because the seven-item audit now explicitly accepts a passing remote content-publication verification report as an alternative to a full remote Git mirror.

## What Mode B Does Not Prove

Mode B does not prove:

1. The remote repository is a full Git mirror.
2. The remote repository is the final ideal academic publication location.
3. Any real H1 hardware result exists.
4. Any physics discovery is established.
5. The git bundle or tag is GPG-signed.

The correct wording is **checksum-verified local git bundle**, not signed bundle.

## Governance Decision

For this milestone:

```text
item 6 = closed under Mode B content-publication
overall goal = not complete
remaining item = real H1 hardware transition
```

Future preferred hardening step:

```text
promote the publication package to a dedicated full Git mirror or attach a release artifact under this dedicated repository
```
