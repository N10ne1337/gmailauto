from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import random
from fake_useragent import UserAgent
import urllib.parse

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Gmail Auto-Registrar</title>
        </head>
        <body>
            <h1>Gmail Auto-Registrar</h1>
            <form method="post" action="/">
                <label for="username">Желаемое название почты:</label><br>
                <input type="text" id="username" name="username"><br>
                <label for="password">Желаемый пароль:</label><br>
                <input type="text" id="password" name="password"><br><br>
                <input type="radio" id="random" name="option" value="random">
                <label for="random">Случайные данные</label><br>
                <input type="radio" id="custom" name="option" value="custom" checked>
                <label for="custom">Ввести свои данные</label><br><br>
                <input type="submit" value="Регистрация">
            </form>
        </body>
        </html>
        """)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_data = urllib.parse.parse_qs(post_data)

        option = post_data.get('option', ['custom'])[0]
        if option == 'random':
            user_data = generate_user_data()
        else:
            user_data = {
                "username": post_data.get('username', ['user'])[0],
                "password": post_data.get('password', ['pass'])[0],
                "email": f"{post_data.get('username', ['user'])[0]}@gmail.com",
                "user_agent": UserAgent().random
            }

        success = register_gmail_account(user_data)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Registration Result</title>
        </head>
        <body>
        """)
        if success:
            self.wfile.write(b"<h1>Аккаунт успешно создан!</h1>")
            self.wfile.write(f"<p>Имя пользователя: {user_data['username']}</p>".encode())
            self.wfile.write(f"<p>Пароль: {user_data['password']}</p>".encode())
        else:
            self.wfile.write(b"<h1>Не удалось создать аккаунт!</h1>")
        self.wfile.write(b"""
        </body>
        </html>
        """)

def generate_user_data():
    ua = UserAgent()
    username = f"user{random.randint(1000, 9999)}"
    password = f"Pass{random.randint(10000, 99999)}!"
    email = f"{username}@gmail.com"
    return {
        "username": username,
        "password": password,
        "email": email,
        "user_agent": ua.random
    }

def register_gmail_account(user_data):
    url = "https://accounts.google.com/signup"
    headers = {
        "User-Agent": user_data["user_agent"]
    }

    payload = {
        "username": user_data["username"],
        "password": user_data["password"],
        "email": user_data["email"]
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            print(f"Аккаунт создан: {user_data['email']}")
            return True
        else:
            print(f"Не удалось создать аккаунт: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 3000), Handler)
    print("Сервер запущен на порту 3000")
    server.serve_forever()
