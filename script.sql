# Acceder a la consola de PostgreSQL
sudo -u postgres psql          # Linux / macOS
# En Windows: abrir pgAdmin o usar la consola psql desde el menú de inicio

# Dentro de la consola psql
CREATE USER lopez_cursos_user WITH PASSWORD 'lopez_cursos_pass';
CREATE DATABASE lopez_cursos_db OWNER lopez_cursos_user;
GRANT ALL PRIVILEGES ON DATABASE lopez_cursos_db TO lopez_cursos_user;
\q

mkdir -p store/models store/serializers store/views store/tests

touch cursos/models/__init__.py
touch cursos/serializers/__init__.py
touch cursos/views/__init__.py
touch cursos/tests/__init__.py
touch cursos/filters.py
touch cursos/permissions.py