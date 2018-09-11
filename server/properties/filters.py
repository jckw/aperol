from server.properties import models
from graphql_geojson.filters import GeometryFilterSet


class PropertyFilter(GeometryFilterSet):
    class Meta:
        model = models.Property
        fields = {
            'name': ['exact'],
            'location': ['exact', 'intersects', 'distance_lte'],
        }
