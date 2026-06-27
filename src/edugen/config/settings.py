from dataclasses import dataclass
from pathlib import Path
import os

from edugen.config.constants import APP_NAME, APP_TAGLINE, APP_VERSION


@dataclass(frozen=True)
class AppSettings:
    app_name: str = APP_NAME
    tagline: str = APP_TAGLINE
    version: str = APP_VERSION
    environment: str = os.getenv("EDUGEN_ENV", "development")
    log_level: str = os.getenv("EDUGEN_LOG_LEVEL", "INFO")
    database_path: Path = Path(os.getenv("EDUGEN_DATABASE_PATH", "database/edugen.db"))
    log_dir: Path = Path("logs")
