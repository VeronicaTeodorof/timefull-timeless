from django.db import models


# Create your models here.
class DeliveryCost(models.Model):
    """
    A model that allows business owner to adjust delivery cost
    """
    class Country(models.TextChoices):
        RO = "RO", "Romania"
        UK = "UK", "United Kingdom"
    country = models.CharField(max_length=2,
                               choices=Country.choices,
                               default=Country.UK)
    cost = models.DecimalField(
        max_digits=5,
        decimal_places=2)
