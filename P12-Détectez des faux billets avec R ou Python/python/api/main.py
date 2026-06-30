from fastapi import FastAPI
from api.router import router

app = FastAPI(
    title="Detecting the fake bills in euro",
    description="ONCFM — API de détection de faux billets",
    version="1.0.0",
)
app.include_router(router)

@app.get("/", tags=['Welcome'])
def welcome():
    return {
        "message": "Welcome!"
    }
