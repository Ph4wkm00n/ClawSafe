"""User service — CRUD, password hashing, JWT tokens."""

from __future__ import annotations

import hashlib
import hmac
import logging
import secrets
import uuid

from app.core.config import settings
from app.db.database import get_db
from app.models.user import UserCreate, UserList, UserResponse

logger = logging.getLogger(__name__)

VALID_ROLES = {"admin", "officer", "viewer"}


def _hash_password(password: str) -> str:
    """Hash password using SHA-256 with salt. Simple but effective."""
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256(f"{salt}:{password}".encode()).hexdigest()
    return f"{salt}:{hashed}"


def _verify_password(password: str, stored_hash: str) -> bool:
    """Verify password against stored hash."""
    try:
        salt, hashed = stored_hash.split(":", 1)
        expected = hashlib.sha256(f"{salt}:{password}".encode()).hexdigest()
        return hmac.compare_digest(hashed, expected)
    except ValueError:
        return False


def _create_jwt(user_id: str, email: str, role: str) -> str:
    """Create a simple JWT-like token. For production, use python-jose."""
    import json
    import base64
    import time

    header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode().rstrip("=")
    now = int(time.time())
    payload_data = {
        "sub": user_id,
        "email": email,
        "role": role,
        "iat": now,
        "exp": now + (settings.jwt_expire_minutes * 60),
    }
    payload = base64.urlsafe_b64encode(json.dumps(payload_data).encode()).decode().rstrip("=")
    signing_input = f"{header}.{payload}"
    signature = hmac.new(
        (settings.jwt_secret or "dev-secret").encode(),
        signing_input.encode(),
        hashlib.sha256,
    ).hexdigest()
    return f"{header}.{payload}.{signature}"


def decode_jwt(token: str) -> dict | None:
    """Decode and verify a JWT token. Returns payload dict or None."""
    import json
    import base64
    import time

    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None

        header, payload, signature = parts

        # Verify signature
        signing_input = f"{header}.{payload}"
        expected_sig = hmac.new(
            (settings.jwt_secret or "dev-secret").encode(),
            signing_input.encode(),
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(signature, expected_sig):
            return None

        # Decode payload
        padding = 4 - len(payload) % 4
        payload_bytes = base64.urlsafe_b64decode(payload + "=" * padding)
        data = json.loads(payload_bytes)

        # Check expiry
        if data.get("exp", 0) < time.time():
            return None

        return data
    except Exception:
        return None


async def create_user(data: UserCreate) -> UserResponse:
    db = await get_db()
    user_id = str(uuid.uuid4())[:8]
    password_hash = _hash_password(data.password)
    role = data.role if data.role in VALID_ROLES else "viewer"

    await db.execute(
        "INSERT INTO users (id, email, password_hash, role) VALUES (?, ?, ?, ?)",
        (user_id, data.email, password_hash, role),
    )
    await db.commit()
    logger.info("Created user %s (%s) with role %s", user_id, data.email, role)
    return (await get_user_by_id(user_id))  # type: ignore[return-value]


async def authenticate(email: str, password: str) -> tuple[UserResponse, str] | None:
    """Authenticate user and return (user, token) or None."""
    db = await get_db()
    row = await db.fetch_one("SELECT * FROM users WHERE email = ? AND is_active = 1", (email,))
    if row is None:
        return None

    if not _verify_password(password, row["password_hash"]):
        return None

    user = UserResponse(
        id=row["id"],
        email=row["email"],
        role=row["role"],
        is_active=bool(row["is_active"]),
        created_at=row["created_at"],
    )
    token = _create_jwt(user.id, user.email, user.role)
    return user, token


async def get_user_by_id(user_id: str) -> UserResponse | None:
    db = await get_db()
    row = await db.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
    if row is None:
        return None
    return UserResponse(
        id=row["id"],
        email=row["email"],
        role=row["role"],
        is_active=bool(row["is_active"]),
        created_at=row["created_at"],
    )


async def list_users() -> UserList:
    db = await get_db()
    rows = await db.fetch_all("SELECT id, email, role, is_active, created_at FROM users ORDER BY created_at")
    users = [
        UserResponse(
            id=row["id"],
            email=row["email"],
            role=row["role"],
            is_active=bool(row["is_active"]),
            created_at=row["created_at"],
        )
        for row in rows
    ]
    return UserList(users=users, total=len(users))
