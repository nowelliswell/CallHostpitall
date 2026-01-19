from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routers import queue
from .database.connection import db_manager

# Initialize FastAPI app
app = FastAPI(
    title="Hospital Queue Management API",
    description="API for managing hospital patient queues",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(queue.router)

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Hospital Queue Management API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    db_manager.init_database()
    print("Database initialized successfully")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)