from fastapi import APIRouter

router = APIRouter(prefix="/components")

@router.get("/")
async def list_components():
    return {"message": ["Component 1", "Component 2", "Component 3"]}

@router.get("/{component_id}")
async def get_component(component_id: int):
    return {"message": f"Details of Component {component_id}"}