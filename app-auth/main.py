from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
import os
import jwt
from datetime import datetime, timedelta, timezone

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY", "domyslny-sekret")
EXPECTED_USER = os.getenv("ADMIN_USER", "brak_usera")
EXPECTED_PASS = os.getenv("ADMIN_PASS", "brak_hasla")

@app.get("/auth/login", response_class=HTMLResponse)
def login_view():
    html_content = """
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <title>System Logowania</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f3f4f6; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .login-panel { background: #ffffff; padding: 30px; border: 1px solid #e5e7eb; border-radius: 6px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); width: 100%; max-width: 380px; }
            .login-panel h2 { margin-top: 0; color: #111827; font-size: 1.25rem; font-weight: 600; border-bottom: 1px solid #e5e7eb; padding-bottom: 10px; margin-bottom: 20px; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; color: #374151; font-size: 0.875rem; font-weight: 500; }
            input { width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 4px; box-sizing: border-box; font-size: 0.875rem; }
            input:focus { outline: none; border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1); }
            button { width: 100%; padding: 10px; background-color: #2563eb; color: white; border: none; border-radius: 4px; font-weight: 500; cursor: pointer; transition: background-color 0.2s; }
            button:hover { background-color: #1d4ed8; }
            .footer-link { display: block; text-align: center; margin-top: 15px; color: #6b7280; text-decoration: none; font-size: 0.875rem; }
            .footer-link:hover { color: #111827; }
        </style>
    </head>
    <body>
        <div class="login-panel">
            <h2>Panel Uwierzytelniania</h2>
            <form id="loginForm">
                <div class="form-group">
                    <label for="username">Identyfikator użytkownika</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Hasło dostępowe</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit">Zaloguj</button>
            </form>
            <a href="/main" class="footer-link">Wróć do głównego modułu</a>
        </div>

        <script>
            document.getElementById('loginForm').addEventListener('submit', async function(e) {
                e.preventDefault(); 
                const formData = new FormData(e.target);
                const response = await fetch('/auth/login', { method: 'POST', body: formData });
                const data = await response.json();
                
                if (response.ok) {
                    localStorage.setItem('token', data.token);
                    window.location.href = "/main";
                } else {
                    alert("Błąd uwierzytelniania: " + data.detail);
                }
            });
        </script>
    </body>
    </html>
    """
    return html_content

@app.post("/auth/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username == EXPECTED_USER and password == EXPECTED_PASS:
        payload = {
            "sub": username,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        }
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        
        return {"token": encoded_jwt}
    
    raise HTTPException(status_code=401, detail="Nieprawidłowy identyfikator lub hasło.")