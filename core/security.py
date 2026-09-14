import hashlib
import secrets

API_KEY_PREFIX = "sk"


def generate_api_key() -> tuple[str, str]:
    key_id = secrets.token_hex(4)
    secret = secrets.token_urlsafe(32)
    api_key = f"{API_KEY_PREFIX}_{key_id}_{secret}"
    return api_key, key_id


def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()


def extract_key_id(api_key: str) -> str | None:
    parts = api_key.split("_", maxsplit=2)
    if len(parts) != 3:
        return None

    prefix, key_id, _ = parts
    if prefix != API_KEY_PREFIX:
        return None

    return key_id