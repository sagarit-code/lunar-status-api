from fastapi import FastAPI
from lunar import get_lunar_data

app = FastAPI()

@app.get("/lunar-status")
def lunar_status():
    data = get_lunar_data()
    return {
        "status": "success",
        "data": data
    }
