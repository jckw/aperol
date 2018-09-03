from django.contrib.gis.db import models
from django.contrib.auth import get_user_model


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CityArea(models.Model):
    name = models.CharField(max_length=50)
    city = models.ForeignKey('City', on_delete=models.CASCADE)

    def __str__(self):
        return "{}, {}".format(self.name, self.city.name)


class LettingAgency(models.Model):
    name = models.CharField(max_length=50)

    # TODO: Fee information

    def __str__(self):
        return self.name


class Landlord(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name if self.name is not None else "#" + str(self.pk)


def get_blank_landlord():
    return Landlord.objects.create()


class Property(models.Model):
    # TODO: Filter the number from API requests - backend only
    # TODO: Trim number and make case insensitive for uniqueness
    # TODO: Are number, street, and postcode unique? No, not necessarily but
    #       the post office must rely on it being
    name = models.CharField(max_length=50, help_text="Property number or name")
    street = models.CharField(max_length=50)
    area = models.ForeignKey('CityArea', on_delete=models.CASCADE)
    postcode = models.CharField(max_length=10)
    location = models.PointField()

    price = models.IntegerField(verbose_name="Total price per month")
    deposit = models.IntegerField(null=True)
    agency = models.ForeignKey('LettingAgency', on_delete=models.CASCADE)
    landlord = models.ForeignKey(
        'Landlord', default=get_blank_landlord,
        on_delete=models.CASCADE)

    # Features
    bedrooms = models.IntegerField()
    double_bedrooms = models.IntegerField()
    single_bedrooms = models.IntegerField()
    total_area = models.IntegerField(
        verbose_name="Total area in square metres", null=True)
    bathrooms = models.IntegerField()
    ensuites = models.IntegerField()

    # True values must be a positive thing
    furnished = models.BooleanField()
    dishwasher = models.BooleanField()
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


class PropertyPhoto(models.Model):
    photo = models.ImageField()
    agency_photo = models.BooleanField()
    property = models.ForeignKey('Property', on_delete=models.CASCADE)

    def __str__(self):
        return "{}, {} - {}".format(self.property.street,
                                    self.property.postcode, 'Agency Photo' if
                                    self.agency_photo else 'Tenant Photo')


class PropertyReview(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE)  # TODO: Sentinal user
    would_recommend = models.BooleanField()


class AgencyReview(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE)  # TODO:
    would_recommend = models.BooleanField()
