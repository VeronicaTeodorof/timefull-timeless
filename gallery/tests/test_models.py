from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.db import models
from gallery.models import Theme, Sculpture
from datetime import date
from cloudinary.models import CloudinaryField


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

    def test_theme_slug_auto_generates_from_name(self):
        """
        Tests that slug is automatically generated from name
        when not explicitly provided.
        """
        theme = Theme.objects.create(name='Any Theme')
        self.assertEqual(theme.slug, 'any-theme')

    def test_theme_name_must_be_unique_case_insensitive(self):
        """
        Tests that creating a theme with a name matching an existing one,
        different only in case, raises Integrity Error
        """

        Theme.objects.create(name='Any Theme')
        with self.assertRaises(IntegrityError):
            Theme.objects.create(name='any theme')

    def test_theme_name_strips_whitespace(self):
        """
        Tests that whitespace leading/trailling whitespace is
        stirpped from name when saved
        """
        theme = Theme.objects.create(name=' Any Name ')
        self.assertEqual(theme.name, 'Any Name')

    def test_theme_representative_sculpture_set_null_on_delete(self):
        """
        Tests that deleting a Sculpture sets representative_sculpture
        to None on any Theme referencing it, rather than deleting
        the Theme or raising an error.
        """
        sculpture = Sculpture.objects.create(
            title='Deletable Sculpture',
            year=2024,
            price=100.00,
            image='image/upload/v1234/deletable.jpg',
            material='Bronze',
        )
        theme = Theme.objects.create(
            name='Test Theme',
            representative_sculpture=sculpture,
        )

        sculpture.delete()
        theme.refresh_from_db()

        self.assertIsNone(theme.representative_sculpture)


class SculptureModelCase(TestCase):
    """
    Tests for the Sculpture model
    """
    def setUp(self):
        """
        Creates a temporary Sculpture object for tests
        """
        self.sculpture = Sculpture.objects.create(
            title='Test Sculpture',
            year=2024,
            price=100.00,
            image='image/upload/v1234/test_sculpture.jpg',
            material='Bronze',
        )

    def test_sculpture_has_title_field(self):
        """
        Tests that title is a CharField on Sculpture model
        """
        field = Sculpture._meta.get_field('title')
        self.assertIsInstance(field, models.CharField)

    def test_sculpture_title_cannot_be_null(self):
        """
        Tests that creating a Sculpture with title=None raises
        IntegrityError, since title is not nullable.
        """
        with self.assertRaises(IntegrityError):
            Sculpture.objects.create(title=None)

    def test_sculpture_has_title_translation_field(self):
        """
        Tests that title_translation is a CharField on Sculpture model
        """
        field = Sculpture._meta.get_field('title_translation')
        self.assertIsInstance(field, models.CharField)

    def test_sculpture_title_must_be_unique_case_insensitive(self):
        """
        Tests that creating a sculpture with a title matching an existing one,
        differing only in case, raises an Integrity Error

        """
        with self.assertRaises(IntegrityError):
            Sculpture.objects.create(
                title=self.sculpture.title.upper(),
                year=2024,
                price=100.00,
                image='image/upload/v1234/other.jpg',
                material='Bronze',
            )

    def test_sculpture_title_translation_can_be_null(self):
        """
        Tests that a Sculpture can be created with
        title_translation=None, since null=True.
        """
        try:
            Sculpture.objects.create(
                title='Another Sculpture',
                year=2024,
                price=100.00,
                image='image/upload/v1234/test_sculpture2.jpg',
                material='Bronze',
                title_translation=None,
            )
        except IntegrityError:
            self.fail("translation_title should allow null=True")

    def test_sculpture_has_slug_field(self):
        """
        Tests that slug is a SlugField on Sculpture model
        """
        field = Sculpture._meta.get_field('slug')
        self.assertIsInstance(field, models.SlugField)

    def test_sculpture_slug_auto_generates_from_name(self):
        """
        Tests that slug is automatically generated from name
        when not explicitly provided.
        """
        self.assertEqual(self.sculpture.slug, 'test-sculpture')

    def test_sculpture_slug_must_be_unique(self):
        """
        Tests that creating two sculptures with the same slug raises
        Integrity Error
        """
        with self.assertRaises(IntegrityError):
            Sculpture.objects.create(
                title='Different Title',
                year=2024,
                price=100.00,
                image='image/upload/v1234/other.jpg',
                material='Bronze',
                slug=self.sculpture.slug,
            )

    def test_sculpture_has_dimensions_field(self):
        """
        Tests that slug is a CharField on Sculpture model
        """
        field = Sculpture._meta.get_field('dimensions')
        self.assertIsInstance(field, models.CharField)

    def test_sculpture_dimensions_can_be_null(self):
        """
        Tests that a Sculpture can be created with
        dimensions=None, since null=True.
        """
        try:
            Sculpture.objects.create(
                title='Another Sculpture',
                year=2024,
                price=100.00,
                image='image/upload/v1234/test_sculpture2.jpg',
                material='Bronze',
                dimensions=None,
            )
        except IntegrityError:
            self.fail("dimensions should allow null=True")

    def test_sculpture_has_material_field(self):
        """
        Tests that material is a CharField on Sculpture model
        """
        field = Sculpture._meta.get_field('material')
        self.assertIsInstance(field, models.CharField)

    def test_sculpture_material_cannot_be_null(self):
        """
        Tests that creating a Sculpture with material=None raises
        IntegrityError, since material is not nullable.
        """
        with self.assertRaises(IntegrityError):
            Sculpture.objects.create(
                title='Materialless Sculpture',
                year=2024,
                price=100.00,
                image='image/upload/v1234/other.jpg',
                material=None,
            )

    def test_sculpture_material_strips_whitespace(self):
        """
        Tests that leading/trailling whitespace is
        stirpped from material when saved
        """
        sculpture = Sculpture.objects.create(
            title='Whitespace Material Test',
            year=2024,
            price=100.00,
            image='image/upload/v1234/other.jpg',
            material='  Bronze  ',
            )
        self.assertEqual(sculpture.material, 'Bronze')

    def test_sculpture_material_normalizes_to_title_case(self):
        """Tests that material is normalized to title case when saved"""

        sculpture = Sculpture.objects.create(
            title='Normalized Material Test',
            year=2024,
            price=100.00,
            image='image/upload/v1234/other.jpg',
            material='bronze wire',
            )
        self.assertEqual(sculpture.material, 'Bronze Wire')

    def test_sculpture_has_price_field(self):
        """
        Tests that price is a DecimalField on Sculpture model
        """
        field = Sculpture._meta.get_field('price')
        self.assertIsInstance(field, models.DecimalField)

    def test_sculpture_price_cannot_be_negative(self):
        """
        Tests that a negative value for price fails validation
        """
        sculpture = Sculpture(
            title='Underpriced Sculpture',
            year=2024,
            price=-10.00,
            image='image/upload/v1234/other.jpg',
            material='Bronze',
        )
        with self.assertRaises(ValidationError):
            sculpture.full_clean()

    def test_sculpture_price_cannot_be_null(self):
        """
        Tests that creating a sculpture with a price=None raises
        Integrity Error
        """
        with self.assertRaises(IntegrityError):
            Sculpture.objects.create(
                title='Priceless Sculpture',
                year=2024,
                price=None,
                image='image/upload/v1234/other.jpg',
                material='Bronze',
            )

    def test_sculpture_has_weight_field(self):
        """
        Tests that weight is a DecimalField on Sculpture model
        """
        field = Sculpture._meta.get_field('weight')
        self.assertIsInstance(field, models.DecimalField)

    def test_sculpture_weight_can_be_null(self):
        """
        Tests that a Sculpture can be created with
        weight=None, since null=True.
        """
        try:
            Sculpture.objects.create(
                title='Weightless Sculpture',
                year=2024,
                price=100.00,
                image='image/upload/v1234/other.jpg',
                material='Bronze',
                weight=None,
            )
        except IntegrityError:
            self.fail("weight should allow null=True")

    def test_sculpture_weight_rejects_below_minimum(self):
        """
        Tests that a Sculpture's weight fails validation
        when below minimum.
        """
        sculpture = Sculpture(
            title='Light Sculpture',
            year=2024,
            price=100.00,
            image='image/upload/v1234/other.jpg',
            material='Bronze',
            weight=0.05,
        )
        with self.assertRaises(ValidationError):
            sculpture.full_clean()

    def test_sculpture_has_year_field(self):
        """
        Tests that year is a PositiveIntegerField on Sculpture model
        """
        field = Sculpture._meta.get_field('year')
        self.assertIsInstance(field, models.PositiveIntegerField)

    def test_sculpture_year_rejects_below_minimum(self):
        """
        Tests that a Sculpture's year fails validation
        when below minimum.
        """
        sculpture = Sculpture(
            title='Earliest Sculpture',
            year=1989,
            price=100.00,
            image='image/upload/v1234/other.jpg',
            material='Bronze',
        )
        with self.assertRaises(ValidationError):
            sculpture.full_clean()

    def test_sculpture_year_rejects_above_maximum(self):
        """
        Tests that a Sculpture's year fails validation
        when above maximum.
        """
        sculpture = Sculpture(
            title='Future Sculpture',
            year=date.today().year + 1,
            price=100.00,
            image='image/upload/v1234/other.jpg',
            material='Bronze',
        )
        with self.assertRaises(ValidationError):
            sculpture.full_clean()

    def test_sculpture_year_cannot_be_null(self):
        """
        Tests that creating a Sculpture with year=None raises
        IntegrityError, since year is not nullable.
        """
        with self.assertRaises(IntegrityError):
            Sculpture.objects.create(
                title='Placeholder Title',
                year=None,
                price=100.00,
                image='image/upload/v1234/other.jpg',
                material='Bronze',
            )

    def test_sculpture_has_image_field(self):
        """
        Tests that image is a CloudinaryField on Sculpture model
        """
        field = Sculpture._meta.get_field('image')
        self.assertIsInstance(field, CloudinaryField)

    def test_sculpture_image_cannot_be_blank(self):
        """
        Tests that a Sculpture without an image fails validation,
        since blank=False on the image field (validated via
        full_clean(), not a database constraint).
        """
        sculpture = Sculpture(
            title='Imageless Sculpture',
            year=2024,
            price=100.00,
            material='Bronze',
            image=None,
        )
        with self.assertRaises(ValidationError):
            sculpture.full_clean()

    def test_sculpture_can_save_without_image_at_database_level(self):
        """
        Tests that Sculpture.objects.create() succeeds with image=None,
        since CloudinaryField does not enforce null at the database
        level — only full_clean()'s blank check catches a missing image.
        """
        sculpture = Sculpture.objects.create(
            title='Database Level Imageless Sculpture',
            year=2024,
            price=100.00,
            material='Bronze',
            image=None,
        )
        sculpture.refresh_from_db()
        self.assertIsNone(sculpture.image.public_id)

    def test_sculpture_has_status_field(self):
        """
        Tests that status is a CharField on Sculpture model
        """
        field = Sculpture._meta.get_field('status')
        self.assertIsInstance(field, models.CharField)

    def test_sculpture_status_has_correct_choices(self):
        """
        Tests that status field has the expected choices:
        available, reserved, sold.
        """
        field = Sculpture._meta.get_field('status')
        self.assertIn(('available', 'Available'), field.choices)
        self.assertIn(('reserved', 'Reserved'), field.choices)
        self.assertIn(('sold', 'Sold'), field.choices)

    def test_sculpture_status_defaults_to_available(self):
        """
        Tests that status defaults to available when not specified
        """
        sculpture = Sculpture.objects.create(
            title='Default Status Sculpture',
            year=2024,
            price=100.00,
            image='image/upload/v1234/other.jpg',
            material='Bronze',
        )
        self.assertEqual(sculpture.status, 'available')

    def test_sculpture_has_reserved_at_field(self):
        """
        Tests that reserved_at is a DateTimeField on Sculpture model
        """
        field = Sculpture._meta.get_field('reserved_at')
        self.assertIsInstance(field, models.DateTimeField)

    def test_sculpture_reserved_at_can_be_null(self):
        """
        Tests that a Sculpture can be created with
        reserved_at=None, since null=True.
        """
        try:
            Sculpture.objects.create(
                title='Not Reserved',
                year=2024,
                price=100.00,
                image='image/upload/v1234/other.jpg',
                material='Bronze',
                reserved_at=None,
            )
        except IntegrityError:
            self.fail("reserved_at should allow null=True")

    def test_sculpture_has_is_manually_reserved_field(self):
        """
        Tests that is_manually_reserved is a BooleanField on Sculpture model
        """
        field = Sculpture._meta.get_field('is_manually_reserved')
        self.assertIsInstance(field, models.BooleanField)

    def test_sculpture_is_manually_reserved_defaults_to_false(self):
        """
        Tests that is_manually_reserved defaults to False.
        """
        sculpture = Sculpture.objects.create(
            title='Default Reservation Sculpture',
            year=2024,
            price=100.00,
            image='image/upload/v1234/other.jpg',
            material='Bronze',
        )
        self.assertFalse(sculpture.is_manually_reserved)

    def test_sculpture_has_is_visible_field(self):
        """
        Tests that is_visible is a BooleanField on Sculpture model
        """
        field = Sculpture._meta.get_field('is_visible')
        self.assertIsInstance(field, models.BooleanField)

    def test_sculpture_is_visible_defaults_to_true(self):
        """
        Tests that is_visible defaults to True.
        """
        sculpture = Sculpture.objects.create(
            title='Default Visible Sculpture',
            year=2024,
            price=100.00,
            image='image/upload/v1234/other.jpg',
            material='Bronze',
        )
        self.assertTrue(sculpture.is_visible)

    def test_sculpture_has_insurance_rate_override_field(self):
        """
        Tests that insurance_rate_override is a DecimalField on Sculpture model
        """
        field = Sculpture._meta.get_field('insurance_rate_override')
        self.assertIsInstance(field, models.DecimalField)

    def test_sculpture_insurance_rate_override_can_be_null(self):
        """
        Tests that a Sculpture can be created with
        insurance_rate_override=None, since null=True.
        """
        try:
            Sculpture.objects.create(
                title='Placeholder Title',
                year=2024,
                price=100.00,
                image='image/upload/v1234/other.jpg',
                material='Bronze',
                insurance_rate_override=None,
            )
        except IntegrityError:
            self.fail("insurance_rate_override should allow null=True")

    def test_sculpture_insurance_rate_override_rejects_below_minimum(self):
        """
        Tests that a Sculpture's insurance_rate_override fails validation
        when below minimum.
        """
        sculpture = Sculpture(
            title='Under Insured',
            year=2024,
            price=100.00,
            image='image/upload/v1234/other.jpg',
            material='Bronze',
            insurance_rate_override=-0.1
        )
        with self.assertRaises(ValidationError):
            sculpture.full_clean()

    def test_sculpture_insurance_rate_override_rejects_above_maximum(self):
        """
        Tests that a Sculpture's insurance_rate_override fails validation
        when above maximum.
        """
        sculpture = Sculpture(
            title='Over Insured',
            year=2024,
            price=100.00,
            image='image/upload/v1234/other.jpg',
            material='Bronze',
            insurance_rate_override=50.01
        )
        with self.assertRaises(ValidationError):
            sculpture.full_clean()

    def test_sculpture_has_themes_field(self):
        """
        Tests that themes is a ManyToManyField on Sculpture model,
        related to Theme.
        """
        field = Sculpture._meta.get_field('themes')
        self.assertIsInstance(field, models.ManyToManyField)
        self.assertEqual(field.related_model, Theme)
