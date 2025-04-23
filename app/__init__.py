from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_pagination import add_pagination

from app.controllers import auth_controller, lot_scan_controller, secure_controller

# Create a FastAPI instance
app = FastAPI()

app.include_router(auth_controller.router, prefix="", tags=["Authentication"])

app.include_router(lot_scan_controller.router, prefix="/api/v1", tags=["OCR"])
app.include_router(secure_controller.router, prefix="/api/v1", tags=["Secure"])

# Add CORS middleware to the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_methods="*",
    allow_headers="*",
)

# Add pagination to the FastAPI application
add_pagination(app)
