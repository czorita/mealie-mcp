"""
Unit tests for the HTTP transport configuration and bearer-token auth
used by the server's entry point (src/server.py).
"""

import pytest

from src.server import _check_bearer_token, _resolve_http_config


@pytest.mark.unit
class TestResolveHttpConfig:
    def test_defaults(self, monkeypatch):
        monkeypatch.delenv("MCP_HOST", raising=False)
        monkeypatch.delenv("MCP_PORT", raising=False)
        monkeypatch.setenv("MEALIE_API_TOKEN", "test-token")

        host, port, token = _resolve_http_config()

        assert host == "0.0.0.0"
        assert port == 8000
        assert token == "test-token"

    def test_env_overrides(self, monkeypatch):
        monkeypatch.setenv("MCP_HOST", "127.0.0.1")
        monkeypatch.setenv("MCP_PORT", "9001")
        monkeypatch.setenv("MEALIE_API_TOKEN", "another-token")

        host, port, token = _resolve_http_config()

        assert host == "127.0.0.1"
        assert port == 9001
        assert token == "another-token"

    def test_missing_token_exits(self, monkeypatch):
        monkeypatch.delenv("MEALIE_API_TOKEN", raising=False)

        with pytest.raises(SystemExit):
            _resolve_http_config()


@pytest.mark.unit
class TestCheckBearerToken:
    def test_correct_token_accepted(self):
        assert _check_bearer_token("Bearer secret123", "secret123") is True

    def test_wrong_token_rejected(self):
        assert _check_bearer_token("Bearer wrong", "secret123") is False

    def test_missing_header_rejected(self):
        assert _check_bearer_token(None, "secret123") is False

    def test_missing_bearer_prefix_rejected(self):
        assert _check_bearer_token("secret123", "secret123") is False

    def test_empty_header_rejected(self):
        assert _check_bearer_token("", "secret123") is False

    def test_bearer_with_no_token_rejected(self):
        assert _check_bearer_token("Bearer ", "secret123") is False
