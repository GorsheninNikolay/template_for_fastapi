from os import environ

from app.config.default import AppSettings


def get_settings() -> AppSettings:
    settings = AppSettings()
    env = environ.get("ENV", "local")
    if env == "local":
        return settings
    # ...
    # space for other settings
    # ...
    return settings  # fallback to default
