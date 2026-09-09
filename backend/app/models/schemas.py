from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional

class Vector3Schema(BaseModel):
    x: float
    y: float
    z: float

class MeshPartSchema(BaseModel):
    name: str
    sculptOffsets: list[float] = Field(default_factory=list)
    rotation: Vector3Schema
    position: Vector3Schema

class BrushConfig(BaseModel):
    mode: Literal["push", "pull", "smooth", "inflate", "flatten", "crease"]
    radius: float = Field(ge=0.01, le=5.0)
    strength: float = Field(ge=0.01, le=2.0)

class KeyframePartSchema(BaseModel):
    name: str
    rotation: Vector3Schema
    scale: float
    position: Vector3Schema

class KeyframeSchema(BaseModel):
    frame: int = Field(ge=0)
    parts: list[KeyframePartSchema]

class AnimationData(BaseModel):
    keyframes: list[KeyframeSchema] = Field(default_factory=list)
    totalFrames: int = Field(default=120, ge=1)
    fps: int = Field(default=30, ge=1, le=120)

class ProjectMesh(BaseModel):
    shape: str
    material: str
    parts: list[MeshPartSchema]
    rotation: Vector3Schema
    scale: float

class HF3DProject(BaseModel):
    magic: Literal["HF3D"]
    version: int = Field(ge=1)
    timestamp: int
    mesh: ProjectMesh
    brush: BrushConfig
    animation: Optional[AnimationData] = None

    @field_validator("magic")
    @classmethod
    def validate_magic_header(cls, v: str) -> str:
        if v != "HF3D":
            raise ValueError("Invalid magic header. Must be 'HF3D'")
        return v

class GalleryItem(BaseModel):
    id: str
    title: str
    author: str
    vertexCount: int
    likes: int = 0
    createdAt: int
    thumbnailUrl: Optional[str] = None
    project: Optional[dict] = None

class TelemetryFrame(BaseModel):
    timestamp: float
    fps: float
    handCount: int
    activeGesture: str
    vertexCount: int
    brushPressure: float
