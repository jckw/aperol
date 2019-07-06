from aperol.properties import models
from graphql_geojson.filters import GeometryFilterSet
import django_filters


class PropertyFilter(GeometryFilterSet):
    class Meta:
        model = models.Property
        fields = {
            "name": ["exact"],
            "location": ["exact", "intersects", "distance_lte"],
            "price": ["gte", "lte"],
            "total_price": ["gte", "lte"],
            "bedrooms": ["gte", "lte"],
        }
