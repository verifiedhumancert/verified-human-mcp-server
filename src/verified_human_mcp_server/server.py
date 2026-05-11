"""MCP server exposing Verified Human Cert tools for Claude Code."""

import json
import logging
from collections.abc import Callable
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

from . import client

logger = logging.getLogger(__name__)

mcp = FastMCP(
    "verified-human-mcp-server",
    instructions=(
        "Verified Human Cert registry — verify human-made music certifications "
        "by ISRC, artist/track, or cert number. Browse the public registry and "
        "check platform stats and pricing."
    ),
)


def _call(fn: Callable[..., Any], *args: Any, **kwargs: Any) -> str:
    """Call a client function and return JSON, with unified error handling.

    Catches every httpx error class and converts it to a structured JSON
    response, so the MCP client receives a valid tool result instead of a
    server-side traceback. All caught exceptions are logged to stderr.
    """
    try:
        result = fn(*args, **kwargs)
        return json.dumps(result, indent=2, ensure_ascii=False)
    except httpx.HTTPStatusError as e:
        logger.exception(
            "Upstream HTTP %s for %s", e.response.status_code, e.request.url
        )
        return json.dumps(
            {"error": f"HTTP {e.response.status_code}", "detail": e.response.text}
        )
    except httpx.RequestError as e:
        logger.exception("Upstream request error: %s", type(e).__name__)
        return json.dumps({"error": type(e).__name__, "detail": str(e)})


@mcp.tool()
def vhc_verify_isrc(isrc: str) -> str:
    """Verify a human-made music certification by ISRC code.

    Returns certification details if the ISRC is registered, or a not-found
    response otherwise.

    Args:
        isrc: International Standard Recording Code (e.g. "USHM82148308").
    """
    return _call(client.verify_by_isrc, isrc)


@mcp.tool()
def vhc_verify_track(artist: str, track: str) -> str:
    """Check certification status by artist and track name.

    Args:
        artist: Artist or band name (e.g. "The Beatles").
        track: Track title (e.g. "Yesterday").
    """
    return _call(client.status_by_artist_track, artist, track)


@mcp.tool()
def vhc_verify_cert(cert_number: str) -> str:
    """Look up a certification by its cert number.

    Args:
        cert_number: Certification number (e.g. "VH-2026-000001").
    """
    return _call(client.verify_by_cert_number, cert_number)


@mcp.tool()
def vhc_registry() -> str:
    """List all recently issued human-made music certifications.

    Returns the public registry of verified certifications.
    """
    return _call(client.get_recent_registry)


@mcp.tool()
def vhc_stats() -> str:
    """Get platform statistics — totals, tier breakdown, certification counts.

    Combines data from both registry and certification stats endpoints.
    """
    return _call(
        lambda: {
            "registry": client.get_registry_stats(),
            "certifications": client.get_certification_stats(),
        }
    )


@mcp.tool()
def vhc_pricing() -> str:
    """Get current pricing and bundle options for VHC certifications."""
    return _call(client.get_pricing)
