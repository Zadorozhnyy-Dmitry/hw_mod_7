FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . .

# CMD ['sh', '-c', 'python manage.py migrate && python manage.py runserver 0.0.0.0:8000']
CMD ['python manage.py migrate && python manage.py runserver 0.0.0.0:8000']
