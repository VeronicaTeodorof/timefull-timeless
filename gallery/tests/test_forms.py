# gallery test_form
from django.test import TestCase
from gallery.forms import SculptureForm, ThemeForm
from gallery.models import Sculpture, Theme


class SculptureFormTest(TestCase):
    """
    Tests for Sculpture Form
    """
    def test_form_has_expected_fields(self):
        """
        Tests that all expected fields are on the form
        """
        form = SculptureForm()
        expected_fields = [
            'title', 'title_translation', 'dimensions', 'year',
            'material', 'price', 'themes', 'image', 'status', 'new_theme',
        ]
        self.assertEqual(expected_fields, list(form.fields.keys()))

    def test_form_has_custom_new_themes_field(self):
        """
        Tests that form has a distinct from model, custom new_themes field
        """
        form = SculptureForm()
        self.assertIn('new_theme', form.fields)


class ThemeFormTests(TestCase):
    """
    Tests for Theme Form
    """
    def setUp(self):
        """
        Creates temporary theme for tests in this class
        """
        self.theme = Theme.objects.create(name='Time')

    def test_edit_theme_form_filters_representative_sculpture_by_theme(self):
        """
        Tests that ThemeForm's representative_sculpture field only
        filters and displays sculptures actually belonging
        to the theme being edited, excluding sculptures from other themes.
        """
        own_sculpture = Sculpture.objects.create(
            title='Own Piece', year=2024, price=100,
            material='Bronze', image='image/upload/v1/own.jpg',
        )
        own_sculpture.themes.add(self.theme)

        other_theme = Theme.objects.create(name='Angels')
        other_sculpture = Sculpture.objects.create(
            title='Other Piece', year=2024, price=100,
            material='Bronze', image='image/upload/v1/other.jpg',
        )
        other_sculpture.themes.add(other_theme)

        form = ThemeForm(instance=self.theme)

        self.assertIn(own_sculpture,
                      form.fields['representative_sculpture'].queryset)
        self.assertNotIn(other_sculpture,
                         form.fields['representative_sculpture'].queryset)
