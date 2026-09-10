from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Weather dashboard :)"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/health")
def read_health():
	return {"message": "Looks Healthy"}


#if __name__ == "__main__":
#    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
