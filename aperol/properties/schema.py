import graphene
from graphene import relay, NonNull
from graphql import GraphQLError
from graphene_django.types import DjangoObjectType

# Contains a converter for Point to Geometry Field
from graphql_geojson import converter
from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Max, Min
from aperol.properties.models import (
    Property as PropertyModel,
    LettingAgency as LettingAgencyModel,
    City as CityModel,
    CityArea as CityAreaModel,
    PropertyPhoto as PropertyPhotoModel,
    PropertyVariant as PropertyVariantModel,
    PropertyLandmarkDistance as PropertyLandmarkDistanceModel,
    Landmark as LandmarkModel,
)
from aperol.properties.filters import PropertyFilter
from aperol.graphql.common import NonNullConnection


class Landmark(DjangoObjectType):
    class Meta:
        model = LandmarkModel
        interfaces = (relay.Node,)


class LandmarkConnection(relay.Connection):
    class Meta:
        node = Landmark


class PropertyLandmarkDistance(DjangoObjectType):
    class Meta:
        model = PropertyLandmarkDistanceModel
        interfaces = (relay.Node,)


class PropertyLandmarkDistanceConnectionType(relay.Connection):
    class Meta:
        node = PropertyLandmarkDistance


class PropertyPhoto(DjangoObjectType):
    class Meta:
        model = PropertyPhotoModel
        interfaces = (relay.Node,)


class PropertyPhotoConnectionType(NonNullConnection):
    class Meta:
        node = PropertyPhoto


class PropertyVariant(DjangoObjectType):
    class Meta:
        model = PropertyVariantModel
        interfaces = (relay.Node,)


class Property(DjangoObjectType):
    class Meta:
        model = PropertyModel
        interfaces = (relay.Node,)
        exclude_fields = ("name",)
        connection_class = NonNullConnection

    node = relay.Node.Field()
    photos = relay.ConnectionField(PropertyPhotoConnectionType)
    url = graphene.String()
    landmark_distances = relay.ConnectionField(PropertyLandmarkDistanceConnectionType)

    def resolve_photos(self, info, **kwargs):
        return PropertyPhotoModel.objects.filter(property=self)

    def resolve_url(self, info):
        return "/properties/{}/{}/{}".format(
            self.area.city.slug, self.area.slug, self.slug
        )

    def resolve_landmark_distances(self, info, **kwargs):
        return PropertyLandmarkDistanceModel.objects.filter(property=self)


class PropertyConnectionType(NonNullConnection):
    class Meta:
        node = Property


class LettingAgency(DjangoObjectType):
    class Meta:
        model = LettingAgencyModel
        interfaces = (relay.Node,)


class City(DjangoObjectType):
    class Meta:
        model = CityModel
        interfaces = (relay.Node,)


class CityArea(DjangoObjectType):
    class Meta:
        model = CityAreaModel
        interfaces = (relay.Node,)


class Meta(graphene.ObjectType):
    max_price = graphene.Int()
    min_price = graphene.Int()
    max_bedrooms = graphene.Int()
    min_bedrooms = graphene.Int()
    landmarks = relay.ConnectionField(LandmarkConnection)

    def resolve_max_price(self, info):
        return PropertyModel.objects.all().aggregate(Max("price"))["price__max"]

    def resolve_min_price(self, info):
        return PropertyModel.objects.all().aggregate(Min("price"))["price__min"]

    def resolve_max_bedrooms(self, info):
        return PropertyModel.objects.all().aggregate(Max("bedrooms"))["bedrooms__max"]

    def resolve_min_bedrooms(self, info):
        return PropertyModel.objects.all().aggregate(Min("bedrooms"))["bedrooms__min"]

    def resolve_landmarks(self, info):
        return LandmarkModel.objects.all()


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    property = graphene.Field(
        Property,
        city_slug=graphene.String(required=True),
        area_slug=graphene.String(required=True),
        property_slug=graphene.String(required=True),
    )
    agency = relay.Node.Field(LettingAgency)
    # TODO: Set this to required=True when a fix is found.
    filtered_properties = DjangoFilterConnectionField(
        Property, filterset_class=PropertyFilter
    )
    meta = graphene.Field(Meta, required=True)

    def resolve_property(self, info, city_slug, area_slug, property_slug):
        try:
            return PropertyModel.objects.filter(
                slug=property_slug, area__slug=area_slug, area__city__slug=city_slug
            )[0]
        except IndexError:
            raise GraphQLError("No property found matching given input.")

    def resolve_meta(self, info):
        return Meta()
