""" Модуль для сокрытия данных """

import os

from dotenv import load_dotenv
from pydantic import BaseSettings, SecretStr, StrictStr


load_dotenv()


class SiteSettings(BaseSettings):
    api_key: SecretStr = os.getenv('API_KEY', None)
    api_token: SecretStr = os.getenv('API_TOKEN', None)
    api_host_common: StrictStr = os.getenv('API_HOST_COMMON', None)
    api_host_top: StrictStr = os.getenv('API_HOST_TOP', None)
