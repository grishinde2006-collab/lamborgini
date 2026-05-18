# Базовый образ с Python 
FROM python:3.13-slim

# Принудительно указываем SQLite
ENV DATABASE_URL=sqlite:///db.sqlite3
ENV DISABLE_DATABASE_ENV_CHECK=true

# Отключаем буферизацию вывода
ENV PYTHONUNBUFFERED 1

# Создаём рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Открываем порт
EXPOSE 8000

# Команда запуска 
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
