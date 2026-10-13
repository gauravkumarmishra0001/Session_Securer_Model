FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER appuser
EXPOSE 8080
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--workers=2", "--access-logfile=-", "--error-logfile=-", "app:create_app()"]
