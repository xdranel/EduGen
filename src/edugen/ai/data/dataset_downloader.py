import hashlib
import shutil
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlretrieve
import tarfile
import zipfile

from edugen.core.exceptions import EduGenError


class DatasetDownloader:
    def __init__(self, download_dir: Path) -> None:
        self.download_dir = download_dir

    def download(self, url: str, checksum: str | None = None, extract: bool = False) -> Path:
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

        if extract:
            return self.extract(target)

        return target

    def extract(self, archive_path: Path) -> Path:
        extract_dir = self.download_dir / archive_path.stem
        extract_dir.mkdir(parents=True, exist_ok=True)

        if zipfile.is_zipfile(archive_path):
            with zipfile.ZipFile(archive_path) as archive:
                archive.extractall(extract_dir)
            return extract_dir

        if tarfile.is_tarfile(archive_path):
            with tarfile.open(archive_path) as archive:
                archive.extractall(extract_dir)
            return extract_dir

        raise EduGenError("Unsupported archive format.")

    @staticmethod
    def sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
