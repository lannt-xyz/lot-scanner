from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.templating import Jinja2Templates
from fastapi_pagination import add_pagination

from app.controllers import image_controller

# Create a FastAPI instance
app = FastAPI()

app.include_router(image_controller.router, prefix="/api/v1", tags=["ocr"])

# Add CORS middleware to the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_methods="*",
    allow_headers="*",
)

# Add pagination to the FastAPI application
add_pagination(app)
