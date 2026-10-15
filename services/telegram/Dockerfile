FROM python:3.12-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 OMP_THREAD_LIMIT=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends poppler-utils tesseract-ocr tesseract-ocr-tur && rm -rf /var/lib/apt/lists/*
COPY services/telegram/requirements.txt /app/requirements.txt
RUN pip install --disable-pip-version-check -r requirements.txt
COPY services/telegram /app/services/telegram
RUN useradd --uid 10001 --create-home botuser && mkdir -p /data && chown botuser:botuser /data
USER botuser
VOLUME /data
CMD ["python", "-m", "services.telegram.bot"]
