

import os


class Settings:
    def __init__(self):
        self.DEBUG = os.getenv("DEBUG", "true").lower() == "true"
        self.SECRET_KEY = os.getenv("SECRET_KEY", "mikusecret")
        self.APP_NAME = os.getenv("APP_NAME", "MikuAPI")
        self.VERSION = os.getenv("VERSION", "0.1.0")


settings = Settings()