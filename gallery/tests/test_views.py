# gallery app test_views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class GalleryViewTests(TestCase):
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
