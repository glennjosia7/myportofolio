from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import override_settings
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from main.models import Project


class Tutorial10Tests(APITestCase):
    password = "tutorial-test-password"
    payload = {
        "title": "Portfolio demo", "description": "Project description",
        "tech_stack": "Flutter, Django", "project_url": "https://example.com",
    }

    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.owner = user_model.objects.create_superuser("owner-test", password=cls.password)
        cls.member = user_model.objects.create_user("member-test", password=cls.password)
        cls.editor = user_model.objects.create_user("editor-test", password=cls.password)
        cls.editor.user_permissions.add(Permission.objects.get(codename="change_certification"))

    def setUp(self):
        self.login_url = reverse("api:api_token_auth")
        self.logout_url = reverse("api:api_logout")
        self.projects_url = reverse("api:project-list")

    def sign_in(self, user):
        response = self.client.post(self.login_url, {
            "username": user.username, "password": self.password,
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["token"])
        return response.data["token"]

    def test_public_get_and_invalid_credentials(self):
        self.assertEqual(self.client.get(self.projects_url).status_code, 200)
        invalid = self.client.post(self.login_url, {
            "username": self.owner.username, "password": "wrong-password",
        }, format="json")
        self.assertEqual(invalid.status_code, 400)
        self.assertNotIn("token", invalid.data)
        self.assertEqual(self.client.post(self.projects_url, self.payload).status_code, 403)

    def test_token_authenticated_get_and_post(self):
        auth = f"Token {self.sign_in(self.owner)}"
        self.assertEqual(self.client.get(self.projects_url, HTTP_AUTHORIZATION=auth).status_code, 200)
        response = self.client.post(self.projects_url, self.payload, format="json", HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())
        self.assertEqual(response.data["project_image_url"], "")

    def test_non_owner_tokens_cannot_create(self):
        for user in (self.member, self.editor):
            with self.subTest(user=user.username):
                response = self.client.post(self.projects_url, self.payload, format="json",
                                            HTTP_AUTHORIZATION=f"Token {self.sign_in(user)}")
                self.assertEqual(response.status_code, 403)
        self.assertFalse(Project.objects.exists())

    def test_logout_revokes_only_callers_token(self):
        auth = f"Token {self.sign_in(self.owner)}"
        member_key = self.sign_in(self.member)
        self.assertEqual(self.client.get(self.logout_url, HTTP_AUTHORIZATION=auth).status_code, 405)
        self.assertEqual(self.client.post(self.logout_url, HTTP_AUTHORIZATION=auth).status_code, 204)
        self.assertTrue(Token.objects.filter(user=self.member, key=member_key).exists())
        self.assertEqual(self.client.post(self.projects_url, self.payload, format="json",
                                          HTTP_AUTHORIZATION=auth).status_code, 401)
        self.assertEqual(self.client.post(self.logout_url, HTTP_AUTHORIZATION=auth).status_code, 401)

    def test_session_logout_endpoint_does_not_end_web_session(self):
        self.client.force_login(self.owner)
        self.assertEqual(self.client.post(self.logout_url).status_code, 204)
        self.assertIn("_auth_user_id", self.client.session)
        client = APIClient(enforce_csrf_checks=True)
        client.force_login(self.owner)
        self.assertEqual(client.post(self.projects_url, self.payload).status_code, 403)

    @override_settings(CORS_ALLOWED_ORIGIN_REGEXES=[r"^http://localhost:7357$"])
    def test_api_cors_preflight_and_untrusted_origin(self):
        origin = "http://localhost:7357"
        allowed = self.client.options(self.projects_url, HTTP_ORIGIN=origin,
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="POST",
            HTTP_ACCESS_CONTROL_REQUEST_HEADERS="authorization,content-type")
        self.assertEqual(allowed.headers.get("access-control-allow-origin"), origin)
        self.assertIn("authorization", allowed.headers["access-control-allow-headers"].lower())
        denied = self.client.get(self.projects_url, HTTP_ORIGIN="https://untrusted.example")
        self.assertNotIn("access-control-allow-origin", denied.headers)
