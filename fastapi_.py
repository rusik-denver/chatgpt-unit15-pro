from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# создаем объект приложения
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello to the Calculator App!"}

@app.get("/add/{a}/{b}/")
def add(a, b):
    return HTMLResponse(f"{a} + {b} = {int(a)+int(b)}")

@app.get("/subtract/{a}/{b}/")
def subtract(a, b):
    return HTMLResponse(f"{a} - {b} = {int(a)-int(b)}")

@app.get("/divide/{a}/{b}/")
def divide(a, b):
    if int(b) == 0:
        return HTMLResponse(f"Error: Division by zero")
    return HTMLResponse(f"{a} / {b} = {int(a)/int(b)}")

@app.get("/multiply/{a}/{b}/")
def multiply(a, b):
    return HTMLResponse(f"{a} * {b} = {int(a)*int(b)}")