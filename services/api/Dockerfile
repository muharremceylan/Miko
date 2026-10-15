FROM python:3.12-slim
WORKDIR /app
COPY services/api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY services /app/services
COPY akademi_ai_prototip/content /app/akademi_ai_prototip/content
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN useradd --create-home appuser
USER appuser
CMD ["sh", "-c", "exec uvicorn services.api.app:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]
