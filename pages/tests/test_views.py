from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()

class ContactViewTests(TestCase):
    """Tests for the contact view."""
    def setUp(self):
        """
        Creates a temporary user for the tests in this class
        """
        self.user = User.objects.create_user(
            username="testvisitor",
            email="visitor@example.com",
            password="testpass123",
        )

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

    def test_invalid_post_returns_200_with_errors(self):
        """
        Tests that an invalid POST re-renders the form with errors,
        without redirecting
        """
        response = self.client.post(
            reverse("pages:contact"), data=self.valid_data(email="")
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"],
                             "email",
                             "This field is required.")

    def test_anonymous_get_email_field_is_empty(self):
        """
        Tests that an anonymous GET request has no prefilled email
        """
        response = self.client.get(reverse("pages:contact"))
        self.assertEqual(response.context["form"].initial.get("email"), None)

    def test_authenticated_get_prepopulated_email_field(self):
        """
        Tests that an authenticated GET request prefills the email
        field with the logged in user's email
        """
        self.client.login(username="testvisitor", password="testpass123")
        response = self.client.get(reverse("pages:contact"))
        self.assertEqual(
            response.context["form"].initial.get("email"),
            "visitor@example.com"
        )
