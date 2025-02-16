#!/usr/bin/env python3

# TODO Shift the Running of the Application here

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes import seller_submission, card_verification, auth, search
import logging
from app.exceptions import ServiceException
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse

# Import the HTTPBearer class
security = HTTPBearer()

# Update the FastAPI application
app = FastAPI(
    title="Pokémon Card Auction Platform API",
    description="This API provides endpoints for the Pokémon Card Auction Platform.",
    version="1.0.0"
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global exception handler for HTTP exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTP exception occurred: {str(exc)}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Global exception handler for custom exceptions - service layer (i.e. biz logic layer) exceptions
@app.exception_handler(ServiceException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"Service exception occurred: {str(exc)}")
    return JSONResponse(
        status_code=exc.status_code, #status code from the exception
        content={"detail": exc.detail}, #message from the exception
    )

# Global exception handler for unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception occurred: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"}
    )


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register search routes
app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(seller_submission.router, prefix="/auction")
app.include_router(card_verification.router, prefix="/verification")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Pokémon Card Auction Platform"}

# Include auth routes
app.include_router(auth.router, prefix="", tags=["Authentication"])