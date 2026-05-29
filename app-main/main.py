from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import os
import jwt

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY", "domyslny-sekret")

@app.get("/")
def root_redirect():
    return RedirectResponse(url="/main")

@app.get("/main", response_class=HTMLResponse)
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <title>Główny Moduł Aplikacji</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f9fafb; margin: 0; padding: 40px; color: #1f2937; }
            .dashboard { background: #ffffff; padding: 30px; border: 1px solid #e5e7eb; border-radius: 6px; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1); max-width: 800px; margin: auto; }
            .dashboard h1 { margin-top: 0; font-size: 1.5rem; border-bottom: 1px solid #e5e7eb; padding-bottom: 15px; margin-bottom: 20px; color: #111827; }
            .btn-group { margin-bottom: 20px; }
            button { padding: 8px 16px; margin-right: 10px; font-size: 0.875rem; font-weight: 500; border: none; border-radius: 4px; cursor: pointer; transition: background-color 0.2s; }
            .btn-primary { background-color: #2563eb; color: white; }
            .btn-primary:hover { background-color: #1d4ed8; }
            .btn-danger { background-color: #dc2626; color: white; }
            .btn-danger:hover { background-color: #b91c1c; }
            .btn-outline { background-color: white; color: #374151; border: 1px solid #d1d5db; text-decoration: none; padding: 7px 15px; display: inline-block; font-size: 0.875rem; border-radius: 4px; }
            .btn-outline:hover { background-color: #f3f4f6; }
            .data-display { background: #1f2937; color: #f3f4f6; padding: 15px; border-radius: 4px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 0.875rem; white-space: pre-wrap; word-break: break-all; min-height: 100px;}
        </style>
    </head>
    <body>
        <div class="dashboard">
            <h1>Pulpit Nawigacyjny</h1>
            <div class="btn-group">
                <button class="btn-primary" onclick="pobierzDane()">Pobierz chronione dane</button>
                <button class="btn-danger" onclick="wyloguj()">Wyloguj</button>
                <a href="/auth/login" class="btn-outline">Moduł uwierzytelniania</a>
            </div>
            <div class="data-display" id="wynik">System w gotowości. Czekam na żądanie...</div>
        </div>
        
        <script>
            async function pobierzDane() {
                const token = localStorage.getItem('token');
                try {
                    const response = await fetch('/api/data', {
                        headers: { 'Authorization': token ? 'Bearer ' + token : '' }
                    });
                    
                    if (!response.ok) {
                        const errorData = await response.json();
                        document.getElementById('wynik').textContent = "BŁĄD " + response.status + "\\nSzczegóły: " + errorData.detail;
                        return;
                    }
                    
                    const data = await response.json();
                    document.getElementById('wynik').textContent = JSON.stringify(data, null, 2);
                } catch (error) {
                    document.getElementById('wynik').textContent = "Błąd komunikacji z API.";
                }
            }

            function wyloguj() {
                localStorage.removeItem('token');
                document.getElementById('wynik').textContent = "Sesja zakończona. Token usunięty z pamięci lokalnej.";
            }
        </script>
    </body>
    </html>
    """
    return html_content

@app.get("/api/data")
def data(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Brak nagłówka autoryzacyjnego.")
    
    token = authorization.split("Bearer ")[1]
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = payload.get("sub")
        
        return {
            "status": "sukces",
            "autoryzacja": f"Pomyślnie zweryfikowano token JWT dla użytkownika: {user}",
            "dane_infrastruktury": [
                {"serwer": "app_main", "obciazenie": "12%"},
                {"serwer": "app_auth", "obciazenie": "4%"}
            ]
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token wygasł. Zaloguj się ponownie.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Nieprawidłowy podpis tokenu.")