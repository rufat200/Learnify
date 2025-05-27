# Learnify – Educational Platform API

**Learnify** — это серверное API-приложение для образовательной платформы, разработанное с использованием Django и Django REST Framework. Проект предоставляет функциональность управления курсами, уроками, заданиями, а также систему уведомлений в реальном времени через WebSocket (Django Channels).

---

## 📦 Возможности

- Управление курсами, уроками и заданиями
- Разграничение ролей (преподаватель и студент)
- Загрузка и просмотр учебных материалов
- Уведомления о новых заданиях и комментариях в реальном времени
- Авторизация с использованием JWT токенов
- Асинхронные WebSocket-каналы через Django Channels и Redis

---

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/learnify.git
cd learnify
```

### 2. Создание виртуального окружения и его активация


```bash
python -m venv venv
```
MacOS/Linux
```bash
source venv/bin/activate
```
Windows
```bash
venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Запуск базы данных и Redis через Docker
#### для начала в главной директории проекта создай .env файл и заполни его по примеру.Только после этого запускай Docker и пропиши.

```bash
docker run -d -e POSTGRES_PASSWORD=<введи сюда пароль из .env> -p 5432:5432 postgres

docker run -d -p 6379:6379 redis
```

### 5. Применение миграций.

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Запуск сервера.

```bash
python manage.py runserver
```

## После запуска сервера перейдите по этой ссылке для регистрации нового пользователя

[http://127.0.0.1:8000/auth/users/me](http://127.0.0.1:8000/auth/users/me)
