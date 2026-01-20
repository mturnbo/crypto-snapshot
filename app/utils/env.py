import os
from functools import lru_cache
from dotenv import load_dotenv


@lru_cache
def load_env() -> bool:
    load_dotenv()
    return True


def get_env(key: str, default: str | None = None) -> str | None:
    load_env()
    return os.getenv(key, default)