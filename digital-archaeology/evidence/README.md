# Evidence and provenance

For each experimental run, preserve:

- `manifest.json`: case ID, chain IDs, pinned block hashes, addresses, code hash, source commit, tool versions, UTC start/end.
- `calls.jsonl`: sanitized RPC requests and exact responses/errors, no private URLs or credentials.
- `provenance.md`: observations, implementation history, citations and hypotheses clearly separated.
- `hypotheses.md`: attempted recovery paths, expected permissions, failure evidence.
- `results.json`: each evidence gate marked PASS / FAIL / BLOCKED / NOT_RUN, with links.
- `report.md`: findings, limitations, reproducibility, honest uncertainty.
- `SHA256SUMS.txt`: independently computed hashes of final files.
- Executable local tests and their original stdout/stderr/exit codes.

Keep original submitted evidence in [submissions](../../submissions/). Preserve peer audit trails in [reviews](../../reviews/). Never overwrite original logs with a cleaned narrative.
