# GO2 SPAIN — backend

Backend independiente que recibe y guarda los datos del formulario y las
reseñas de la página GO2 SPAIN (asesoría de extranjería). Separado del
proyecto AI Lead Machine para poder desplegarse solo, sin depender del
motor de chatbot de otras verticales.

## Endpoints

- `POST /study-leads` — guarda una solicitud del formulario (público).
- `GET /study-leads?key=...` — lista las solicitudes (protegido).
- `POST /reviews` — guarda una reseña sin publicar (público).
- `GET /reviews` — lista las reseñas ya publicadas (público).
- `GET /reviews/pending?key=...` — lista reseñas pendientes de revisar (protegido).
- `POST /reviews/{id}/publish?key=...` — publica una reseña (protegido).

`key` debe coincidir con la variable de entorno `ADMIN_KEY`.

## Desarrollo local

```bash
python -m venv .venv
.venv/Scripts/activate  # o source .venv/bin/activate en Mac/Linux
pip install -r requirements.txt
cp .env.example .env  # y rellena ADMIN_KEY
uvicorn main:app --reload
```

## Despliegue en Render

1. Sube este repositorio a GitHub.
2. En Render: **New → Blueprint**, selecciona el repositorio.
3. Rellena `ADMIN_KEY` cuando te lo pida (el resto lo define `render.yaml`).
4. Aplica — Render te da una URL fija que no cambia.
5. Actualiza `API_URL` en la página GO2 SPAIN con esa URL.
