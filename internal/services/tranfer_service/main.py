import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from internal.services.tranfer_service.api.routes import router as api_router
from internal.lib.logging.logging_config import LoggerConfigurator
from internal.lib.config.main import get_app_settings

def create_app() -> FastAPI:
    settings = get_app_settings()

    application = FastAPI(**settings.fastapi_kwargs)


    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_router, prefix="/api")


    logger_configurator = LoggerConfigurator(logger_name="transfer-service")
    logger_configurator.configure_logger(json_logs=True)


    return application


app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=True)