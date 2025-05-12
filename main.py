from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller import images  # import your route modules


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(images.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app"}