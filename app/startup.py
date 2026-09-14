from features.implants.seed import seed_database


def run_startup() -> None:
    seed_database()