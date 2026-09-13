from database import SessionLocal, get_db, get_session
from schemas.enums import ApiKeyRole
from services.api_key import create_api_key


def main() -> None:
    db = get_session()

    try:
        db_key, api_key = create_api_key(
            db=db,
            name="Initial admin",
            role=ApiKeyRole.ADMIN,
        )

        print()
        print("Admin API key created")
        print()
        print(f"Key ID : {db_key.key_id}")
        print(f"API Key: {api_key}")
        print()

        print(
            "Save this key now. "
            "It will not be displayed again."
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()