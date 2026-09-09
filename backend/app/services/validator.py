from typing import Any, Tuple
from app.models.schemas import HF3DProject

def validate_hf3d_payload(raw_data: dict[str, Any]) -> Tuple[bool, str, dict[str, Any]]:
    """
    Validate .hf3d sculpt session file format.
    Checks:
    1. Magic header ("HF3D")
    2. Format version (>= 1)
    3. Structural schema compliance
    4. Offset array size multiples of 3 (X, Y, Z displacement components)
    5. Finite float values
    """
    try:
        project = HF3DProject.model_validate(raw_data)
        
        total_offsets = 0
        min_bound = [float("inf"), float("inf"), float("inf")]
        max_bound = [float("-inf"), float("-inf"), float("-inf")]

        for part in project.mesh.parts:
            offsets = part.sculptOffsets
            if len(offsets) % 3 != 0:
                return False, f"Part '{part.name}' sculptOffsets length {len(offsets)} is not divisible by 3 (X, Y, Z tuples required).", {}
            
            total_offsets += len(offsets) // 3
            for i in range(0, len(offsets), 3):
                ox, oy, oz = offsets[i], offsets[i+1], offsets[i+2]
                min_bound[0] = min(min_bound[0], ox)
                min_bound[1] = min(min_bound[1], oy)
                min_bound[2] = min(min_bound[2], oz)
                max_bound[0] = max(max_bound[0], ox)
                max_bound[1] = max(max_bound[1], oy)
                max_bound[2] = max(max_bound[2], oz)

        analysis = {
            "version": project.version,
            "partsCount": len(project.mesh.parts),
            "deformedVertices": total_offsets,
            "shape": project.mesh.shape,
            "material": project.mesh.material,
            "brushMode": project.brush.mode,
            "keyframesCount": len(project.animation.keyframes) if project.animation else 0,
            "boundingBox": {
                "min": min_bound if total_offsets > 0 else [0, 0, 0],
                "max": max_bound if total_offsets > 0 else [0, 0, 0]
            }
        }
        return True, "Valid HandForge .hf3d payload", analysis

    except Exception as e:
        return False, f"Schema validation error: {str(e)}", {}
