from functools import lru_cache

from internal.lib.config.app import AppSettings
from internal.lib.config.base import AppEnvTypes, BaseAppSettings
from internal.lib.config.production import ProdAppSettings
from internal.lib.config.development import DevAppSettings
from internal.lib.config.test import TestAppSettings

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

