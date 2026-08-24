# gallery test_form
from django.test import TestCase
from gallery.forms import SculptureForm


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
