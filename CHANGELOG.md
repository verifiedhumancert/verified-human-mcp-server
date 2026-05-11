# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `VHC_API_TIMEOUT` environment variable to configure HTTP request timeout.
- `VHC_API_RETRIES` and `VHC_API_BACKOFF` environment variables. The client now
  retries idempotent GETs on transient transport errors and 5xx responses with
  exponential backoff (2 retries by default).
- `.env.example` documenting supported environment variables.
- `license` field and trove classifiers in `pyproject.toml`.
- `SECURITY.md` with a coordinated disclosure policy and reporting channels.
- Coverage reporting in CI (`pytest-cov`) with `--cov-fail-under=80`. Current
  total coverage is 87% (`server.py` at 100%, `client.py` at 88%).

### Changed
- CI now runs lint and tests against Python 3.10, 3.11, 3.12, and 3.13 in a
  matrix, instead of only 3.12.
- CI installs Poetry via `snok/install-poetry@v1` pinned to `2.0.1`, and
  caches dependencies via `actions/setup-python` for faster runs.
- `_call` in the server now catches `httpx.RequestError` (covering timeouts,
  read errors, and protocol errors in addition to connection failures) and
  logs every caught upstream error to stderr via the `logging` module.
- The CLI entry point (`python -m verified_human_mcp_server`) configures
  stderr logging at the level set by `VHC_LOG_LEVEL` (default `WARNING`).

### Added (continued)
- `VHC_LOG_LEVEL` environment variable for the server log level.
- `tests/test_server.py` covering `_call` (success, every handled httpx error
  class, unknown-exception propagation) and every `vhc_*` tool wrapper,
  including the `vhc_stats` two-source merge and its upstream-error path.
- CI `security` job: gitleaks (binary install, no license required) for
  secret scanning and `pip-audit` against the exported `requirements.txt`
  for dependency CVE scanning. Both run on push and pull request.
- pytest now also emits `coverage.xml` so downstream tooling (audit
  analyzers, Codecov, IDE gutters) can ingest coverage.

## [0.1.0] - 2026-05-11

### Added
- Initial release of the Verified Human MCP Server.
- Tools: `vhc_verify_isrc`, `vhc_verify_track`, `vhc_verify_cert`, `vhc_registry`, `vhc_stats`, `vhc_pricing`.
- Unit tests for the HTTP client with `respx`-mocked responses.
- GitHub Actions CI: ruff lint, ruff format check, pytest.

[Unreleased]: https://github.com/verifiedhuman/verified-human-mcp-server/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/verifiedhuman/verified-human-mcp-server/releases/tag/v0.1.0
