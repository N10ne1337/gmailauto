from http.server import BaseHTTPRequestHandler
   import requests
   import random
   import time
   from fake_useragent import UserAgent

   class Handler(BaseHTTPRequestHandler):
       def do_GET(self):
           self.send_response(200)
           self.send_header('Content-type', 'text/plain')
           self.end_headers()
           self.wfile.write(b"Gmail Auto-Registrar is running!\n")
           register_gmail_account()

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

   def register_gmail_account():
       url = "https://accounts.google.com/signup"
       user_data = generate_user_data()
       
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
           else:
               print(f"Не удалось создать аккаунт: {response.status_code}")
       except Exception as e:
           print(f"Ошибка: {e}")

   if __name__ == "__main__":
       from http.server import HTTPServer
       server = HTTPServer(('0.0.0.0', 3000), Handler)
       server.serve_forever()
