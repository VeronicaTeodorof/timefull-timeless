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

    def test_add_sculpture_url_resolves(self):
        url = reverse('gallery:add-sculpture')
        self.assertEqual(url, '/gallery/add_sculpture/')

    def test_anonymous_user_gets_302_for_add_sculpture(self):
        """
        Tests anonymous user is redirected
        when trying to access add sculpture page
        """
        response = self.client.get(reverse('gallery:add-sculpture'))
        self.assertEqual(response.status_code, 302)

    def test_non_staff_user_gets_403_for_add_sculpture(self):
        """
        Tests non-staff authenticated users get 403
        when trying to access add sculpture page
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse('gallery:add-sculpture'))
        self.assertEqual(response.status_code, 403)

    def test_staff_user_gets_200_for_add_sculpture(self):
        """
        Tests staff user can successfully access the add sculpture page
        """
        staff_user = get_user_model().objects.create_user(
            username='staffuser', password='testpass', is_staff=True
        )
        self.client.force_login(staff_user)
        response = self.client.get(reverse('gallery:add-sculpture'))
        self.assertEqual(response.status_code, 200)
