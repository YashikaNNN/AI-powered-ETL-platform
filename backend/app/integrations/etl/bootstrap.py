import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def ensure_etl_importable() -> Path:
    root = repo_root()
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    return root


def configure_etl_database(sync_database_url: str) -> None:
    ensure_etl_importable()
    from etl.config import settings as etl_settings

    etl_settings.database_url = sync_database_url
