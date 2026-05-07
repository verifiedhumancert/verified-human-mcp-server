"""HTTP client for the Verified Human Cert public REST API."""

import os

import httpx

VHC_BASE_URL = os.environ.get("VHC_API_URL", "https://verifiedhumancert.com")

_TIMEOUT = 15.0


def _get(path: str, params: dict | None = None) -> dict | list:
    """Send a GET request to the VHC API and return parsed JSON."""
    url = f"{VHC_BASE_URL}{path}"
    with httpx.Client(timeout=_TIMEOUT) as client:
        resp = client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()


def verify_by_isrc(isrc: str) -> dict:
    """Verify a certification by ISRC code."""
    return _get("/api/v1/verify", params={"isrc": isrc})


def status_by_artist_track(artist: str, track: str) -> dict:
    """Check certification status by artist and track name."""
    return _get("/api/v1/status", params={"artist": artist, "track": track})


def verify_by_cert_number(cert_number: str) -> dict:
    """Look up a certification by its cert number (e.g. VH-2026-000001)."""
    return _get(f"/api/certifications/verify/{cert_number}")


def get_recent_registry() -> list[dict]:
    """List all recently issued certifications."""
    result = _get("/api/registry/recent")
    if isinstance(result, list):
        return result
    return result.get("certifications", [result])


def get_registry_stats() -> dict:
    """Get registry statistics (totals, tier breakdown)."""
    return _get("/api/registry/stats")


def get_certification_stats() -> dict:
    """Get certification statistics."""
    return _get("/api/certifications/stats")


def get_pricing() -> dict:
    """Get current pricing and bundle options."""
    return _get("/api/certifications/pricing")
