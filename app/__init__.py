from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_pagination import add_pagination

from app.controllers import (
    auth_controller,
    lot_scan_controller,
    quick_scan_controller,
    secure_controller,
    config_controller,
    ticket_controller,
)

# Create a FastAPI instance
app = FastAPI()

app.include_router(auth_controller.router, prefix="", tags=["Authentication"])

api_version_prefix = "/api/v1"
app.include_router(lot_scan_controller.router, prefix=api_version_prefix, tags=["OCR"])
app.include_router(config_controller.router, prefix=api_version_prefix, tags=["Configurations"])
app.include_router(secure_controller.router, prefix=api_version_prefix, tags=["Secure"])
app.include_router(quick_scan_controller.router, prefix=f'{api_version_prefix}/quick-scan', tags=["Quick Scan"])
app.include_router(ticket_controller.router, prefix=f'{api_version_prefix}/tickets', tags=["Tickets"])

# Add CORS middleware to the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_methods="*",
    allow_headers="*",
)

# Add pagination to the FastAPI application
add_pagination(app)
