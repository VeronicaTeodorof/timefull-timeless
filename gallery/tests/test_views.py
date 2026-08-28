# gallery app test_views.py
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from gallery.models import Theme, Sculpture


@override_settings(STORAGES={
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
})
class GalleryViewCase(TestCase):
    """Tests for gallery page view"""
    def setUp(self):
        """
        Creates temporary test user
        """
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )

    def test_anonymous_user_cannot_see_cta_button(self):
        """Tests whether an anonymous user can see the cta staff-only button"""
        response = self.client.get(reverse('gallery:gallery'))
        self.assertNotContains(response, 'Add sculpture')

    def test_authenticated_non_staff_user_cannot_see_cta(self):
        "Tests whether an authenticated non-staff user can see the cta button"
        self.client.force_login(self.user)
        response = self.client.get(reverse('gallery:gallery'))
        self.assertNotContains(response, 'Add sculpture')

# Decorator overrides production STORAGES setting for staticfiles,
# which requires an extra build step that doesn't run in tests.
# Provides a default setting for this test case only.
@override_settings(STORAGES={
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
})
class AddSculptureViewCase(TestCase):
    """Tests for add sculpture page view"""
    def setUp(self):
        """
        Creates temporary test user
        """
        self.url = reverse('gallery:add-sculpture')
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.staff_user = get_user_model().objects.create_user(
                    username='staffuser', password='testpass', is_staff=True
                )
        self.theme = Theme.objects.create(name='time')
        self.data = {
            "title": "Test Piece",
            "year": 2024,
            "price": 500,
            "material": "Bronze",
            "dimensions": "30x20x10cm",
            "status": "draft",
            "themes": [self.theme.pk],
        }

    def test_add_sculpture_url_resolves(self):
        self.assertEqual(self.url, '/gallery/add_sculpture/')

    def test_anonymous_user_gets_302_for_add_sculpture(self):
        """
        Tests anonymous user is redirected
        when trying to access add sculpture page
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_non_staff_user_gets_403_for_add_sculpture(self):
        """
        Tests non-staff authenticated users get 403
        when trying to access add sculpture page
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_staff_user_gets_200_for_add_sculpture(self):
        """
        Tests staff user can successfully access the add sculpture page
        """
        self.client.force_login(self.staff_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_add_sculpture_view_passes_form_in_context(self):
        """
        Tests form is passed in context so it can be used in templae
        """
        self.client.force_login(self.staff_user)
        response = self.client.get(self.url)
        self.assertIn('form', response.context)
