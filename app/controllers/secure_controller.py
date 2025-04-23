from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.context import ApplicationContext, AuthenticatedUser, get_application_context

router = APIRouter()

@router.get("/test-secure")
def test_secure(context: ApplicationContext = Depends(get_application_context())):
    user: AuthenticatedUser = context.user
    return JSONResponse(content={
        "message": f"Hello {user.email}!",
        "user_id": user.user_id,
    })