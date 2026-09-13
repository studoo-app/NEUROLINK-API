from sqlalchemy.orm import Session

from models import ApiKeyModel
from schemas.enums import ApiKeyRole
from security.hashing import generate_api_key, hash_api_key


def create_api_key(
    db: Session,
    name: str,
    role: ApiKeyRole,
) -> tuple[ApiKeyModel, str]:

    api_key, key_id = generate_api_key()

    db_api_key = ApiKeyModel(
        name=name,
        key_id=key_id,
        key_hash=hash_api_key(api_key),
        role=role,
        is_active=True,
    )

    db.add(db_api_key)

    db.commit()

    db.refresh(db_api_key)

    return db_api_key, api_key
