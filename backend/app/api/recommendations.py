from fastapi import APIRouter

from app.models.schemas import CategoryName, Recommendation, SafetyLevel
from app.services.scanner import get_demo_findings, scan_openclaw
from app.services.scoring import compute_status

router = APIRouter()

RECOMMENDATION_DB: dict[str, Recommendation] = {
    "fix_network_binding": Recommendation(
        id="fix_network_binding",
        title="Make OpenClaw Private",
        description="People outside your home can reach your AI right now. We can change this so only you can use it.",
        category=CategoryName.network,
        severity=SafetyLevel.risk,
        action_label="Make it private",
        steps=[
            "Open your terminal",
            "Edit the OpenClaw config file",
            "Change bind_address to \"127.0.0.1\"",
            "Restart OpenClaw",
        ],
        commands=[
            "sudo nano /etc/openclaw/config.yaml",
            "# Set: bind_address: \"127.0.0.1\"",
            "docker restart openclaw",
        ],
    ),
    "fix_tools_policy": Recommendation(
        id="fix_tools_policy",
        title="Disable Risky Tools",
        description="Some dangerous abilities are turned on, like shell access. Turning them off makes your setup much safer.",
        category=CategoryName.tools,
        severity=SafetyLevel.risk,
        action_label="Disable risky tools",
        steps=[
            "Open your terminal",
            "Edit the OpenClaw config file",
            "Set high-risk skills to enabled: false",
            "Restart OpenClaw",
        ],
        commands=[
            "sudo nano /etc/openclaw/config.yaml",
            "# Set shell_exec enabled: false",
            "docker restart openclaw",
        ],
    ),
    "fix_data_mounts": Recommendation(
        id="fix_data_mounts",
        title="Limit File Access",
        description="OpenClaw can see sensitive areas of your system. We can restrict it to only the folders it needs.",
        category=CategoryName.data,
        severity=SafetyLevel.risk,
        action_label="Limit access",
        steps=[
            "Open your Docker Compose file",
            "Remove broad volume mounts (like / or /home)",
            "Add only specific folders OpenClaw needs",
            "Restart the containers",
        ],
        commands=[
            "sudo nano docker-compose.yml",
            "# Replace '/' with specific paths like './data:/app/data'",
            "docker compose down && docker compose up -d",
        ],
    ),
    "fix_updates": Recommendation(
        id="fix_updates",
        title="Update OpenClaw",
        description="You're running an older version. Updating gets you the latest security fixes.",
        category=CategoryName.updates,
        severity=SafetyLevel.attention,
        action_label="See update guide",
        steps=[
            "Pull the latest OpenClaw image",
            "Restart the containers",
            "Verify the new version is running",
        ],
        commands=[
            "docker pull openclaw/openclaw:latest",
            "docker compose down && docker compose up -d",
            "docker exec openclaw openclaw --version",
        ],
    ),
}


@router.get("/recommendations", response_model=list[Recommendation])
async def get_recommendations():
    findings = scan_openclaw()
    if not findings["openclaw_detected"]:
        findings = get_demo_findings()
    status = compute_status(findings)

    recs = []
    for cat in status.categories:
        if cat.status != SafetyLevel.safe and cat.action_id in RECOMMENDATION_DB:
            recs.append(RECOMMENDATION_DB[cat.action_id])
    return recs
