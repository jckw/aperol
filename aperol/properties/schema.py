import graphene
from graphene import relay
from graphql import GraphQLError
from graphene_django.types import DjangoObjectType
# Contains a converter for Point to Geometry Field
from graphql_geojson import converter
from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Max, Min
from aperol.properties.models import (
    Property,
    LettingAgency,
    City,
    CityArea,
    PropertyPhoto,
    PropertyVariant,
    PropertyLandmarkDistance,
    Landmark
)
from aperol.properties.filters import PropertyFilter


class LandmarkType(DjangoObjectType):
    class Meta:
        model = Landmark
        interfaces = (relay.Node, )


class LandmarkConnection(relay.Connection):
    class Meta:
        node = LandmarkType


class PropertyLandmarkDistanceType(DjangoObjectType):
    class Meta:
        model = PropertyLandmarkDistance
        interfaces = (relay.Node, )


class PropertyLandmarkDistanceConnection(relay.Connection):
    class Meta:
        node = PropertyLandmarkDistanceType


class PropertyPhotoType(DjangoObjectType):
    class Meta:
        model = PropertyPhoto
        interfaces = (relay.Node, )


class PropertyPhotoConnection(relay.Connection):
    class Meta:
        node = PropertyPhotoType


class PropertyVariantType(DjangoObjectType):
    class Meta:
        model = PropertyVariant
        interfaces = (relay.Node, )


class PropertyType(DjangoObjectType):
    class Meta:
        model = Property
        interfaces = (relay.Node, )
        exclude_fields = ('name',)

    node = relay.Node.Field()
    photos = relay.ConnectionField(PropertyPhotoConnection)
    url = graphene.String()
    landmark_distances = relay.ConnectionField(
        PropertyLandmarkDistanceConnection)

    def resolve_photos(self, info, **kwargs):
        return PropertyPhoto.objects.filter(property=self)

    def resolve_url(self, info):
        return "/properties/{}/{}/{}".format(
            self.area.city.slug,
            self.area.slug,
            self.slug)

    def resolve_landmark_distances(self, info, **kwargs):
        return PropertyLandmarkDistance.objects.filter(property=self)


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
    landmarks = relay.ConnectionField(LandmarkConnection)

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

    def resolve_landmarks(self, info):
        return Landmark.objects.all()


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    property = graphene.Field(
        PropertyType,
        city_slug=graphene.String(required=True),
        area_slug=graphene.String(required=True),
        property_slug=graphene.String(required=True))
    agency = relay.Node.Field(LettingAgencyType)
    filtered_properties = DjangoFilterConnectionField(
        PropertyType, filterset_class=PropertyFilter)
    meta = graphene.Field(MetaType)

    def resolve_property(self, info, city_slug, area_slug, property_slug):
        try:
            return Property.objects.filter(
                slug=property_slug,
                area__slug=area_slug,
                area__city__slug=city_slug)[0]
        except IndexError:
            raise GraphQLError('No property found matching given input.')

    def resolve_meta(self, info):
        return MetaType()
