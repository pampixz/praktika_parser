# Используйте официальный образ Python
FROM python:3.12.4

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файлы проекта
COPY . /app

# Установите зависимости
RUN pip install -r requirements.txt





# Запустите бота при старте контейнера
CMD ["python", "parser_hh.py"]
