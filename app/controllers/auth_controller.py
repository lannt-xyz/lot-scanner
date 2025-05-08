
from click import prompt
from fastapi import APIRouter, Request
from fastapi.responses import  RedirectResponse

from app.db.services.user_schemas import UserCreate, UserRead, UserUpdate
from app.modules.auth import fastapi_users, SECRET, auth_backend
from app.modules.auth.google_idp import google_oauth_client

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
router.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, SECRET, "https://apis.lannt.store/auth/google/app-callback"),
    prefix="/auth/google",
    tags=["auth"],
)

@router.get("/auth/google/app-callback")
def app_callback(request: Request):
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    scope = request.query_params.get("scope")
    authuser = request.query_params.get("authuser")
    prompt = request.query_params.get("prompt")
    
    # build redirect_uri with the custom scheme including all the parameters
    redirect_uri = f"store.lannt.lot-scanner-app://callback#code={code}&state={state}&scope={scope}&authuser={authuser}&prompt={prompt}"

    return RedirectResponse(redirect_uri)
