import pytest
from app.services.validator import validate_hf3d_payload

def test_valid_hf3d_payload():
    payload = {
        "magic": "HF3D",
        "version": 2,
        "timestamp": 1741564800000,
        "mesh": {
            "shape": "sphere",
            "material": "clay",
            "parts": [
                {
                    "name": "base_mesh",
                    "sculptOffsets": [0.1, -0.2, 0.3, 0.0, 0.5, -0.1],
                    "rotation": {"x": 0.0, "y": 0.0, "z": 0.0},
                    "position": {"x": 0.0, "y": 0.0, "z": 0.0}
                }
            ],
            "rotation": {"x": 0.0, "y": 0.0, "z": 0.0},
            "scale": 1.0
        },
        "brush": {
            "mode": "push",
            "radius": 0.4,
            "strength": 0.35
        },
        "animation": {
            "keyframes": [],
            "totalFrames": 120,
            "fps": 30
        }
    }
    valid, message, analysis = validate_hf3d_payload(payload)
    assert valid is True
    assert analysis["version"] == 2
    assert analysis["deformedVertices"] == 2
    assert analysis["shape"] == "sphere"

def test_invalid_magic_header():
    payload = {
        "magic": "INVALID",
        "version": 2,
        "timestamp": 1741564800000,
        "mesh": {
            "shape": "sphere",
            "material": "clay",
            "parts": [],
            "rotation": {"x": 0, "y": 0, "z": 0},
            "scale": 1.0
        },
        "brush": {"mode": "push", "radius": 0.4, "strength": 0.35}
    }
    valid, message, analysis = validate_hf3d_payload(payload)
    assert valid is False
    assert "magic" in message.lower()

def test_invalid_offsets_length():
    payload = {
        "magic": "HF3D",
        "version": 2,
        "timestamp": 1741564800000,
        "mesh": {
            "shape": "sphere",
            "material": "clay",
            "parts": [
                {
                    "name": "part1",
                    "sculptOffsets": [0.1, 0.2],  # Not divisible by 3
                    "rotation": {"x": 0, "y": 0, "z": 0},
                    "position": {"x": 0, "y": 0, "z": 0}
                }
            ],
            "rotation": {"x": 0, "y": 0, "z": 0},
            "scale": 1.0
        },
        "brush": {"mode": "push", "radius": 0.4, "strength": 0.35}
    }
    valid, message, analysis = validate_hf3d_payload(payload)
    assert valid is False
    assert "divisible by 3" in message
