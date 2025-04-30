from fastapi import FastAPI
from controller import images  # import your route modules

app = FastAPI()

# Include routers
app.include_router(images.router)
#app.include_router(product.router)

# Optional root path
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app"}