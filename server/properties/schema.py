import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
# Not sure why, but importing this allows conversion of PointFields
from graphql_geojson import GeoJSONType
from server.properties.models import (
    Property, LettingAgency, City, CityArea, PropertyPhoto
)


class PropertyPhotoType(DjangoObjectType):
    class Meta:
        model = PropertyPhoto
        interfaces = (relay.Node, )


class PropertyPhotoConnection(relay.Connection):
    class Meta:
        node = PropertyPhotoType


class PropertyType(DjangoObjectType):
    class Meta:
        model = Property
        interfaces = (relay.Node, )
        exclude_fields = ('name',)

    node = relay.Node.Field()
    photos = relay.ConnectionField(PropertyPhotoConnection)

    def resolve_photos(self, info, **kwargs):
        return PropertyPhoto.objects.filter(property=self)


class PropertyConnection(relay.Connection):
    class Meta:
        node = PropertyType


class LettingAgencyType(DjangoObjectType):
    class Meta:
        model = LettingAgency
        interfaces = (relay.Node, )


class CityType(DjangoObjectType):
    class Meta:
        model = City
        interfaces = (relay.Node, )


class CityAreaType(DjangoObjectType):
    class Meta:
        model = CityArea
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    all_properties = relay.ConnectionField(PropertyConnection)
    property = relay.Node.Field(PropertyType)
    agency = relay.Node.Field(LettingAgencyType)

    def resolve_all_properties(self, info, **kwargs):
        return Property.objects.all()
