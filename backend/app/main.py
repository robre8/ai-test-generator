from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="AI Test Generator",
    description="AI-powered test generation with a hardened Docker sandbox.",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint for deployment services"""
    return {"status": "healthy"}
