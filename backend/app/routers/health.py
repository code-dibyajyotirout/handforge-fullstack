from fastapi import APIRouter
import time

router = APIRouter(tags=["Health"])

START_TIME = time.time()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "HandForge Distributed Backend",
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "engine": "WebGPU / Three.js Shading Language Ready",
        "redis_sorted_sets": "active",
        "cloud_edge": "Cloudflare Workers Compatible"
    }
