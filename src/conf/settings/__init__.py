from split_settings.tools import include as settings_include
from split_settings.tools import optional

settings_include(
    "toml.py",
    "develop.py",
    "installed_apps.py",
    "database.py",
    "base.py",
    "rest.py",
    "swagger.py",
    "celery.py",
    optional("local_settings.py"),
)
