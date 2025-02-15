#!/usr/bin/env python3

# TODO Shift the Running of the Application here
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import search, seller_submission

app = FastAPI()

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
# app.include_router(card_verification.router, prefix="/books", tags=["Books"])
app.include_router(seller_submission.router, prefix="", tags=["Reviews"])

