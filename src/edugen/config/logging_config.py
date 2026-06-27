from logging.config import dictConfig

from edugen.config.settings import AppSettings


def configure_logging(settings: AppSettings) -> None:
    settings.log_dir.mkdir(parents=True, exist_ok=True)

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s %(levelname)s [%(name)s] %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": settings.log_level,
                },
                "app_file": {
                    "class": "logging.FileHandler",
                    "filename": str(settings.log_dir / "app.log"),
                    "formatter": "default",
                    "level": "INFO",
                },
                "debug_file": {
                    "class": "logging.FileHandler",
                    "filename": str(settings.log_dir / "debug.log"),
                    "formatter": "default",
                    "level": "DEBUG",
                },
                "warning_file": {
                    "class": "logging.FileHandler",
                    "filename": str(settings.log_dir / "warning.log"),
                    "formatter": "default",
                    "level": "WARNING",
                },
                "error_file": {
                    "class": "logging.FileHandler",
                    "filename": str(settings.log_dir / "error.log"),
                    "formatter": "default",
                    "level": "ERROR",
                },
            },
            "root": {
                "handlers": ["console", "app_file", "debug_file", "warning_file", "error_file"],
                "level": settings.log_level,
            },
        }
    )
