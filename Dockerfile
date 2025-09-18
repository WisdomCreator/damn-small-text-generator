FROM python:3.12.11-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev libpq-dev \
  && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv 
RUN uv sync --frozen --no-dev

COPY . .

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]