from fastapi import APIRouter, HTTPException

from app.models.user import LoginRequest, TokenResponse, UserCreate, UserList, UserResponse
from app.services.user_service import authenticate, create_user, list_users

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=UserResponse)
async def register(data: UserCreate):
    try:
        return await create_user(data)
    except Exception as e:
        if "UNIQUE" in str(e).upper():
            raise HTTPException(status_code=409, detail="Email already registered.")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest):
    result = await authenticate(data.email, data.password)
    if result is None:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    user, token = result
    return TokenResponse(access_token=token, user=user)


@router.get("/me", response_model=UserResponse)
async def get_me():
    """Get current user. Requires valid JWT or API key."""
    # In a full implementation, this would use the require_user dependency
    # For now, return a placeholder that indicates auth is working
    raise HTTPException(status_code=401, detail="Authentication required. Send JWT token.")


@router.get("/users", response_model=UserList)
async def get_users():
    return await list_users()
