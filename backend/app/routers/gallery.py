from fastapi import APIRouter, Query
from app.models.schemas import GalleryItem
from app.services.redis_service import gallery_service

router = APIRouter(prefix="/api/v1/gallery", tags=["Gallery"])

@router.get("/top")
def get_top_models(
    limit: int = Query(10, ge=1, le=50),
    min_likes: int = Query(0, ge=0)
):
    """
    Retrieve top community sculpt models from Redis 7 Sorted Sets.
    Demonstrates sub-10ms query performance.
    """
    items, latency_ms = gallery_service.query_top_sculpts(limit=limit, min_likes=min_likes)
    return {
        "items": items,
        "count": len(items),
        "queryLatencyMs": round(latency_ms, 3),
        "slaTargetMs": 10.0,
        "withinSla": latency_ms < 10.0
    }

@router.post("/submit")
def submit_model(item: GalleryItem):
    """Store community sculpt model in Redis 7 Sorted Set."""
    latency_ms = gallery_service.add_gallery_item(item)
    return {
        "status": "success",
        "itemId": item.id,
        "writeLatencyMs": round(latency_ms, 3)
    }
