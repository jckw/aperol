from django.db.models.signals import post_save
from aperol.properties.models import Property, Landmark, PropertyLandmarkDistance
from django.dispatch import receiver


@receiver(post_save, sender=Property)
def calculate_distances_to_landmarks(sender, instance, **kwargs):
    for landmark in Landmark.objects.all():
        PropertyLandmarkDistance.objects.update_or_create(
            landmark=landmark, property=instance
        )


@receiver(post_save, sender=Landmark)
def calculate_distances_to_properties(sender, instance, **kwargs):
    for property in Property.objects.all():
        PropertyLandmarkDistance.objects.update_or_create(
            landmark=instance, property=property
        )
