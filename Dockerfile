# Usamos Python sobre Debian slim (buena compatibilidad)
FROM python:3.12-slim

# Variables de entorno que evitan .pyc y mejoran buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo
WORKDIR /usr/src/app

# Instalamos dependencias de sistema necesarias (postgre client libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gettext \
  && rm -rf /var/lib/apt/lists/*

# Copiamos requirements e instalamos dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiamos el script de entrada
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# El código vendrá montado por volumen (./app)
# Exponemos puerto 8000 para quien quiera mapearlo
EXPOSE 8000

CMD ["bash", "-c", "/entrypoint.sh && python manage.py runserver 0.0.0.0:8000"]
