from fastapi import FastAPI

from .routers import auth


app = FastAPI(
    title="Real Estate Service API",
    description="A FastAPI project",
    version="0.1.0",
    docs_url="/",
    redoc_url="/redoc",
    contact={
        "name": "Martin",
        "email": "tuyiiya.web@gmail.com",
        "url": "https://www.linkedin.com/in/joseph-s-1000/"
    }
)



@app.get("/testing")
async def read_root():
    return {"message": "Hello World!"}

app.include_router(auth.router)