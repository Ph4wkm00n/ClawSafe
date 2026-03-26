"""ClawSafe OpenClaw Skill — Ask your AI helper "Is it safe?"

This is a reference skill that connects to the ClawSafe API
and provides plain-language safety summaries.

Usage:
    python clawsafe_skill.py [api_url]
"""

import sys

import httpx


DEFAULT_API_URL = "http://localhost:8000"


def check_safety(api_url: str = DEFAULT_API_URL) -> str:
    """Query ClawSafe API and return a plain-language safety summary."""
    try:
        resp = httpx.get(f"{api_url}/api/v1/skill/status", timeout=5)
        resp.raise_for_status()
        data = resp.json()

        lines = [data["summary"]]
        if data["top_actions"]:
            lines.append("\nSuggested actions:")
            for action in data["top_actions"]:
                lines.append(f"  - {action}")
        else:
            lines.append("No actions needed right now.")

        return "\n".join(lines)
    except httpx.ConnectError:
        return "Could not reach ClawSafe. Make sure it's running."
    except Exception as e:
        return f"Error checking safety: {e}"


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_API_URL
    print(check_safety(url))
