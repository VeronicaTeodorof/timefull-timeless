from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


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


class Order(models.Model):
    """
    Stores data about a specific purchase.
    """
    order_number = models.CharField(max_length=32, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=2)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=True, blank=True)
    street_address1 = models.CharField(max_length=80, null=True, blank=True)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    region = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    shipping_method = models.CharField(
        max_length=10,
        choices=[('delivery', 'Delivery'), ('pickup', 'Studio Pickup')]
    )
    shipped_at = models.DateTimeField(null=True, blank=True)
    stripe_pid = models.CharField(max_length=254)

    # from Code Institute Boutique Ado
    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number
    # end of Boutique Ado copied code


class OrderLineItem(models.Model):
    """Stores data about each specific sculpture within a purchase."""
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='lineitems')
    sculpture = models.ForeignKey('gallery.Sculpture',
                                  on_delete=models.CASCADE)
    price_at_purchase = models.DecimalField(max_digits=6, decimal_places=2)
    insurance_cost = models.DecimalField(max_digits=5, decimal_places=2)
    delivery_cost = models.DecimalField(max_digits=5,
                                        decimal_places=2,
                                        default=0)
    lineitem_total = models.DecimalField(max_digits=7,
                                         decimal_places=2,
                                         editable=False)

    def __str__(self):
        return f"Order {self.order.order_number} - {self.sculpture.title}"
