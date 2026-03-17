# Guía de Despliegue para Know U (Flask)

Tu proyecto usa **Flask**, un framework de Python que requiere un servidor activo para funcionar. **GitHub Pages** solo sirve archivos estáticos (HTML/CSS), por lo que no puede ejecutar `app.py`.

Aquí tienes los pasos para desplegar tu aplicación gratis usando **Render** (Recomendado).

---

## 1. Preparar el Proyecto

### Crear `requirements.txt`
Render necesita saber qué librerías usa tu proyecto. Ejecuta este comando en tu terminal para generar el archivo:

```bash
pip freeze > requirements.txt
```

Asegúrate de que `Flask`, `Flask-SQLAlchemy`, `Flask-Login`, `Flask-WTF`, y `Flask-Limiter` estén en la lista. Si no tienes `gunicorn`, instálalo y agrégalo: `pip install gunicorn`.

---

## 2. Desplegar en Render (vía GitHub)

1. **Sube tus cambios a GitHub**: Haz commit y push de todos tus archivos (incluyendo el nuevo `requirements.txt`).
2. **Crea una cuenta en [Render.com](https://render.com/)**: Regístrate con tu cuenta de GitHub.
3. **Nuevo Web Service**:
   - Haz clic en **"New +"** -> **"Web Service"**.
   - Conecta tu repositorio de GitHub.
4. **Configuración del Servicio**:
   - **Name**: `know-u-ecommerce` (o el que prefieras).
   - **Environment**: `Python 3`.
   - **Build Command**: `pip install -r requirements.txt`.
   - **Start Command**: `gunicorn app:app`.
   - **Plan**: Selecciona el plan **Free**.
5. **Variables de Entorno (Opcional pero Recomendado)**:
   - Ve a la pestaña **Environment** en Render.
   - Agrega `SECRET_KEY` con un valor seguro.

---

## 3. Consideraciones de Base de Datos

Tu aplicación usa **SQLite** (`know_u.db`). En el plan gratis de Render:
- El disco es efímero, lo que significa que **los datos (usuarios, productos nuevos) se borrarán cada vez que el servidor se reinicie**.
- **Solución**: Para un proyecto real, deberías usar una base de datos externa como **PostgreSQL** (Render ofrece una base de datos gratis por 90 días).

---

## 4. ¿Por qué salía en blanco?

GitHub Pages busca un archivo `index.html` y lo sirve como texto estático. Tu archivo `index.html` original intentaba cargar un script de `templates/index.html`, lo cual no funciona en un navegador sin un servidor Flask que procese las rutas.

---

### Verificación Local
Antes de subirlo, asegúrate de que corre en tu PC:
```bash
python app.py
```
Y visita `http://127.0.0.1:5000`.
