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
                # TODO: Break this up into logical "get_city" "get_???" functions
                agency, _ = LettingAgency.objects.get_or_create(name=p["agency__name"])
                city, _ = City.objects.get_or_create(
                    name__iexact=p["city__name"], defaults={"name": p["city__name"]}
                )
                area, _ = CityArea.objects.get_or_create(
                    name__iexact=p["area__name"],
                    city__pk=city.pk,
                    defaults={"city": city, "name": p["area__name"]},
                )
                variant, _ = PropertyVariant.objects.get_or_create(
                    name__iexact=p["variant__name"],
                    defaults={"name": p["variant__name"]},
                )

                prop = Property.objects.create(
                    street=p["street"],
                    postcode=p["postcode"],
                    area=area,
                    variant=variant,
                    total_price=p["total_price"],
                    bedrooms=p["bedrooms"],
                    price=int(p["total_price"] / p["bedrooms"]),
                    listing_url=p["link"],
                    agency=agency,
                )

                # TODO: Try to filter out duplicates (at different sizes)
                for photo_url in p["photos"]:
                    photo = PropertyPhoto.objects.create(
                        photo_url=photo_url, property=prop, agency_photo=True
                    )

                self.stdout.write(
                    " ".join(
                        ["Added", p["street"], str(p["bedrooms"]), p["variant__name"]]
                    )
                )

