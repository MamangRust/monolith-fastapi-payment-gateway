from lib.config.app import AppSettings

class ProdAppSettings(AppSettings):
    class Config(AppSettings.Config):
        env_file = ".env"

    