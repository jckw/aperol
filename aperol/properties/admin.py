from django.contrib import admin
from django.contrib.gis.db import models
from aperol.properties.models import (
    City,
    CityArea,
    LettingAgency,
    Landlord,
    Property,
    PropertyPhoto,
    PropertyLandmarkDistance,
    Landmark,
    PropertyVariant,
)
from mapwidgets.widgets import GooglePointFieldWidget


class PropertyPhotoInline(admin.TabularInline):
    model = PropertyPhoto


class LandmarkDistanceInline(admin.TabularInline):
    model = PropertyLandmarkDistance


class PropertyAdmin(admin.ModelAdmin):
    formfield_overrides = {models.PointField: {"widget": GooglePointFieldWidget}}
    inlines = [PropertyPhotoInline, LandmarkDistanceInline]


class LandmarkAdmin(admin.ModelAdmin):
    formfield_overrides = {models.PointField: {"widget": GooglePointFieldWidget}}


admin.site.register(City)
admin.site.register(CityArea)
admin.site.register(LettingAgency)
admin.site.register(Landlord)
admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyLandmarkDistance)
admin.site.register(Landmark, LandmarkAdmin)
admin.site.register(PropertyVariant)
