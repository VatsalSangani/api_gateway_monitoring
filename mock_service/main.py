from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
def get_users():
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

@app.post("/users")
def create_user():
    return {"message": "User created"}

@app.get("/status")
def status():
    return {"status": "Mock service is healthy"}
