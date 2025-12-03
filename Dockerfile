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
    libglib2.0-0 \
    libnss3 \
    libgobject-2.0-0 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libatspi2.0-0 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxshmfence1 \
    libglu1-mesa \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libxext6 \
    libxfixes3 \
    libxcursor1 \
    libx11-6 \
    libx11-xcb1 \
    libxss1 \
    libdrm2 \
    libexpat1 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libxrender1 \
    libxcb1 \
    wget \
  && rm -rf /var/lib/apt/lists/*

# Copiamos requirements e instalamos dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN playwright install


# Copiamos el script de entrada
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# El código vendrá montado por volumen (./app)
# Exponemos puerto 8000 para quien quiera mapearlo
EXPOSE 8000

CMD ["bash", "-c", "/entrypoint.sh && python manage.py runserver 0.0.0.0:8000"]
