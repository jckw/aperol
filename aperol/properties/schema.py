import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
# Contains a converter for Point to Geometry Field
from graphql_geojson import converter
from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Max, Min
from aperol.properties.models import (
    Property, LettingAgency, City, CityArea, PropertyPhoto
)
from aperol.properties.filters import PropertyFilter


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


class MetaType(graphene.ObjectType):
    max_price = graphene.Int()
    min_price = graphene.Int()
    max_bedrooms = graphene.Int()
    min_bedrooms = graphene.Int()

    def resolve_max_price(self, info):
        return Property.objects.all().aggregate(Max('price'))['price__max']

    def resolve_min_price(self, info):
        return Property.objects.all().aggregate(Min('price'))['price__min']

    def resolve_max_bedrooms(self, info):
        return Property.objects.all().aggregate(
            Max('bedrooms'))['bedrooms__max']

    def resolve_min_bedrooms(self, info):
        return Property.objects.all().aggregate(
            Min('bedrooms'))['bedrooms__min']


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    property = relay.Node.Field(PropertyType)
    agency = relay.Node.Field(LettingAgencyType)
    filtered_properties = DjangoFilterConnectionField(
        PropertyType, filterset_class=PropertyFilter)
    meta = graphene.Field(MetaType)

    def resolve_all_properties(self, info, **kwargs):
        return Property.objects.all()

    def resolve_meta(self, info):
        return MetaType()
