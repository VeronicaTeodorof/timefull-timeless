from django.db import models


# Create your models here.
class BusinessSettings(models.Model):
    """
    Singleton model holding rarely changed, owner-editable
    business constants (now just insurance rate), so the business
    owner can adjust the values without developer involvement.
    """
    insurance_rate = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        default=0.015
    )

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
