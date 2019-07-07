from django.db.models import Q, CheckConstraint
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
import geocoder
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django_extensions.db.fields import AutoSlugField
from aperol.properties.data import BingMapsRoutes
import os
import math

key = os.environ.get(
    "BING_MAPS_KEY", "AhQUdnsAv1EPYZ62GZJ_7yoyb3SQnHEHUrq9MeuDZWHhOqwN7ahF5C4awvfZxu8Q"
)
routes = BingMapsRoutes(key)


def get_apartment_variant():
    v, c = PropertyVariant.objects.get_or_create(name="apartment")
    return v.pk


class City(models.Model):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from=["name"], unique=True)

    def __str__(self):
        return self.name


class CityArea(models.Model):
    name = models.CharField(max_length=50)
    city = models.ForeignKey("City", on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from=["name"], unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{}, {}".format(self.name, self.city.name)


class LettingAgency(models.Model):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from=["name"], unique=True)

    # TODO: Fee information

    def __str__(self):
        return self.name


class Landlord(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name if self.name is not None else "#" + str(self.pk)


class Property(models.Model):
    # TODO: Trim number and make case insensitive for uniqueness
    # TODO: Are number, street, and postcode unique? No, not necessarily but
    #       the post office must rely on it being
    name = models.CharField(
        max_length=50, help_text="Property number or name", null=True, blank=True
    )
    street = models.CharField(max_length=50)
    area = models.ForeignKey("CityArea", on_delete=models.CASCADE)
    postcode = models.CharField(max_length=10)
    location = models.PointField(blank=True, null=True)
    slug = AutoSlugField(populate_from=["street", "pk"], unique=True)
    listing_url = models.URLField(null=True, blank=True)
    variant = models.ForeignKey(
        "PropertyVariant", on_delete=models.CASCADE, default=get_apartment_variant
    )

    price = models.PositiveIntegerField(
        verbose_name="Minimum price per month per person"
    )
    total_price = models.PositiveIntegerField(
        verbose_name="Total price per month for all tenants"
    )
    deposit = models.PositiveIntegerField(null=True)
    agency = models.ForeignKey(
        "LettingAgency", on_delete=models.CASCADE, null=True, blank=True
    )
    landlord = models.ForeignKey(
        "Landlord", on_delete=models.CASCADE, null=True, blank=True
    )

    lease_length_months = models.PositiveIntegerField(null=True, blank=True)
    lease_start_date = models.DateField(null=True, blank=True)

    # Features
    bedrooms = models.PositiveIntegerField()
    double_bedrooms = models.PositiveIntegerField(null=True, blank=True)
    single_bedrooms = models.PositiveIntegerField(null=True, blank=True)
    total_area = models.PositiveIntegerField(
        verbose_name="Total area in square metres", null=True, blank=True
    )
    bathrooms = models.PositiveIntegerField(null=True, blank=True)
    ensuites = models.PositiveIntegerField(null=True, blank=True)

    # True values must indicate having something
    furnished = models.NullBooleanField()
    dishwasher = models.NullBooleanField()
    bath = models.NullBooleanField()
    shower = models.NullBooleanField()
    garden = models.NullBooleanField()
    dryer = models.NullBooleanField()
    washing_machine = models.NullBooleanField()
    microwave = models.NullBooleanField()
    fridge = models.NullBooleanField()
    freezer = models.NullBooleanField()
    stove = models.NullBooleanField()
    oven = models.NullBooleanField()
    air_conditioning = models.NullBooleanField()
    kitchen_table = models.NullBooleanField()
    desks_in_rooms = models.NullBooleanField()
    double_glazing = models.NullBooleanField()
    bike_storage = models.NullBooleanField()
    parking_space = models.NullBooleanField()
    fire_alarm = models.NullBooleanField()
    burglar_alarm = models.NullBooleanField()

    def __str__(self):
        return "{} {}, {}, {}".format(
            self.name, self.street, self.area, self.area.city, self.postcode
        )

    def clean(self):
        g = geocoder.osm(self.postcode, max_rows=1)

        if g.error:
            raise ValidationError(
                (
                    "Couldn't geocode postcode <{}>.\n Are you sure that it is "
                    + "valid (try Open Street Maps)? {}"
                ).format(self.postcode, g.error)
            )

        lat, lng = g.latlng
        self.location = Point(lng, lat)


class PropertyPhoto(models.Model):
    uploaded_photo = models.ImageField(null=True)
    photo_url = models.URLField(blank=True, null=True)
    agency_photo = models.BooleanField()
    property = models.ForeignKey("Property", on_delete=models.CASCADE)

    # class Meta:
    #     constraints = [
    #         CheckConstraint(
    #             check=Q(uploaded_photo__isnull=False) | Q(photo_url__isnull=False),
    #             name="at_least_one_photo_source",
    #         )
    #     ]

    def __str__(self):
        return "{}, {} - {}".format(
            self.property.street,
            self.property.postcode,
            "Agency Photo" if self.agency_photo else "Tenant Photo",
        )


class PropertyVariant(models.Model):
    name = models.CharField(max_length=50, help_text="The variant name", unique=True)

    def __str__(self):
        return self.name


class Landmark(models.Model):
    name = models.CharField(max_length=70)
    location = models.PointField()

    def __str__(self):
        return "{}".format(self.name)


class PropertyLandmarkDistance(models.Model):
    property = models.ForeignKey("Property", on_delete=models.CASCADE)
    landmark = models.ForeignKey("Landmark", on_delete=models.CASCADE)
    distance = models.FloatField(
        help_text="Distance in kilometers between the property and landmark", blank=True
    )
    cycling_time = models.IntegerField(
        help_text="Cycling time between property and landmark in minutes", blank=True
    )
    walking_time = models.IntegerField(
        help_text="Walking time between property and landmark in minutes", blank=True
    )

    class Meta:
        unique_together = (("property", "landmark"),)

    def __str__(self):
        return "{} - {}".format(self.property, self.landmark)

    def save(self, *args, **kwargs):
        start_lng, start_lat = (self.property.location.x, self.property.location.y)
        end_lng, end_lat = (self.landmark.location.x, self.landmark.location.y)

        result = routes.calculate_distance((start_lat, start_lng), (end_lat, end_lng))

        distance = result.get("travelDistance", -1)

        if distance < 0:
            raise Exception("Distance could not be calculated.")

        CYCLING_SPEED = 15.5  # in KM/h
        cycling_time = distance / CYCLING_SPEED * 60

        WALKING_SPEED = 5.0  # in KM/h
        walking_time = distance / WALKING_SPEED * 60

        self.distance = distance
        self.cycling_time = math.ceil(cycling_time)
        self.walking_time = math.ceil(walking_time)

        super().save(*args, **kwargs)
