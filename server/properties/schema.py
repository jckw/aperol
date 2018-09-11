import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
# Contains a converter for Point to Geometry Field
from graphql_geojson import converter
from graphene_django.filter import DjangoFilterConnectionField
from server.properties.models import (
    Property, LettingAgency, City, CityArea, PropertyPhoto
)
from server.properties.filters import PropertyFilter


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

    property = relay.Node.Field(PropertyType)
    agency = relay.Node.Field(LettingAgencyType)
    filtered_properties = DjangoFilterConnectionField(
        PropertyType, filterset_class=PropertyFilter)

    def resolve_all_properties(self, info, **kwargs):
        return Property.objects.all()
