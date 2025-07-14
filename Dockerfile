# Используем официальный образ Python
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Открываем порт (если нужен)
EXPOSE 8000

# Команда по умолчанию
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
