FROM python:3.11-slim-bullseye
WORKDIR /usr/src/repo-app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update -y \
  && apt-get -y install netcat gcc postgresql -y \
  && apt-get clean -y
RUN python -m venv venv
RUN . venv/bin/activate
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV FLASK_APP=/app
COPY . .
CMD ["gunicorn", "--bind", ":5000", "app:create_app()"]