"""ClawSafe API client SDK — Python wrapper for the ClawSafe REST API."""

from __future__ import annotations

import httpx


class ClawSafeClient:
    """Python client for the ClawSafe API.

    Usage:
        client = ClawSafeClient("http://localhost:8000", api_key="your-key")
        status = client.get_status()
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        api_key: str = "",
        jwt_token: str = "",
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._headers: dict[str, str] = {}
        if api_key:
            self._headers["Authorization"] = f"Bearer {api_key}"
        elif jwt_token:
            self._headers["Authorization"] = f"Bearer {jwt_token}"

    def _url(self, path: str) -> str:
        return f"{self.base_url}/api/v1{path}"

    def _get(self, path: str, params: dict | None = None) -> dict:
        with httpx.Client(timeout=self._timeout) as client:
            resp = client.get(self._url(path), headers=self._headers, params=params)
            resp.raise_for_status()
            return resp.json()

    def _post(self, path: str, json: dict | None = None) -> dict:
        with httpx.Client(timeout=self._timeout) as client:
            resp = client.post(self._url(path), headers=self._headers, json=json)
            resp.raise_for_status()
            return resp.json()

    def _put(self, path: str, json: dict | None = None) -> dict:
        with httpx.Client(timeout=self._timeout) as client:
            resp = client.put(self._url(path), headers=self._headers, json=json)
            resp.raise_for_status()
            return resp.json()

    # ── Read Endpoints ─────────────────────────────────────────────────────

    def get_health(self) -> dict:
        """Check API health."""
        return self._get("/health")

    def get_status(self) -> dict:
        """Get overall safety status."""
        return self._get("/status")

    def get_status_category(self, category: str) -> dict:
        """Get status for a specific category."""
        return self._get(f"/status/{category}")

    def get_activity(self, limit: int = 20, offset: int = 0) -> dict:
        """Get activity events."""
        return self._get("/activity", params={"limit": limit, "offset": offset})

    def get_scans(self, limit: int = 20) -> dict:
        """Get scan history."""
        return self._get("/scans", params={"limit": limit})

    def get_recommendations(self) -> dict:
        """Get security recommendations."""
        return self._get("/recommendations")

    def get_settings(self) -> dict:
        """Get user settings."""
        return self._get("/settings")

    def get_policy(self) -> dict:
        """Get active policy."""
        return self._get("/policy")

    def get_instances(self) -> dict:
        """List all instances."""
        return self._get("/instances")

    # ── Write Endpoints ────────────────────────────────────────────────────

    def apply_fix(self, action_id: str) -> dict:
        """Apply an auto-fix action."""
        return self._post(f"/fix/{action_id}")

    def undo_fix(self, action_id: str) -> dict:
        """Undo a previously applied fix."""
        return self._post(f"/fix/{action_id}/undo")

    def update_settings(self, settings: dict) -> dict:
        """Update user settings."""
        return self._put("/settings", json=settings)

    def update_policy(self, policy: dict) -> dict:
        """Update the active policy."""
        return self._put("/policy", json=policy)

    def simulate_policy(self, policy: dict, findings: dict | None = None) -> dict:
        """Simulate a policy change."""
        return self._post("/policy/simulate", json={"policy": policy, "findings": findings})
