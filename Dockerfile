FROM python:3.12-slim

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1 \
    libxcb1 \
    libx11-6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*


COPY backend/requirements.txt ./requirements.txt
ARG PIP_EXTRA_INDEX_URL
RUN pip install --no-cache-dir --extra-index-url ${PIP_EXTRA_INDEX_URL} -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]
