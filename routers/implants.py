from fastapi import APIRouter

from schemas.Implant import Implant
from schemas.SideEffect import SideEffect
from schemas.prerequisites import Prerequisites
from schemas.enums import Tier, Category, Severity

router = APIRouter(prefix="/implants", tags=["Implant"])


@router.get("/" , response_model=list[Implant])
async def list_implants():
    prerequisites = Prerequisites(minAge=20, maxAge=30,minSize=150, maxSize=200, minWeight=50, maxWeight=100,incompatibleImplants=["REF001", "REF002"])

    implants = [
        Implant(reference="REF001", name="Component 1", category=Category.NEURAL, tier=Tier.STANDARD,prerequisites=Prerequisites(minAge=20, maxAge=30,minSize=150, maxSize=200, minWeight=50, maxWeight=100,incompatibleImplants=[ "REF002"]), sideseffects=[SideEffect(reference="REF01",name="Headache", severity=Severity.MILD,description="lorem ipsum ...."), SideEffect(reference="REF02",name="Nausea", severity=Severity.MODERATE, description="lorem ipsum ....")]),
        Implant(reference="REF002", name="Component 2", category=Category.SENSORY, tier=Tier.CLINICAL,prerequisites=Prerequisites(minAge=20, maxAge=30,minSize=150, maxSize=200, minWeight=50, maxWeight=100,incompatibleImplants=[]), sideseffects=[SideEffect(reference="REF01",name="Headache", severity=Severity.MILD,description="lorem ipsum ...."), SideEffect(reference="REF02",name="Nausea", severity=Severity.MODERATE, description="lorem ipsum ....")]),
        Implant(reference="REF003", name="Component 3", category=Category.MOTOR, tier=Tier.PRIME,prerequisites=Prerequisites(minAge=20, maxAge=30,minSize=150, maxSize=200, minWeight=50, maxWeight=100,incompatibleImplants=["REF001", "REF002"]), sideseffects=[SideEffect(reference="REF01",name="Headache", severity=Severity.MILD,description="lorem ipsum ...."), SideEffect(reference="REF02",name="Nausea", severity=Severity.MODERATE, description="lorem ipsum ....")])
    ]

    return implants


