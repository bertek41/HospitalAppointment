# syntax=docker/dockerfile:1
FROM python:3.10-slim as base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

FROM base AS python-deps
COPY ./requirements.txt .
RUN python -m venv /.venv
ENV PATH="/.venv/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

FROM base AS runtime
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

WORKDIR /code
COPY . /code/

RUN chmod +x run.sh

EXPOSE 8080

CMD ["python3", "./manage.py", "runserver", "0.0.0.0:8080"]
