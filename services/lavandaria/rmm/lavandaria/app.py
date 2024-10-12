import uvicorn
from fastapi import FastAPI

from rmm.lavandaria.router import router

app = FastAPI(
    title="API da Lavandaria",
    description="API para gestão das máquinas da lavandaria",
    version="0.1",
    docs_url="/",
)

app.include_router(router)


def run() -> None:
    uvicorn.run("rmm.lavandaria.app:app", host="localhost", port=8000, reload=True)


if __name__ == "__main__":
    run()
