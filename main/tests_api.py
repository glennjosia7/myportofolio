import uuid
from datetime import date

from django.contrib.auth.models import Group, Permission, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Certification, Project


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(
            username="visitor", password="test-password",
        )
        self.project = Project.objects.create(
            title="Portfolio", description="My website", tech_stack="Django",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app", "tech_stack": "Python",
            "project_url": "https://example.com/", "project_image_url": "",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(
            self.client.get(self.detail_url).status_code, status.HTTP_200_OK,
        )

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(
            self.client.get(url).status_code, status.HTTP_404_NOT_FOUND,
        )

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(
                self.client.post(
                    self.list_url, self.payload, format="json",
                ).status_code,
                403,
            )
            self.assertEqual(
                self.client.patch(
                    self.detail_url, {"title": "Changed"}, format="json",
                ).status_code,
                403,
            )
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"project_url": "javascript:alert(1)"}, "project_url"),
        ]:
            response = self.client.post(
                self.list_url, {**self.payload, **changes}, format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(
            self.detail_url, {"title": "Changed"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(
            self.detail_url, {"title": "Incomplete"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(
            self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(
            self.client.get(self.star_url).status_code, status.HTTP_403_FORBIDDEN,
        )
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(
            self.detail_url, {"title": "Changed"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(
            self.client.delete(self.list_url).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )
        self.assertEqual(
            self.client.get(self.star_url).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CertificationAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(
            username="visitor", password="test-password",
        )
        self.editor = User.objects.create_user(
            username="editor", password="test-password",
        )
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        editor_group.permissions.add(
            Permission.objects.get(codename="change_certification")
        )
        self.editor.groups.add(editor_group)
        self.certification = Certification.objects.create(
            name="Web Security Fundamentals",
            issuing_organization="Security Academy",
            issue_date=date(2026, 9, 1),
            credential_id="SEC-2026-001",
            credential_url="https://example.com/verify/SEC-2026-001",
        )
        self.list_url = reverse("api:certification-list")
        self.detail_url = reverse(
            "api:certification-detail", args=[self.certification.id],
        )
        self.star_url = reverse(
            "api:certification-star", args=[self.certification.id],
        )
        self.payload = {
            "name": "Cloud Practitioner",
            "issuing_organization": "Amazon",
            "issue_date": "2026-08-01",
            "credential_id": "AWS-001",
            "credential_url": "https://example.com/verify/AWS-001",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], self.certification.id)
        self.assertEqual(response.data[0]["name"], self.certification.name)
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(
            self.client.get(self.detail_url).status_code, status.HTTP_200_OK,
        )

    def test_regular_user_can_read(self):
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(
            self.client.get(self.list_url).status_code, status.HTTP_200_OK,
        )

    def test_search_by_name_and_organization(self):
        Certification.objects.create(
            name="Cloud Practitioner",
            issuing_organization="Amazon",
            issue_date=date(2026, 7, 1),
            credential_id="AWS-002",
            credential_url="https://example.com/verify/AWS-002",
        )
        by_name = self.client.get(self.list_url, {"name": "cloud"})
        self.assertEqual([item["name"] for item in by_name.data], ["Cloud Practitioner"])
        by_org = self.client.get(self.list_url, {"name": "amazon"})
        self.assertEqual([item["name"] for item in by_org.data], ["Cloud Practitioner"])
        by_existing_org = self.client.get(
            self.list_url, {"name": "security academy"},
        )
        self.assertEqual(
            [item["name"] for item in by_existing_org.data],
            ["Web Security Fundamentals"],
        )
        self.assertEqual(
            self.client.get(self.list_url, {"name": "missing"}).data, [],
        )

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Certification.objects.filter(pk=response.data["id"]).exists(),
        )

    def test_owner_can_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(
            Certification.objects.filter(pk=self.certification.id).exists(),
        )

    def test_editor_can_patch(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(
            self.detail_url, {"name": "Editor Updated"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.certification.refresh_from_db()
        self.assertEqual(self.certification.name, "Editor Updated")

    def test_editor_can_put_full_update(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.certification.refresh_from_db()
        self.assertEqual(self.certification.name, "Cloud Practitioner")
        self.assertEqual(self.certification.issuing_organization, "Amazon")

    def test_editor_invalid_patch_does_not_change_database(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(
            self.detail_url, {"name": "   "}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.certification.refresh_from_db()
        self.assertEqual(
            self.certification.name, "Web Security Fundamentals",
        )

    def test_anonymous_cannot_write(self):
        self.assertEqual(
            self.client.post(
                self.list_url, self.payload, format="json",
            ).status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(
            self.client.put(
                self.detail_url, self.payload, format="json",
            ).status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(
            self.client.patch(
                self.detail_url, {"name": "Nope"}, format="json",
            ).status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(
            self.client.delete(self.detail_url).status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(Certification.objects.count(), 1)
        self.certification.refresh_from_db()
        self.assertEqual(
            self.certification.name, "Web Security Fundamentals",
        )

    def test_editor_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            self.client.delete(self.detail_url).status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(Certification.objects.count(), 1)
        self.certification.refresh_from_db()
        self.assertEqual(
            self.certification.name, "Web Security Fundamentals",
        )

    def test_regular_user_cannot_patch(self):
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(
            self.detail_url, {"name": "Nope"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.certification.refresh_from_db()
        self.assertEqual(
            self.certification.name, "Web Security Fundamentals",
        )

    def test_regular_user_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(
            self.client.post(
                self.list_url, self.payload, format="json",
            ).status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(
            self.client.delete(self.detail_url).status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(Certification.objects.count(), 1)

    def test_unsupported_methods_and_missing_certification(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(
            self.client.delete(self.list_url).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )
        self.assertEqual(
            self.client.patch(self.list_url, {}, format="json").status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )
        self.assertEqual(
            self.client.get(self.star_url).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )
        self.assertEqual(
            self.client.get(
                reverse("api:certification-detail", args=[999999]),
            ).status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.assertEqual(
            self.client.get(f"{self.list_url}not-an-int/").status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_star_is_tied_to_request_user(self):
        self.client.force_authenticate(user=self.visitor)
        self.client.post(self.star_url)
        self.certification.refresh_from_db()
        self.assertIn(self.visitor, self.certification.starred_by.all())

        self.client.force_authenticate(user=self.owner)
        data = self.client.get(self.detail_url).data
        self.assertEqual(data["star_count"], 1)
        self.assertFalse(data["is_starred"])

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"name": "   "}, "name"),
            ({"name": '<img src="x" onerror="alert(1)">'}, "name"),
            ({"credential_url": "javascript:alert(1)"}, "credential_url"),
            ({"issue_date": "not-a-date"}, "issue_date"),
        ]:
            response = self.client.post(
                self.list_url, {**self.payload, **changes}, format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Certification.objects.count(), 1)

    def test_expiration_date_is_optional(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data["expiration_date"])

    def test_missing_certification(self):
        url = reverse("api:certification-detail", args=[999999])
        self.assertEqual(
            self.client.get(url).status_code, status.HTTP_404_NOT_FOUND,
        )

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(
            self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(
            self.client.get(self.star_url).status_code, status.HTTP_403_FORBIDDEN,
        )
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="editor", password="test-password"))
        response = client.patch(
            self.detail_url, {"name": "No CSRF"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.certification.refresh_from_db()
        self.assertEqual(
            self.certification.name, "Web Security Fundamentals",
        )

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="editor", password="test-password")
        page = client.get(self.detail_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.patch(
            self.detail_url, {"name": "Editor via CSRF"}, format="json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.certification.refresh_from_db()
        self.assertEqual(self.certification.name, "Editor via CSRF")
