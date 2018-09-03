from django.contrib import admin
from server.properties.models import (
    City,
    CityArea,
    LettingAgency,
    Landlord,
    Property,
    PropertyPhoto,
    PropertyReview,
    AgencyReview,
)


admin.site.register(City)
admin.site.register(CityArea)
admin.site.register(LettingAgency)
admin.site.register(Landlord)
admin.site.register(Property)
admin.site.register(PropertyPhoto)
admin.site.register(PropertyReview)
admin.site.register(AgencyReview)
