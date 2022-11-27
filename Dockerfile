FROM python:3.10-bullseye

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -U -r requirements.txt

COPY . .

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
