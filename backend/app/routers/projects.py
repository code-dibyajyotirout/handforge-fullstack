from fastapi import APIRouter, HTTPException, Body
from typing import Any
from app.services.validator import validate_hf3d_payload
from app.services.obj_exporter import parse_obj_mesh_stream

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])

@router.post("/validate")
def validate_project(payload: dict[str, Any] = Body(...)):
    """Validate a .hf3d sculpt session file and compute bounding box / topology statistics."""
    valid, message, analysis = validate_hf3d_payload(payload)
    if not valid:
        raise HTTPException(status_code=422, detail=message)
    return {
        "status": "success",
        "message": message,
        "analysis": analysis
    }

@router.post("/obj-inspect")
def inspect_obj(payload: dict[str, str] = Body(...)):
    """Inspect client-generated Wavefront OBJ text payload."""
    raw_obj = payload.get("content", "")
    valid, message, summary = parse_obj_mesh_stream(raw_obj)
    if not valid:
        raise HTTPException(status_code=400, detail=message)
    return {
        "status": "success",
        "message": message,
        "summary": summary
    }
