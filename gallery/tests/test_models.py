from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import models
from gallery.models import Theme


class ThemeModelCase(TestCase):
    """
    Tests for the Theme model
    """

    def test_theme_has_name_field(self):
        """
        Tests that name is a CharField on Theme model
        """
        field = Theme._meta.get_field('name')
        self.assertIsInstance(field, models.CharField)

    def test_theme_has_slug_field(self):
        """
        Tests that slug is a SlugField on Theme model
        """
        field = Theme._meta.get_field('slug')
        self.assertIsInstance(field, models.SlugField)

    def test_theme_has_representative_sculpture_field(self):
        """
        Tests that representative_sculpture is a ForeignKey on Theme model
        """
        field = Theme._meta.get_field('representative_sculpture')
        self.assertIsInstance(field, models.ForeignKey)

    def test_theme_name_cannot_be_null(self):
        """
        Tests that creating a Theme with name=None raises
        IntegrityError, since name is not nullable.
        """
        with self.assertRaises(IntegrityError):
            Theme.objects.create(name=None)

    def test_theme_representative_sculpture_can_be_null(self):
        """
        Tests that a Theme can be created with
        representative_sculpture=None, since null=True.
        """
        try:
            Theme.objects.create(name='Any theme',
                                 representative_sculpture=None)
        except IntegrityError:
            self.fail("representative_sculpture should allow null=True")

    def test_theme_slug_must_be_unique(self):
        """
        Tests that creating two Themes with the same slug
        raises IntegrityError
        """
        Theme.objects.create(name='Any Theme')
        with self.assertRaises(IntegrityError):
            Theme.objects.create(name='Any Theme')
