from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="member",
            password="SecurePass!245",
            email="member@example.com",
        )

    def test_registration_creates_account(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newmember",
                "email": "newmember@example.com",
                "password1": "SecurePass!245",
                "password2": "SecurePass!245",
            },
        )

        self.assertRedirects(response, reverse("login"))
        self.assertTrue(
            get_user_model().objects.filter(username="newmember").exists()
        )

    def test_registration_rejects_mismatched_passwords(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newmember",
                "email": "newmember@example.com",
                "password1": "SecurePass!245",
                "password2": "DifferentPass!245",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            get_user_model().objects.filter(username="newmember").exists()
        )

    def test_registration_rejects_existing_username(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "member",
                "email": "another@example.com",
                "password1": "SecurePass!245",
                "password2": "SecurePass!245",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            get_user_model().objects.filter(username="member").count(), 1
        )

    def test_login_and_logout(self):
        response = self.client.post(
            reverse("login"),
            {"username": "member", "password": "SecurePass!245"},
        )
        self.assertRedirects(response, reverse("profile"))

        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("login"))

    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('profile')}",
        )

    def test_profile_displays_user_data_and_does_not_allow_edits(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("profile"))

        self.assertContains(response, "member")
        self.assertContains(response, "member@example.com")

        response = self.client.post(
            reverse("profile"),
            {
                "username": "updated",
                "first_name": "Member",
                "last_name": "User",
                "email": "updated@example.com",
                "is_staff": "on",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "member")
        self.assertEqual(self.user.email, "member@example.com")
        self.assertFalse(self.user.is_staff)

    def test_regular_user_cannot_access_admin(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("admin:login"), response.url)
