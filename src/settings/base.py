from dataclasses import dataclass

from envparse import env


@dataclass
class Config:
    SECRET_KEY: str = env("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI: str = env("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    def __getitem__(self, value):
        return self.__dict__.get(value)

    def __getattr__(self, value):
        return self.__dict__.get(value)
