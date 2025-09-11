from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Fetch all Property objects, cache them in Redis for 1 hour (3600s).
    """
    properties = cache.get("all_properties")

    if properties is None:  # not in cache
        properties = list(
            Property.objects.all().values(
                "id", "title", "description", "price", "location", "created_at"
            )
        )
        cache.set("all_properties", properties, 3600)  # cache for 1 hour

    return properties
