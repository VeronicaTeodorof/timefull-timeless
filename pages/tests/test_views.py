from django.test import TestCase
from django.urls import reverse


class ContactViewTests(TestCase):
    """Tests for the contact view."""

    def valid_data(self, **overrides):
        """
        Helper method - avoids writing data dictionary once per test
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

    def test_valid_post_redirects(self):
        """
        Tests that a valid POST redirects back to the contact page
        """
        response = self.client.post(
            reverse("pages:contact"), data=self.valid_data()
        )
        self.assertRedirects(response, reverse("pages:contact"))
