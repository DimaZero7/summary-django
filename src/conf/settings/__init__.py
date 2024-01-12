from split_settings.tools import include as settings_include
from split_settings.tools import optional

settings_include(
    "toml.py",
    "installed_apps.py",
    "base.py",
    optional("local_settings.py"),
)
