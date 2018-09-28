from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
import geocoder
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django_extensions.db.fields import AutoSlugField


class City(models.Model):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from=['name'], unique=True)

    def __str__(self):
        return self.name


class CityArea(models.Model):
    name = models.CharField(max_length=50)
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from=['name'], unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{}, {}".format(self.name, self.city.name)


class LettingAgency(models.Model):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from=['name'], unique=True)

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
    name = models.CharField(max_length=50, help_text="Property number or name")
    street = models.CharField(max_length=50)
    area = models.ForeignKey('CityArea', on_delete=models.CASCADE)
    postcode = models.CharField(max_length=10)
    location = models.PointField(blank=True)
    slug = AutoSlugField(populate_from=['street', 'pk'], unique=True)
    variant = models.ForeignKey(
        'PropertyVariant', on_delete=models.CASCADE, null=True, blank=True)

    price = models.IntegerField(
        verbose_name="Minimum price per month per person")
    total_price = models.IntegerField(
        verbose_name="Total price per month for all tenants")
    deposit = models.IntegerField(null=True)
    agency = models.ForeignKey(
        'LettingAgency', on_delete=models.CASCADE, null=True, blank=True)
    landlord = models.ForeignKey(
        'Landlord', on_delete=models.CASCADE, null=True, blank=True)

    lease_length = models.DurationField(null=True, blank=True)

    # Features
    bedrooms = models.IntegerField()
    double_bedrooms = models.IntegerField()
    single_bedrooms = models.IntegerField()
    total_area = models.IntegerField(
        verbose_name="Total area in square metres", null=True, blank=True)
    bathrooms = models.IntegerField()
    ensuites = models.IntegerField()

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
        return "{} {}, {}, {}".format(self.name, self.street, self.area,
                                      self.area.city, self.postcode)

    def clean(self):
        g = geocoder.osm(self.postcode, max_rows=1)

        if g.error:
            raise ValidationError(
                ("Couldn't geocode postcode <{}>.\n Are you sure that it is " +
                 "valid (try Open Street Maps)? {}")
                .format(self.postcode, g.error))

        lat, lng = g.latlng
        self.location = Point(lng, lat)


class PropertyPhoto(models.Model):
    photo = models.ImageField()
    agency_photo = models.BooleanField()
    property = models.ForeignKey('Property', on_delete=models.CASCADE)

    def __str__(self):
        return "{}, {} - {}".format(self.property.street,
                                    self.property.postcode, 'Agency Photo' if
                                    self.agency_photo else 'Tenant Photo')


class PropertyVariant(models.Model):
    name = models.CharField(max_length=50, help_text="The variant name")
