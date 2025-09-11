from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    """
    Fetch all Property objects, cache them in Redis for 1 hour (3600s).
    """
    properties = cache.get("all_properties")

    if properties is None:  # cache miss
        properties = list(
            Property.objects.all().values(
                "id", "title", "description", "price", "location", "created_at"
            )
        )
        cache.set("all_properties", properties, 3600)  # cache for 1 hour

    return properties


def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate hit ratio.
    """
    conn = get_redis_connection("default")
    info = conn.info("stats")

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)

    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0.0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2),
    }

    logger.info(f"Redis cache metrics: {metrics}")
    return metrics
