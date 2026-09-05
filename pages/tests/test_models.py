from decimal import Decimal
from django.test import TestCase
from pages.models import BusinessSettings


class BusinessSettingsModelTests(TestCase):

    def test_load_creates_row_with_default_rate_when_none_exists(self):
        """
        Tests that BusinessSettings.load() creates a new row with the
        default insurance rate when no row exists in the database yet.
        """
        self.assertEqual(BusinessSettings.objects.count(), 0)
        settings = BusinessSettings.load()
        self.assertEqual(BusinessSettings.objects.count(), 1)
        self.assertEqual(float(settings.insurance_rate), 0.015)

    def test_load_returns_existing_row_without_creating_a_second(self):
        """
        Tests that BusinessSettings.load() returns the existing row
        (including any edits already saved to it) rather than
        creating a duplicate.
        """
        first = BusinessSettings.load()
        first.insurance_rate = Decimal('0.0200')
        first.save()

        second = BusinessSettings.load()

        self.assertEqual(BusinessSettings.objects.count(), 1)
        self.assertEqual(second.insurance_rate, Decimal('0.0200'))

    def test_save_always_pins_pk_to_one(self):
        """
        Tests that save() pins the primary key to 1 regardless of how
        the instance was created — this is the mechanism that actually
        enforces the singleton behaviour.
        """
        settings = BusinessSettings(insurance_rate=Decimal('0.0180'))
        settings.save()
        self.assertEqual(settings.pk, 1)

    def test_delete_does_not_remove_the_row(self):
        """
        Tests that calling delete() on the singleton has no effect;
        the row remains, since deletion is intentionally disabled to
        protect the the single row.
        """
        settings = BusinessSettings.load()
        settings.delete()
        self.assertEqual(BusinessSettings.objects.count(), 1)
