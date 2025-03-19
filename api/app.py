from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware

from .routers.v1 import v1_router

app = FastAPI(
    description="Плейер для говна",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно указать конкретные домены, например: ["https://your-ngrok-url.ngrok.io"]
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST, PUT и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)


@app.middleware("http")
async def increase_body_limit(request: Request, call_next):
    request.state.body = await request.body()  # Читаем тело запроса полностью
    response = await call_next(request)

    return response


@app.get("/")
def root():
    return {
        "message": "API work!",
    }

app.include_router(v1_router)
