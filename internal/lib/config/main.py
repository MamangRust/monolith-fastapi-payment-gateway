from functools import lru_cache

from lib.config.app import AppSettings
from lib.config.base import AppEnvTypes, BaseAppSettings
from lib.config.production import ProdAppSettings
from lib.config.development import DevAppSettings
from lib.config.test import TestAppSettings

AppEnvType = DevAppSettings | TestAppSettings | ProdAppSettings

environments: dict[str, type[AppEnvType]] = {
    AppEnvTypes.development: DevAppSettings,
    AppEnvTypes.testing: TestAppSettings,
    AppEnvTypes.production: ProdAppSettings,
}

@lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env

    config = environments[app_env]
    return config() 

