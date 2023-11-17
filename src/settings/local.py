from dataclasses import dataclass
from envparse import env

from settings.base import Config as BaseConfig


@dataclass
class Config(BaseConfig):
    FLASK_ENV: str = env("FLASK_ENV", default="local")
