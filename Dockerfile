FROM python:3.11

# ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libpq-dev

WORKDIR /app

COPY requirements.txt /app/

# install asyncpg dependencies
RUN apt-get update && apt-get install -y postgresql gcc python3-dev musl-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# COPY ./entrypoint.sh .

COPY . /app/

# Запускаем бота
CMD ["python", "bot/bot.py"]



