from __future__ import annotations

from database import SessionLocal
from models import ImplantModel, SideEffectModel
from schemas.enums import Category, Severity, Tier

IMPLANT_COUNT = 50

SIDE_EFFECT_TEMPLATES = (
    {
        "reference": "SE-HEADACHE",
        "name": "Headache",
        "severity": Severity.MILD,
        "description": "Transient discomfort during neural calibration.",
    },
    {
        "reference": "SE-NAUSEA",
        "name": "Nausea",
        "severity": Severity.MODERATE,
        "description": "Vestibular disturbance after synchronization.",
    },
    {
        "reference": "SE-INFLAMMATION",
        "name": "Inflammation",
        "severity": Severity.SEVERE,
        "description": "Localized tissue reaction requiring follow-up.",
    },
)


def _build_prerequisites(index: int) -> dict[str, int | None]:
    return {
        "minAge": 18 + (index % 5),
        "maxAge": 55 + (index % 15),
        "minSize": 145 + (index % 10),
        "maxSize": 190 + (index % 12),
        "minWeight": 45 + (index % 8),
        "maxWeight": 95 + (index % 10),
    }


IMPLANT_NAMES = {
    Category.NEURAL: [
        "CortexLink",
        "Synapse Relay",
        "Myelin Mesh",
        "NeuroFuse",
        "Cranial Array",
        "Signal Lattice",
        "Axon Gate",
        "Cerebral Node",
        "Pulse Thread",
        "Thought Bridge",
    ],
    Category.SENSORY: [
        "Optic Bloom",
        "Auditory Lattice",
        "Tactile Veil",
        "Spectral Lens",
        "Sensory Mesh",
        "Retina Thread",
        "Vibrance Array",
        "Echo Crown",
        "Signal Bloom",
        "Perception Grid",
    ],
    Category.MOTOR: [
        "Torque Anchor",
        "Kinetic Spine",
        "Flexion Core",
        "Motion Tether",
        "Stride Relay",
        "Servo Thread",
        "Joint Matrix",
        "Power Lattice",
        "Muscle Sync",
        "Limb Mesh",
    ],
    Category.METABOLIC: [
        "Nutrient Gate",
        "Cellular Regulator",
        "Flux Array",
        "Metabolic Core",
        "Balance Mesh",
        "Biofilter Node",
        "Vital Lattice",
        "Assimilation Drive",
        "Homeostasis Thread",
        "Metabolic Crown",
    ],
    Category.CARDIOVASCULAR: [
        "Heartline Coil",
        "Pulse Beacon",
        "Vascular Mesh",
        "Flow Anchor",
        "Circulation Core",
        "Hemodynamic Thread",
        "Aortic Relay",
        "Cardio Lattice",
        "Pulse Matrix",
        "Valve Sync",
    ],
    Category.DERMAL: [
        "Skin Shield",
        "Thermal Veil",
        "Barrier Mesh",
        "Dermal Weave",
        "Shield Lattice",
        "Protective Thread",
        "Cell Guard",
        "Barrier Core",
        "Skin Relay",
        "Thermal Anchor",
    ],
}


def _implant_description(index: int, category: Category, tier: Tier, name: str) -> str:
    benefit_map = {
        Category.NEURAL: "restores cortical signal fidelity and cuts synaptic delay during high-load neural tasks.",
        Category.SENSORY: "sharpens sensory input, stabilizes perception, and improves contextual awareness in noisy environments.",
        Category.MOTOR: "increases biomechanical control, smooths movement, and reduces fatigue under sustained exertion.",
        Category.METABOLIC: "regulates nutrient transfer and keeps homeostatic rhythms stable during stress or recovery.",
        Category.CARDIOVASCULAR: "supports circulatory efficiency and maintains reliable flow under prolonged physical demand.",
        Category.DERMAL: "improves barrier resilience and thermal control while reducing irritation and tissue stress.",
    }
    tier_map = {
        Tier.SALVAGE: "a reclaimed device intended for emergency fallback and short-term stabilization",
        Tier.STANDARD: "a dependable field model built for everyday performance",
        Tier.CLINICAL: "a clinically validated implant engineered for precision and long-term safety",
        Tier.PRIME: "a premium implant designed for exceptional endurance and adaptive control",
        Tier.MILSPEC: "a hardened implant optimized for harsh operating environments and physical stress",
        Tier.PROTOTYPE: "an experimental platform designed for controlled testing and iterative refinement",
    }
    return (
        f"{name} is {tier_map[tier]} for users who need consistent performance in demanding conditions. "
        f"It {benefit_map[category]}"
    )


def _build_implant(index: int) -> ImplantModel:
    categories = list(Category)
    tiers = list(Tier)
    category = categories[index % len(categories)]
    tier = tiers[index % len(tiers)]
    name = IMPLANT_NAMES[category][index % len(IMPLANT_NAMES[category])]

    implant = ImplantModel(
        reference=f"REF{index + 1:03d}",
        name=name,
        description=_implant_description(index, category, tier, name),
        category=category,
        tier=tier,
        prerequisites=_build_prerequisites(index),
    )

    implant.side_effects = [
        SideEffectModel(
            reference=f"{template['reference']}-{index + 1:03d}",
            name=template["name"],
            severity=template["severity"],
            description=template["description"],
        )
        for template in SIDE_EFFECT_TEMPLATES[: 2 + (index % 2)]
    ]

    return implant


def seed_database() -> None:
    with SessionLocal() as db:
        db.query(SideEffectModel).delete()
        db.query(ImplantModel).delete()
        db.commit()

        implants = [_build_implant(index) for index in range(IMPLANT_COUNT)]
        implants_by_reference = {implant.reference: implant for implant in implants}

        for index, implant in enumerate(implants):
            incompatible_refs = {
                f"REF{((index + 1) % IMPLANT_COUNT) + 1:03d}",
                f"REF{((index + 7) % IMPLANT_COUNT) + 1:03d}",
            }
            implant.incompatible_implants = [
                implants_by_reference[reference]
                for reference in sorted(incompatible_refs)
                if reference != implant.reference
            ]

        db.add_all(implants)
        db.commit()
