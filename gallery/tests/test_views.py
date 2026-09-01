# gallery app test_views.py

# Imports
from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from gallery.models import Theme, Sculpture
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
import cloudinary

# Constants
# written as refactor with Claude AI
MINIMAL_GIF = (
    b'GIF89a\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00'
    b'\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
)


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

    def test_gallery_excludes_themes_with_no_sculptures(self):
        """
        Tests that gallery view exculdes themes with no sculptures
        """
        populated_theme = Theme.objects.create(name='Time')
        sculpture = Sculpture.objects.create(
            title='Piece', year=2024, price=100,
            material='Bronze', image='image/upload/v1/piece.jpg',
        )
        sculpture.themes.add(populated_theme)
        empty_theme = Theme.objects.create(name="Empty")
        response = self.client.get(reverse('gallery:gallery'))
        themes_shown = list(response.context['themes'])

        self.assertIn(populated_theme, themes_shown)
        self.assertNotIn(empty_theme, themes_shown)

    def test_gallery_shows_theme_once_even_with_multiple_sculptures(self):
        """
        Tests that a theme with multiple sculptures appears
        only once in the gallery.
        """
        theme = Theme.objects.create(name='Angels')
        sculpture1 = Sculpture.objects.create(
            title='A',
            year=2024,
            price=100,
            material='Bronze',
            image='image/upload/v1/a.jpg',
        )
        sculpture2 = Sculpture.objects.create(
            title='B',
            year=2024,
            price=100,
            material='Bronze',
            image='image/upload/v1/b.jpg',
        )
        sculpture1.themes.add(theme)
        sculpture2.themes.add(theme)

        response = self.client.get(reverse('gallery:gallery'))
        themes_shown = list(response.context['themes'])

        self.assertEqual(themes_shown.count(theme), 1)


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
            "status": "available",
            "themes": [self.theme.pk],
        }

    def get_mocked_upload_and_image(self):
        """
        Returns a valid CloudinaryResource (to use as a mock's return
        value) and a SimpleUploadedFile built from MINIMAL_GIF, for
        tests that need to simulate a successful image upload.
        """
        mock_result = cloudinary.CloudinaryResource(
            public_id='test_public_id_123',
            version='1234567890',
            format='jpg',
            resource_type='image',
            type='upload',
        )
        image = SimpleUploadedFile(
            name='test_image.gif',
            content=MINIMAL_GIF,
            content_type='image/gif'
        )
        # returning a tuple
        return mock_result, image

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

    # Passing version reached through trial and error, using
    # https://www.honeybadger.io/blog/django-integration-testing/
    # as a starting point, adapted with Claude AI once the article's
    # exact pattern (mocking upload, not upload_resource; returning a
    # dict, not a CloudinaryResource) didn't match this project's setup.

    @patch('cloudinary.uploader.upload_resource')
    def test_valid_data_creates_object(self, mock_upload):
        """
        Tests that a staff user's valid POST data creates a Sculpture object
        """
        mock_upload.return_value, image = self.get_mocked_upload_and_image()
        self.client.force_login(self.staff_user)
        data = {**self.data, "image": image}
        response = self.client.post(self.url, data)
        # assertion written by Claude Ai
        # logic: every assertion can contain an optional msg argument
        # this argument is helpful in debugging
        # in this test, the form's validation errors are printed in the
        # terminal if the form failed validation (re-rendered with context);
        # otherwise there's no context, since success means a redirect
        self.assertEqual(
            Sculpture.objects.count(), 1,
            response.context["form"].errors if response.context else
            "no context (redirect?)"
        )

    @patch('cloudinary.uploader.upload_resource')
    def test_successful_save_redirects_to_sculpture_detail(self, mock_upload):
        """
        Tests that saving a valid sculpture
        redirects to that sculpture's detail page
        """
        mock_upload.return_value, image = self.get_mocked_upload_and_image()
        self.client.force_login(self.staff_user)
        data = {**self.data, "image": image}
        response = self.client.post(self.url, data)
        sculpture = Sculpture.objects.get(title=self.data['title'])
        self.assertRedirects(
            response,
            reverse('gallery:sculpture-detail',
                    kwargs={'slug': sculpture.slug})
        )

    @patch('cloudinary.uploader.upload_resource')
    def test_new_theme_field_creates_theme_when_valid(self, mock_upload):
        """
        Tests that submitting a valid new_theme value
        creates a new Theme record
        """
        mock_upload.return_value, image = self.get_mocked_upload_and_image()
        self.client.force_login(self.staff_user)
        data = {**self.data, "image": image, "new_theme": "Angels"}
        response = self.client.post(self.url, data)
        self.assertTrue(
            Theme.objects.filter(name="Angels").exists(),
            response.context["form"].errors if response.context else
            "no context (redirect?)"
        )

    @patch('cloudinary.uploader.upload_resource')
    def test_new_theme_with_exact_duplicate_name_reuses_existing_theme(
            self, mock_upload):
        """
        Tests that a duplicate name in new theme field reuses the existing one,
        rather than creating a new theme or raising an error
        """
        existing_theme = Theme.objects.create(name='Angels')
        mock_upload.return_value, image = self.get_mocked_upload_and_image()
        self.client.force_login(self.staff_user)
        data = {**self.data, "image": image, "new_theme": "Angels"}
        response = self.client.post(self.url, data)
        sculpture = Sculpture.objects.get(title=self.data['title'])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Theme.objects.filter(name='Angels').count(), 1)
        self.assertIn(sculpture, existing_theme.sculptures.all())

    @patch('cloudinary.uploader.upload_resource')
    def test_existing_theme_different_case_reuses_existing_theme(self,
                                                                 mock_upload):
        """
        Tests that a duplicate name different case in new theme field reuses
        the existing one, rather than creating a new theme or raising an error
        """
        existing_theme = Theme.objects.create(name='Angels')
        mock_upload.return_value, image = self.get_mocked_upload_and_image()
        self.client.force_login(self.staff_user)
        data = {**self.data, "image": image, "new_theme": "ANGELS"}
        response = self.client.post(self.url, data)
        sculpture = Sculpture.objects.get(title=self.data['title'])
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Theme.objects.filter(name='ANGELS').exists())
        self.assertIn(sculpture, existing_theme.sculptures.all())

    @patch('cloudinary.uploader.upload_resource')
    def test_all_themes_selected_or_created_on_a_sculpture_correctly_attach(
            self, mock_upload):
        """
        Tests that all themes selected on a sculpture add or edit
        form correctly attach to the respective sculpture
        """
        theme1 = Theme.objects.create(name='Flight')
        theme2 = Theme.objects.create(name='Angels')
        mock_upload.return_value, image = self.get_mocked_upload_and_image()
        self.client.force_login(self.staff_user)
        data = {**self.data, "image": image, "themes": [theme1.pk, theme2.pk]}
        self.client.post(self.url, data)
        sculpture = Sculpture.objects.get(title=self.data['title'])
        self.assertEqual(sculpture.themes.count(), 2)
        self.assertIn(theme1, sculpture.themes.all())
        self.assertIn(theme2, sculpture.themes.all())

    @patch('cloudinary.uploader.upload_resource')
    def test_existing_themes_and_new_theme_combine_correctly(
            self, mock_upload):
        """
        Tests that all themes selected on a sculpture add or edit
        form correctly attach to the respective sculpture
        """
        theme1 = Theme.objects.create(name='Flight')
        theme2 = Theme.objects.create(name='Angels')
        mock_upload.return_value, image = self.get_mocked_upload_and_image()
        self.client.force_login(self.staff_user)
        data = {**self.data, "image": image,
                "themes": [theme1.pk, theme2.pk],
                "new_theme": "Seeds"}
        self.client.post(self.url, data)
        sculpture = Sculpture.objects.get(title=self.data['title'])
        self.assertEqual(sculpture.themes.count(), 3)
        self.assertIn(theme1, sculpture.themes.all())
        self.assertIn(theme2, sculpture.themes.all())
        self.assertTrue(sculpture.themes.filter(name="Seeds").exists())

    @patch('cloudinary.uploader.upload_resource')
    def test_submtting_theme_with_no_theme_and_no_new_theme_fails(
            self, mock_upload):
        """
        Tests that submitting with no existing themes selected on a sculpture
        and no new theme fails with validation error
        """
        mock_upload.return_value, image = self.get_mocked_upload_and_image()
        self.client.force_login(self.staff_user)
        data = {**self.data, "image": image,
                "themes": [],
                "new_theme": ""}
        response = self.client.post(self.url, data)
        self.assertEqual(
            Sculpture.objects.count(), 0,
            response.context["form"].errors if response.context else
            "no context (redirect?)")

    @patch('cloudinary.uploader.upload_resource')
    def test_multiple_new_theme_fields_all_create_and_attach_fields(
            self, mock_upload):
        """
        Tests that submitting multiple new_theme values
        (as cloned fields would produce)
        creates and attaches each one as own theme
        """
        mock_upload.return_value, image = self.get_mocked_upload_and_image()
        self.client.force_login(self.staff_user)
        data = {**self.data, "image": image, "new_theme": ["Angels", "Seeds"]}
        self.client.post(self.url, data)
        sculpture = Sculpture.objects.get(title=self.data['title'])
        self.assertEqual(sculpture.themes.count(), 3)
        self.assertTrue(sculpture.themes.filter(name='Angels').exists())
        self.assertTrue(sculpture.themes.filter(name='Seeds').exists())

    @patch('cloudinary.uploader.upload_resource')
    def test_new_theme_alone_submits_without_error(self, mock_upload):
        """
        Tests that submitting only a new theme value, with no existing
        themes selected, validates without error and submits successfully
        """
        mock_upload.return_value, image = self.get_mocked_upload_and_image()
        self.client.force_login(self.staff_user)
        data = {**self.data,
                "image": image,
                "themes": [],
                "new_theme": ["Angels"]}
        response = self.client.post(self.url, data)
        self.assertEqual(
            Sculpture.objects.count(), 1,
            response.context["form"].errors if response.context else
            "no context (redirect?)"
        )


class EditThemeViewClass(TestCase):
    """
    Tests for edit_theme view
    """
    def setUp(self):
        """
        Creates temporary theme, url, user and staff user for tests
        """
        self.theme = Theme.objects.create(name='Time')
        self.url = reverse('gallery:edit-theme',
                           kwargs={'slug': self.theme.slug})
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.staff_user = get_user_model().objects.create_user(
            username='staffuser', password='testpass', is_staff=True
        )

    def test_anonymous_user_redirected_from_edit_theme(self):
        """
        Tests that an anonymous user is redirected to login when
        trying to access edit-theme
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_non_staff_user_gets_403_for_edit_theme(self):
        """
        Tests that a non-staff authenticated user gets 403 for edit-theme.
        """
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_staff_user_gets_200_for_edit_theme(self):
        """
        Tests that a staff user can access edit-theme successfully.
        """
        self.client.force_login(self.staff_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_edit_theme_saves_new_name(self):
        """
        Tests that submitting a new name via edit-theme updates and
        saves the theme's name.
        """
        self.client.force_login(self.staff_user)
        self.client.post(self.url, {'name': 'Angels'})
        self.theme.refresh_from_db()
        self.assertEqual(self.theme.name, 'Angels')

    def test_edit_theme_saves_representative_sculpture(self):
        """
        Tests that submitting a representative_sculpture PK via
        edit-theme updates and saves the theme's representative
        sculpture.
        """
        sculpture = Sculpture.objects.create(
            title='Piece', year=2024, price=100,
            material='Bronze', image='image/upload/v1/piece.jpg',
        )
        sculpture.themes.add(self.theme)
        self.client.force_login(self.staff_user)
        self.client.post(self.url, {
            'name': self.theme.name,
            'representative_sculpture': sculpture.pk,
        })
        self.theme.refresh_from_db()
        self.assertEqual(self.theme.representative_sculpture, sculpture)

    def test_edit_theme_rejects_empty_name(self):
        """
        Tests that empty name field is rejected and edits are not saved
        """
        self.client.force_login(self.staff_user)
        response = self.client.post(self.url, {'name': ''})
        self.assertEqual(response.status_code, 400)
        self.theme.refresh_from_db()
        self.assertEqual(self.theme.name, 'Time')
