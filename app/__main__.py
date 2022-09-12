import logging

from fastapi import FastAPI

from app.config.default import AppSettings
from app.endpoints import list_of_routes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s\t" "%(levelname)s\t" "%(name)s\t" "%(message)s\t",
    datefmt='%H:%M:%S',
    encoding='utf8',
)

settings = AppSettings()


def bind_routes(application: FastAPI, setting: AppSettings) -> None:
    """Bind all Routes"""
    for route in list_of_routes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = 'Description'

    tags_metadata = [
        {
            'name': 'Health check',
            'description': 'API health check.',
        }
    ]

    application = FastAPI(
        title='Title application',
        description=description,
        docs_url='/swagger',
        openapi_url='/openapi',
        version='1.0.0',
        openapi_tags=tags_metadata,
    )
    bind_routes(application, settings)
    application.state.settings = settings
    return application


app = get_app()
