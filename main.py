from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller import images_controller  # import your route modules


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

app.include_router(images_controller.router)

@app.get("/")
def read_root():
    return {"message": "Server is running"}