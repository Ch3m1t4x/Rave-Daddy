#!/usr/bin/env bash
set -e

# Esperar a que la base de datos esté lista
echo "Esperando a la base de datos..."

i=0
until python - <<PY
import os, sys, psycopg2
try:
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    db = os.getenv("POSTGRES_DB")
    host = os.getenv("POSTGRES_HOST", "db")
    port = os.getenv("POSTGRES_PORT", "5432")
    conn = psycopg2.connect(dbname=db, user=user, password=password, host=host, port=port)
    conn.close()
    print("DB lista ✅")
    sys.exit(0)
except Exception as e:
    print("DB no disponible:", e)
    sys.exit(1)
PY
do
  i=$((i+1))
  if [ $i -ge 30 ]; then
    echo "❌ No se ha podido conectar a la base de datos tras varios intentos. Abortando."
    exit 1
  fi
  sleep 1
done

echo "Aplicando migraciones..."
python manage.py migrate --noinput

# Crear superusuario si variables definidas
if [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "Creando superusuario..."
  python manage.py createsuperuser --noinput || true
fi

echo "Recogiendo archivos estáticos..."
# Descomentar el collectstatic en producción
# python manage.py collectstatic --noinput

echo "Iniciando servidor Django 🐍"
exec "$@"