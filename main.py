from fastapi import FastAPI
from controller import images  # import your route modules

app = FastAPI()

app.include_router(images.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app"}