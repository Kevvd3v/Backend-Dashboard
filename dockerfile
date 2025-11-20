FROM python:3.11-slim
WORKDIR /app
ENV PYTHONPATH /app
# 1. Copiar solo requirements.txt para aprovechar el caché de Docker
COPY requirements.txt .
# 2. Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt
# 3. Copiar todo el código fuente del proyecto (*ahora* incluyendo la carpeta 'app')
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]