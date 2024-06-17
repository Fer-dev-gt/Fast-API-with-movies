from fastapi import FastAPI

app = FastAPI()
app.title = "Le cambié el nombre a mi API"
app.version = "7.7.7"

@app.get("/", tags=["Root que yo creé"])

def message():
    return {"message": "Hello World"}