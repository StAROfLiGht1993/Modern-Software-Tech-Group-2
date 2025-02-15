#!/usr/bin/env python3

# TODO Shift the Running of the Application here

from fastapi import FastAPI
from app.routes import seller_submission, card_verification

app = FastAPI()

# Include routes
app.include_router(seller_submission.router, prefix="/auction")
app.include_router(card_verification.router, prefix="/verification")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Pokémon Card Auction Platform"}
