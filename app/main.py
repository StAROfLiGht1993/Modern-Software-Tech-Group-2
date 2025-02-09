from fastapi import FastAPI
from app.routes import card_verification, seller_submission

app = FastAPI(
    title="Book Management API",
    description="An API for managing books and integrating with OpenAI",
    version="1.0.0",
)

# Include routes
app.include_router(card_verification.router, prefix="/books", tags=["Books"])
app.include_router(seller_submission.router, prefix="", tags=["Reviews"])
