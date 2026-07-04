FROM python:3.12-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 或者用 pyproject.toml
# COPY pyproject.toml .
# RUN pip install --no-cache-dir .

COPY . .
