# Verified Human MCP Server

MCP server for querying the [Verified Human Cert](https://verifiedhumancert.com) registry — verify human-made music certifications by ISRC, artist, track, or cert number.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/verifiedhuman/verified-human-mcp-server/actions/workflows/ci.yml/badge.svg)](https://github.com/verifiedhuman/verified-human-mcp-server/actions/workflows/ci.yml)

## What is Verified Human Cert?

[Verified Human Cert](https://verifiedhumancert.com) is a registry that certifies music tracks as human-made. Artists and labels can register their tracks and receive a certification that proves the music was created by humans, not AI.

This MCP server lets Claude Code (and other MCP clients) query that registry directly.

## Tools

| Tool | Description |
|------|-------------|
| `vhc_verify_isrc` | Verify a certification by ISRC code |
| `vhc_verify_track` | Check certification status by artist + track name |
| `vhc_verify_cert` | Look up a certification by cert number |
| `vhc_registry` | List recently issued certifications |
| `vhc_stats` | Platform statistics (totals, tiers, counts) |
| `vhc_pricing` | Current pricing and bundle options |

## Quick Start

### Prerequisites

- Python 3.10+
- Poetry

### Installation

```bash
poetry install
```

### Running the server

```bash
poetry run python -m verified_human_mcp_server
```

### Add to Claude Code

Add this to your `~/.claude/settings.json` or project `.claude/settings.local.json`:

```json
{
  "mcpServers": {
    "vhc": {
      "command": "poetry",
      "args": ["--directory", "/path/to/verified-human-mcp-server", "run", "python", "-m", "verified_human_mcp_server"]
    }
  }
}
```

### Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `VHC_API_URL` | Base URL for the VHC API | `https://verifiedhumancert.com` |

## Usage Examples

Once connected, you can ask Claude:

- "Is ISRC USHM82148308 certified as human-made?"
- "Check if 'Yesterday' by The Beatles has a VHC certification"
- "Look up cert number VH-2026-000001"
- "Show me the latest certified tracks"
- "What are the current VHC pricing tiers?"

### Multi-agent workflow: metadata + verification

Combine with [mcp-metadata](https://github.com/musictechlab/mcp-metadata) to read ISRC codes from audio files and verify them automatically:

```text
User: "Read the ISRC from song.flac and check if it's certified"

Agent 1 (mcp-metadata): metadata_read("song.flac") -> ISRC: USHM82148308
Agent 2 (verified-human-mcp-server): vhc_verify_isrc("USHM82148308") -> certified: true
```

## Development

```bash
# Clone the repo
git clone https://github.com/verifiedhuman/verified-human-mcp-server.git
cd verified-human-mcp-server

# Install dependencies
poetry install

# Run tests
poetry run pytest

# Run linter
poetry run ruff check .
poetry run ruff format --check .
```

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a PR.

## Security

To report a vulnerability, please see [SECURITY.md](SECURITY.md).

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
  Built by <a href="https://musictechlab.io">MusicTech Lab</a> for <a href="https://verifiedhumancert.com">Verified Human</a><br>
  <a href="https://musictechlab.io">musictechlab.io</a>
  <span> | </span>
  <a href="https://linkedin.com/company/musictechlab">LinkedIn</a>
  <span> | </span>
  <a href="https://musictechlab.io/contact">Let's talk</a>
</div>
