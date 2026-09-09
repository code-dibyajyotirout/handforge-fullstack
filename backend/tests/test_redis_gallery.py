import pytest
from app.models.schemas import GalleryItem
from app.services.redis_service import RedisGalleryService

def test_redis_gallery_sorted_set_query_latency():
    service = RedisGalleryService()
    
    # Query top models
    models, latency_ms = service.query_top_sculpts(limit=5)
    assert len(models) >= 3
    # Verify descending order of likes
    assert models[0]["likes"] >= models[1]["likes"]
    # SLA check: latency should be well under 10ms
    assert latency_ms < 10.0

def test_redis_gallery_add_item():
    service = RedisGalleryService()
    new_item = GalleryItem(
        id="test_sculpt_999",
        title="Test Neon Torus",
        author="Tester",
        vertexCount=12000,
        likes=9999,
        createdAt=1741564800
    )
    write_latency = service.add_gallery_item(new_item)
    assert write_latency < 10.0

    models, _ = service.query_top_sculpts(limit=1)
    assert models[0]["id"] == "test_sculpt_999"
    assert models[0]["likes"] == 9999
