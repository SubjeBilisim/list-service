FROM python:3.8-slim AS base

FROM base AS builder
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
RUN pip install --upgrade pip
COPY ./requirements ./requirements

FROM builder AS dev
RUN pip install -r requirements/dev.txt
COPY . .
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]

FROM builder AS prod
RUN pip install -r requirements/prod.txt
COPY . .
EXPOSE 8080
CMD ["/app/deployment/init_container.sh"]
