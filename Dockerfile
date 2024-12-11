# syntax=docker/dockerfile:1.4

FROM python:3.12-slim-bullseye AS builder

WORKDIR /app

# Upgrade pip and install wheel
RUN pip install --no-cache-dir --upgrade pip wheel

# Set pip to use faster mirror and configure pip
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn \
    && pip config set global.timeout 1000 \
    && pip config set global.retries 3

# Copy only requirements first for better caching
COPY requirements.txt .

# Install dependencies with all optimizations (removed --no-deps)
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt \
    && pip install --no-cache-dir --compile --find-links=/wheels -r requirements.txt

FROM python:3.12-slim-bullseye

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/

# Copy your application
COPY . .

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PYTHONFAULTHANDLER=1 \
    PYTHONOPTIMIZE=2

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
