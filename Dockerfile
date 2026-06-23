FROM python:3.11-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir fastapi "pydantic>=2,<3" pydantic-settings uvicorn && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pytest httpx

COPY . .

# Build falha se testes nao-integracao falharem.
RUN pytest -q -m "not integration"


FROM python:3.11-slim AS runner

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_NAME="Bella Tavola API"
ENV APP_VERSION="1.0.0"
ENV APP_DESCRIPTION="API do restaurante Bella Tavola"
ENV DEBUG="false"
ENV MAX_MESAS="20"
ENV MAX_PESSOAS_POR_MESA="10"
ENV MODEL_FILENAME="model.pkl"
ENV MODEL_VERSION="docker-local"

COPY requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir fastapi "pydantic>=2,<3" pydantic-settings uvicorn && \
    pip install --no-cache-dir -r requirements.txt

COPY main.py config.py model_utils.py database.py ./
COPY routers ./routers
COPY models ./models
COPY docs ./docs

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
