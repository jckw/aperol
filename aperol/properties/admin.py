from django.contrib import admin
from django.contrib.gis.db import models
from aperol.properties.models import (
    City,
    CityArea,
    LettingAgency,
    Landlord,
    Property,
    PropertyPhoto,
    PropertyReview,
    AgencyReview,
)
from mapwidgets.widgets import GooglePointFieldWidget


class PropertyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }


admin.site.register(City)
admin.site.register(CityArea)
admin.site.register(LettingAgency)
admin.site.register(Landlord)
admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyPhoto)
admin.site.register(PropertyReview)
admin.site.register(AgencyReview)
