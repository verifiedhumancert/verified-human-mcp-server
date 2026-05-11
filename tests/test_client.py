"""Unit tests for the VHC API client with mocked HTTP responses."""

import httpx
import pytest
import respx

from verified_human_mcp_server import client

BASE = "https://test.verifiedhumancert.com"


@pytest.fixture(autouse=True)
def _set_base_url(monkeypatch):
    monkeypatch.setattr(client, "VHC_BASE_URL", BASE)
    monkeypatch.setattr(client, "_BACKOFF_BASE", 0)


class TestVerifyByIsrc:
    @respx.mock
    def test_found(self):
        payload = {
            "certified": True,
            "certNumber": "VH-2026-000001",
            "isrc": "USHM82148308",
            "artist": "Test Artist",
            "track": "Test Track",
            "tier": "gold",
        }
        respx.get(
            f"{BASE}/api/v1/verify",
            params={"isrc": "USHM82148308"},
        ).mock(return_value=httpx.Response(200, json=payload))

        result = client.verify_by_isrc("USHM82148308")
        assert result["certified"] is True
        assert result["certNumber"] == "VH-2026-000001"

    @respx.mock
    def test_not_found(self):
        respx.get(
            f"{BASE}/api/v1/verify",
            params={"isrc": "XXXXXXXXXXXX"},
        ).mock(return_value=httpx.Response(200, json={"certified": False}))

        result = client.verify_by_isrc("XXXXXXXXXXXX")
        assert result["certified"] is False

    @respx.mock
    def test_server_error(self):
        respx.get(
            f"{BASE}/api/v1/verify",
            params={"isrc": "BAD"},
        ).mock(return_value=httpx.Response(500, text="Internal Server Error"))

        with pytest.raises(httpx.HTTPStatusError):
            client.verify_by_isrc("BAD")


class TestStatusByArtistTrack:
    @respx.mock
    def test_found(self):
        payload = {"certified": True, "certNumber": "VH-2026-000042"}
        respx.get(
            f"{BASE}/api/v1/status",
            params={"artist": "The Beatles", "track": "Yesterday"},
        ).mock(return_value=httpx.Response(200, json=payload))

        result = client.status_by_artist_track("The Beatles", "Yesterday")
        assert result["certified"] is True


class TestVerifyByCertNumber:
    @respx.mock
    def test_found(self):
        payload = {"certNumber": "VH-2026-000001", "artist": "Test", "status": "active"}
        respx.get(
            f"{BASE}/api/certifications/verify/VH-2026-000001",
        ).mock(return_value=httpx.Response(200, json=payload))

        result = client.verify_by_cert_number("VH-2026-000001")
        assert result["certNumber"] == "VH-2026-000001"


class TestRecentRegistry:
    @respx.mock
    def test_returns_list(self):
        payload = [{"certNumber": "VH-2026-000001"}, {"certNumber": "VH-2026-000002"}]
        respx.get(f"{BASE}/api/registry/recent").mock(
            return_value=httpx.Response(200, json=payload)
        )

        result = client.get_recent_registry()
        assert len(result) == 2

    @respx.mock
    def test_returns_wrapped(self):
        payload = {"certifications": [{"certNumber": "VH-2026-000001"}]}
        respx.get(f"{BASE}/api/registry/recent").mock(
            return_value=httpx.Response(200, json=payload)
        )

        result = client.get_recent_registry()
        assert len(result) == 1


class TestStats:
    @respx.mock
    def test_registry_stats(self):
        payload = {"total": 150, "tiers": {"gold": 10, "silver": 50, "bronze": 90}}
        respx.get(f"{BASE}/api/registry/stats").mock(
            return_value=httpx.Response(200, json=payload)
        )

        result = client.get_registry_stats()
        assert result["total"] == 150

    @respx.mock
    def test_certification_stats(self):
        payload = {"totalCertified": 200}
        respx.get(f"{BASE}/api/certifications/stats").mock(
            return_value=httpx.Response(200, json=payload)
        )

        result = client.get_certification_stats()
        assert result["totalCertified"] == 200


class TestPricing:
    @respx.mock
    def test_pricing(self):
        payload = {"single": 29.99, "bundle_5": 99.99}
        respx.get(f"{BASE}/api/certifications/pricing").mock(
            return_value=httpx.Response(200, json=payload)
        )

        result = client.get_pricing()
        assert result["single"] == 29.99
