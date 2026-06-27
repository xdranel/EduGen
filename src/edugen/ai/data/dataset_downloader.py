import hashlib
import shutil
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlretrieve

from edugen.core.exceptions import EduGenError


class DatasetDownloader:
    def __init__(self, download_dir: Path) -> None:
        self.download_dir = download_dir

    def download(self, url: str, checksum: str | None = None) -> Path:
        self.download_dir.mkdir(parents=True, exist_ok=True)
        parsed = urlparse(url)
        filename = Path(parsed.path).name
        if not filename:
            raise EduGenError("Dataset URL must include a filename.")

        target = self.download_dir / filename
        if parsed.scheme == "file":
            shutil.copyfile(Path(parsed.path), target)
        elif parsed.scheme in {"http", "https"}:
            urlretrieve(url, target)
        else:
            raise EduGenError(f"Unsupported dataset URL scheme: {parsed.scheme}")

        if checksum and self.sha256(target) != checksum:
            target.unlink(missing_ok=True)
            raise EduGenError("Dataset checksum verification failed.")

        return target

    @staticmethod
    def sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
