import os

from werkzeug.utils import import_string

from .base import Config as _ConfigType

_env = os.environ.get("FLASK_ENV", "development")
_Config = import_string(f"settings.{_env}.Config")

config: _ConfigType = _Config()
