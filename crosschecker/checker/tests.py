from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Query


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.home_url = reverse("home")
        self.check_wiki_url = reverse("check_wiki")
        self.profile_url = reverse("profile")

    def test_home_view(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checker/index.html")

    def test_check_wiki_view_no_auth(self):
        response = self.client.post(
            self.check_wiki_url,
            {
                "wiki_url": "https://en.wikipedia.org/wiki/Tomato",
                "question": "Is tomato a fruit?",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_check_wiki_view_with_auth(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            self.check_wiki_url,
            {
                "wiki_url": "https://en.wikipedia.org/wiki/Tomato",
                "question": "Is tomato a fruit?",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("result_summary", response.json())
        self.assertIn("sources", response.json())

    def test_user_profile_view_no_auth(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_user_profile_view_with_auth(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checker/profile.html")
