from fastapi import FastAPI, Request, Form
from pydantic import BaseModel
import sqlite3
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="statix/htmls")

class User(BaseModel):
    name: str
    email: str

conn = sqlite3.connect("example.db")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              email TEXT)''')

conn.commit()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.post("/user")
async def create_user(request: Request, name: str = Form(...), email: str = Form(...)):
    user = User(name=name, email=email)


    c.execute("INSERT INTO users (name, email) VALUES (?, ?)", (user.name, user.email))
    conn.commit()

    return templates.TemplateResponse("index.html", {"request": request, "message": "User created successfully"})

@app.get("/users", response_class=HTMLResponse)
async def read_users(request: Request):
    c.execute("SELECT * FROM users")
    users = c.fetchall()

    return templates.TemplateResponse("users.html", {"request": request, "users": users})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
