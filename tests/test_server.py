"""Unit tests for the MCP server layer — error handling and tool wrappers."""

import json

import httpx
import pytest

from verified_human_mcp_server import client, server


def _http_status_error(status: int, text: str) -> httpx.HTTPStatusError:
    request = httpx.Request("GET", "https://test.verifiedhumancert.com/x")
    response = httpx.Response(status, text=text, request=request)
    return httpx.HTTPStatusError("err", request=request, response=response)


class TestCallSuccess:
    def test_returns_json_for_dict(self):
        result = server._call(lambda: {"ok": True, "n": 1})
        assert json.loads(result) == {"ok": True, "n": 1}

    def test_returns_json_for_list(self):
        result = server._call(lambda: [{"a": 1}, {"a": 2}])
        assert json.loads(result) == [{"a": 1}, {"a": 2}]

    def test_forwards_args_and_kwargs(self):
        result = server._call(lambda a, b: {"sum": a + b}, 2, b=3)
        assert json.loads(result) == {"sum": 5}

    def test_preserves_unicode(self):
        result = server._call(lambda: {"name": "Łukasz"})
        assert "Łukasz" in result


class TestCallErrorHandling:
    def test_http_status_error(self, caplog):
        def raiser():
            raise _http_status_error(404, "not found")

        with caplog.at_level("ERROR"):
            parsed = json.loads(server._call(raiser))
        assert parsed == {"error": "HTTP 404", "detail": "not found"}
        assert any("Upstream HTTP 404" in r.message for r in caplog.records)

    def test_connect_error(self, caplog):
        def raiser():
            raise httpx.ConnectError("conn refused")

        with caplog.at_level("ERROR"):
            parsed = json.loads(server._call(raiser))
        assert parsed["error"] == "ConnectError"
        assert "conn refused" in parsed["detail"]
        assert any("ConnectError" in r.message for r in caplog.records)

    def test_read_timeout(self, caplog):
        def raiser():
            raise httpx.ReadTimeout("timed out")

        with caplog.at_level("ERROR"):
            parsed = json.loads(server._call(raiser))
        assert parsed["error"] == "ReadTimeout"
        assert "timed out" in parsed["detail"]

    def test_generic_request_error(self, caplog):
        def raiser():
            raise httpx.RequestError("transport broke")

        with caplog.at_level("ERROR"):
            parsed = json.loads(server._call(raiser))
        assert parsed["error"] == "RequestError"
        assert "transport broke" in parsed["detail"]

    def test_unknown_exception_propagates(self):
        """Non-httpx errors are NOT swallowed — they're programming bugs."""

        def raiser():
            raise ValueError("bug")

        with pytest.raises(ValueError):
            server._call(raiser)


class TestToolWrappers:
    def test_vhc_verify_isrc_forwards_arg(self, monkeypatch):
        seen = {}

        def fake(isrc):
            seen["isrc"] = isrc
            return {"certified": True, "certNumber": "VH-2026-000001"}

        monkeypatch.setattr(client, "verify_by_isrc", fake)
        result = json.loads(server.vhc_verify_isrc("USHM82148308"))
        assert seen["isrc"] == "USHM82148308"
        assert result["certified"] is True

    def test_vhc_verify_track_forwards_both_args(self, monkeypatch):
        seen = {}

        def fake(artist, track):
            seen.update(artist=artist, track=track)
            return {"certified": True}

        monkeypatch.setattr(client, "status_by_artist_track", fake)
        json.loads(server.vhc_verify_track("The Beatles", "Yesterday"))
        assert seen == {"artist": "The Beatles", "track": "Yesterday"}

    def test_vhc_verify_cert(self, monkeypatch):
        monkeypatch.setattr(
            client,
            "verify_by_cert_number",
            lambda n: {"certNumber": n, "status": "active"},
        )
        result = json.loads(server.vhc_verify_cert("VH-2026-000001"))
        assert result["status"] == "active"

    def test_vhc_registry(self, monkeypatch):
        monkeypatch.setattr(
            client, "get_recent_registry", lambda: [{"certNumber": "VH-2026-000001"}]
        )
        result = json.loads(server.vhc_registry())
        assert len(result) == 1

    def test_vhc_stats_merges_both_sources(self, monkeypatch):
        monkeypatch.setattr(client, "get_registry_stats", lambda: {"total": 100})
        monkeypatch.setattr(client, "get_certification_stats", lambda: {"active": 50})
        result = json.loads(server.vhc_stats())
        assert result == {"registry": {"total": 100}, "certifications": {"active": 50}}

    def test_vhc_stats_surfaces_upstream_error(self, monkeypatch):
        """If either stats call fails, the wrapper returns a structured error."""

        def boom():
            raise _http_status_error(503, "unavailable")

        monkeypatch.setattr(client, "get_registry_stats", boom)
        monkeypatch.setattr(client, "get_certification_stats", lambda: {"active": 50})
        result = json.loads(server.vhc_stats())
        assert result["error"] == "HTTP 503"

    def test_vhc_pricing(self, monkeypatch):
        monkeypatch.setattr(client, "get_pricing", lambda: {"single": 29.99})
        result = json.loads(server.vhc_pricing())
        assert result["single"] == 29.99
