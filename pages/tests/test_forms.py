from django.contrib.auth import get_user_model
from django.test import TestCase

from ..forms import ContactForm

User = get_user_model()


class ContactFormTests(TestCase):
    """Tests for ContactForm validation rules."""

    # Test data builder pattern — learned from Claude AI
    def valid_data(self, **overrides):
        """
        Helper method - builds a valid set of data to be used by
        all tests in class, allows overrides,
        its purpose is to avoid reapeating same data
        with one variation per test
        """
        data = {
            "name": "Test Visitor",
            "email": "test@example.com",
            "phone": "+44 7123 456789",
            "subject": "General enquiry",
            "message": "Hello, I have a question about a piece.",
        }
        data.update(overrides)
        return data

    def test_missing_phone_is_valid(self):
        """
        Tests that phone with blank phone field submits successfully
        """
        data = self.valid_data()
        del data["phone"]
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())

    def test_missing_name_is_invalid(self):
        """
        Tests that form with blank name field is rejected and
        shows relevant error
        """
        form = ContactForm(data=self.valid_data(name=""))
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_missing_email_is_invalid(self):
        """
        Tests that form with blank email field is rejected and
        shows relevant error
        """
        form = ContactForm(data=self.valid_data(email=""))
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_malformed_email_is_invalid(self):
        """
        Tests that form with invalid format email is rejected and
        shows relevant error
        """
        form = ContactForm(data=self.valid_data(email="not-an-email"))
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_missing_subject_is_valid(self):
        """
        Tests that form with blank subject field submits successfully
        """
        data = self.valid_data()
        del data["subject"]
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())

    def test_missing_message_is_invalid(self):
        """
        Tests that form with blank message field is rejected and
        relevant error is shown
        """
        form = ContactForm(data=self.valid_data(message=""))
        self.assertFalse(form.is_valid())
        self.assertIn("message", form.errors)

    def test_all_fields_valid_submits_successfully(self):
        """
        Tests that a fully completed, valid form submits successfully
        """
        form = ContactForm(data=self.valid_data())
        self.assertTrue(form.is_valid())
