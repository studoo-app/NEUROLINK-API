from core import SessionLocal
from features.implants import ImplantModel, build_implant


def assign_incompatibilities(implants: list[ImplantModel]) -> None:
    seen_pairs: set[tuple[str, str]] = set()

    for implant in implants:
        for other in implant.incompatible_implants:
            seen_pairs.add(tuple(sorted((implant.reference, other.reference))))

    for index, implant in enumerate(implants):
        added = 0

        if len(implant.incompatible_implants) >= 2:
            continue

        for offset in (1, 7, 13, 19, 25):
            if added >= 2:
                break

            candidate = implants[(index + offset) % len(implants)]
            if candidate.reference == implant.reference:
                continue

            pair = tuple(sorted((implant.reference, candidate.reference)))
            if pair in seen_pairs:
                continue

            seen_pairs.add(pair)

            if candidate not in implant.incompatible_implants:
                implant.incompatible_implants.append(candidate)
            if implant not in candidate.incompatible_implants:
                candidate.incompatible_implants.append(implant)

            added += 1


def generate_additionnal_implants(additionnal_implants_nb: int = 10) -> None:
    with SessionLocal() as db:
        count_implants = db.query(ImplantModel).count()
        additional_implants = [
            build_implant(index)
            for index in range(count_implants, count_implants + additionnal_implants_nb)
        ]

        all_implants = db.query(ImplantModel).order_by(ImplantModel.reference).all()
        all_implants.extend(additional_implants)

        assign_incompatibilities(all_implants)

        db.add_all(additional_implants)
        db.commit()