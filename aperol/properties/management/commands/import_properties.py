import json
from django.core.management.base import BaseCommand, CommandError
from aperol.properties.models import (
    Property,
    PropertyPhoto,
    PropertyVariant,
    LettingAgency,
    City,
    CityArea,
)


class Command(BaseCommand):
    help = "Imports properties from the RMA JSON file."

    def add_arguments(self, parser):
        parser.add_argument("input_files", nargs=1, type=str)

    def handle(self, *args, **options):
        for input_file in options["input_files"]:
            with open(input_file) as f:
                properties = json.load(f)

            for p in properties:
                agency = LettingAgency.objects.get_or_create(name=p["agency__name"])
                city = City.objects.get_or_create(name=p["city__name"])
                area = city.area_set.get_or_create(name=p["area__name"])
                variant = PropertyVariant.objects.get_or_create(name=p["variant__name"])
                # INCOMPLETE!
                prop = Property.objects.create(
                    street=p["street"],
                    postcode=p["postcode"],
                    area=area,
                    variant=variant,
                    total_price=p["price"],
                    bedrooms=p.bedrooms,
                    price=int(p["price"] / p["bedrooms"]),
                    listing_url=p["link"],
                    agency=agency,
                )

                for photo_url in p.photos:
                    photo = PropertyPhoto.objects.create(
                        photo_url=photo_url, property=prop, agency_photo=True
                    )

                self.stdout.write(
                    " ".join(["Added", p["street"], p["bedrooms"], p["variant"]])
                )

