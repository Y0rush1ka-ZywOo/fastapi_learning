from fastapi import FastAPI
from path_argument import app as models_app
app = FastAPI()
app.mount("/models_app", models_app)
@app.get("/")
async def root():
    return {"message": "Hello World"}