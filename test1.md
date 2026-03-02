### Sealed Hash Authority Rule (Hard Gate)

If status == Published:

- sealed.sealed_hashes.* is the single source of truth.
- artifact_hashes.* must equal sealed.sealed_hashes.*.
- If artifact_hashes differs from sealed_hashes:
  - Treat as drift.
  - Do NOT attempt to reconcile.

