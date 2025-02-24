import requests
import random
from fake_useragent import UserAgent

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
        else:
            print(f"Не удалось создать аккаунт: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    # Запрос ввода от пользователя
    username = input("Введите имя пользователя (оставьте пустым для случайного): ")
    password = input("Введите пароль (оставьте пустым для случайного): ")

    if not username or not password:
        # Генерация случайных данных, если поля пустые
        user_data = generate_user_data()
    else:
        user_data = {
            "username": username,
            "password": password,
            "email": f"{username}@gmail.com",
            "user_agent": UserAgent().random
        }

    register_gmail_account(user_data)
