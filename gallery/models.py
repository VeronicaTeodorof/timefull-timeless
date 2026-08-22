from django.db import models
from django.utils.text import slugify
from django.db.models.functions import Lower
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from cloudinary.models import CloudinaryField
from django.conf import settings

# Create your models here.


class Theme(models.Model):
    """
    Represents a category of sculptures,
    used to group related works for filtered gallery views.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    representative_sculpture = models.ForeignKey(
        'Sculpture',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='representing_themes'
    )

    class Meta:
        """
        Ensures that no duplicate theme names exist
        regardless of case
        """
        constraints = [
            models.UniqueConstraint(
                # Lower() is a database function that accepts a single text
                # field or expression and returns the lowercase representation.
                Lower('name'),
                name='unique_theme_name_case_insensitive'
            )
        ]

    def save(self, *args, **kwargs):
        """
        Overrides default model save
        and automatically strips leading/trailing
        name whitespace and gives it a slug on save
        """
        if self.name is not None:
            self.name = self.name.strip()
            if not self.slug:
                self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Sculpture(models.Model):
    """
    Represents an individual sculpture available in the
    gallery, including its details, pricing, and availability
    status for sale.
    """
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        RESERVED = 'reserved', 'Reserved'
        SOLD = 'sold', 'Sold'
    status = models.CharField(max_length=10,
                              choices=Status.choices,
                              default=Status.AVAILABLE)
    title = models.CharField(max_length=100)
    title_translation = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    dimensions = models.CharField(max_length=100, null=True, blank=True)
    material = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
        )
    weight = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.10)]
    )
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1990),
                    MaxValueValidator(date.today().year)]
    )
    image = CloudinaryField('image')
    reserved_at = models.DateTimeField(null=True, blank=True)
    is_manually_reserved = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    insurance_rate_override = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        null=True,
        blank=True,
        validators=[MinValueValidator(0),
                    MaxValueValidator(50)]
        )
    themes = models.ManyToManyField(Theme, related_name='sculptures')
    reserved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        )

    class Meta:
        """
        Ensures that no duplicate sculpture title exist
        regardless of case
        """
        constraints = [
            models.UniqueConstraint(
                Lower('title'),
                name='unique_sculpture_title_case_insensitive'
            )
        ]

    def save(self, *args, **kwargs):
        """
        Overrides default model save; strips leading/trailing
        whitespace from title, normalizes material to title case,
        and generates a slug from title if not already set
        """
        if self.title is not None:
            self.title = self.title.strip()
        if self.material is not None:
            self.material = self.material.strip().title()
        if not self.slug and self.title is not None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
