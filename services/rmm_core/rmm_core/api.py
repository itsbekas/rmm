import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .db import Session as DatabaseSession
from .util import get_env

from pydantic import BaseModel, ConfigDict

def to_camel(str):
    output = ''.join(x for x in str.title() if x.isalnum())
    return output[0].lower() + output[1:]

class ResponseModel(BaseModel):
    """
    Base response model for all API responses.
    Converts snake_case to camelCase.
    """
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


def get_app(router: APIRouter, name: str) -> tuple[FastAPI, str, int]:
    HOST: str = get_env("UVICORN_HOST")
    PORT: int = get_env("UVICORN_PORT", int)
    FRONTEND_URL: str = get_env("FRONTEND_URL")

    # Setup app
    app = FastAPI(
        title=f"Agisit - {name}",
        version="1.0.0",
        openapi_url="/api/v0/openapi.json",
        docs_url="/api/v0/docs",
        redoc_url="/api/v0/redoc",
    )

    # Cors
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[FRONTEND_URL],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Router
    app.include_router(router, prefix=f"/api/v0/{name}", tags=[name])

    return app, HOST, PORT


def get_session() -> Session:
    return DatabaseSession()


SessionDep = Annotated[Session, Depends(get_session)]


def get_user_id(user_id: str) -> uuid.UUID:
    return uuid.UUID(user_id)


UserIdDep = Annotated[uuid.UUID, Depends(get_user_id)]
