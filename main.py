from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routes.notes import router as notes_router
from config import HOST, PORT, DEBUG

# Create FastAPI app
app = FastAPI(
    title="Connectinno Notes API",
    description="A FastAPI backend for the Connectinno Notes app",
    version="1.0.0",
    debug=DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(notes_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Connectinno Notes API is running!"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        timeout_keep_alive=30,
        timeout_graceful_shutdown=10
    )
