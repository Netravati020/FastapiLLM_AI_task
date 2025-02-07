from fastapi import FastAPI
from app.api.routes import router


app = FastAPI(title="Text Processing API")

# Include API routes
app.include_router(router)
