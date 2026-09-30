import json
from datetime import date

from django.contrib.auth.models import Group, Permission, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.staticfiles import finders

from main.forms import ProjectForm
from main.models import Achievement, Certification, Experience, Project


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="RISTEK Fasilkom UI - Member of NetSOS SIG",
            description="Develop a Digital Forensics challenge for Project bobol.netsos.id.",
            category="organization",
        )

    def test_main_url_is_accessible(self):
        achievement = Achievement.objects.create(
            title="POLRI CTF",
            result="1st Place",
            organizer="E-Sport Kapolri Cup",
            evidence_image="img/achievements/polri-ctf-award.jpeg",
            year=2026,
        )
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, achievement.title)
        self.assertContains(response, "View experience")
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "RISTEK Fasilkom UI - Member of NetSOS SIG")
        self.assertEqual(self.experience.category, "organization")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Organization")
        self.assertContains(response, "Ongoing")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "No experience added yet.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Ongoing")

    def test_experience_description_uses_list_items(self):
        self.experience.description = "First activity.\n\nSecond activity."
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "<li>First activity.</li>", html=True)
        self.assertContains(response, "<li>Second activity.</li>", html=True)


class AchievementTest(TestCase):
    def test_achievements_url_and_template(self):
        response = self.client.get(reverse("main:show_achievements"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "achievements.html")
        self.assertTemplateUsed(response, "base.html")

    def test_all_achievements_appear_from_database(self):
        first = Achievement.objects.create(
            title="POLRI CTF",
            result="1st Place",
            organizer="E-Sport Kapolri Cup in collaboration with SiberLab.id",
            evidence_image="img/achievements/polri-ctf-award.jpeg",
            year=2026,
        )
        second = Achievement.objects.create(
            title="WreckIT! 7.0 CTF Competition",
            result="Finalist",
            organizer="Politeknik Siber dan Sandi Negara",
        )
        response = self.client.get(reverse("main:show_achievements"))

        self.assertQuerySetEqual(response.context["achievement_list"], [first, second])
        for achievement in [first, second]:
            self.assertContains(response, achievement.title)
            self.assertContains(response, achievement.result)
            self.assertContains(response, achievement.organizer)
        self.assertContains(response, "/static/img/achievements/polri-ctf-award.jpeg")
        self.assertContains(response, "Evidence file not attached")
        self.assertNotContains(response, "No achievements added yet.")

    def test_empty_achievements_page(self):
        response = self.client.get(reverse("main:show_achievements"))

        self.assertContains(response, "No achievements added yet.")
        self.assertNotContains(response, 'class="achievement-card"')
        self.assertNotContains(response, "POLRI CTF")

    def test_achievement_without_year(self):
        achievement = Achievement.objects.create(
            title="WreckIT! 7.0 CTF Competition",
            result="Finalist",
            organizer="Politeknik Siber dan Sandi Negara",
        )
        achievement.full_clean()
        response = self.client.get(reverse("main:show_achievements"))

        self.assertEqual(str(achievement), "Finalist - WreckIT! 7.0 CTF Competition")
        self.assertContains(response, "Evidence file not attached")
        self.assertNotContains(response, "None")

    def test_achievement_text_is_escaped(self):
        Achievement.objects.create(
            title='<script>alert("test")</script>',
            result="Finalist",
            organizer="Test organizer",
        )
        response = self.client.get(reverse("main:show_achievements"))

        self.assertContains(response, "&lt;script&gt;")
        self.assertNotContains(response, "<script>")

    def test_shared_navigation_and_footer_on_every_page(self):
        routes = [
            "show_main",
            "show_experience",
            "show_achievements",
            "show_projects",
            "show_certifications",
        ]
        for current in routes:
            with self.subTest(page=current):
                response = self.client.get(reverse(f"main:{current}"))
                self.assertTemplateUsed(response, "base.html")
                for route in routes:
                    self.assertContains(response, f'href="{reverse(f"main:{route}")}"')
                self.assertContains(response, f'href="{reverse(f"main:{current}")}" aria-current="page"')
                self.assertContains(response, 'aria-current="page"', count=1)
                self.assertContains(response, '<footer class="site-footer">')


class AchievementFixtureTest(TestCase):
    fixtures = ["achievements.json"]

    def test_fixture_matches_cv_awards(self):
        self.assertEqual(Achievement.objects.count(), 5)
        self.assertEqual(
            list(Achievement.objects.order_by("pk").values_list("title", "result", "year")),
            [
                ("POLRI CTF", "1st Place", 2026),
                ("WreckIT! 7.0 CTF Competition", "Finalist", 2026),
                ("FINDIT! CTF", "Finalist", 2026),
                ("DSG Zero Day CTF Open Arena", "Top 10 Honorable Mention", 2026),
                ("Global Cyber Skills Benchmark 2026", "62nd of 589 Teams", 2026),
            ],
        )
        evidence = Achievement.objects.exclude(evidence_image="")
        self.assertEqual(evidence.count(), 5)
        for achievement in evidence:
            self.assertIsNotNone(finders.find(achievement.evidence_image))

    def test_dashboard_shows_all_five_achievements(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(len(response.context["achievement_list"]), 5)


class ExperienceFixtureTest(TestCase):
    fixtures = ["experiences.json"]

    def test_fixture_contains_three_cv_experiences(self):
        self.assertEqual(Experience.objects.count(), 3)
        self.assertEqual(
            list(Experience.objects.order_by("-started_at").values_list("title", "category")),
            [
                ("COMPFEST 18 - CTF Scientific Committee Staff", "committee"),
                ("RISTEK Fasilkom UI - Member of NetSOS SIG", "organization"),
                ("Open House Fasilkom UI 2025 - DEC Staff", "committee"),
            ],
        )
        self.assertEqual(Experience.objects.filter(ended_at__isnull=True).count(), 2)
        logos = Experience.objects.exclude(logo="")
        self.assertEqual(logos.count(), 3)
        for experience in logos:
            self.assertIsNotNone(finders.find(experience.logo))

    def test_dashboard_shows_all_three_experiences(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(len(response.context["experience_list"]), 3)
        self.assertContains(response, "COMPFEST 18")
        self.assertContains(response, "Open House Fasilkom UI 2025")


class ProjectTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="owner", password="ownerpass123"
        )
        self.user = User.objects.create_user(
            username="visitor", password="visitorpass123"
        )
        self.client.force_login(self.admin)
        self.project = Project.objects.create(
            title="Portfolio Website",
            description="A personal portfolio built with Django.",
            tech_stack="Django, Python, HTML, CSS",
            project_url="https://github.com/glennjosia7/myportofolio",
        )

    def test_projects_page_renders_ajax_shell(self):
        response = self.client.get(
            reverse("main:show_projects"),
            {"title": "portfolio"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project.html")
        self.assertContains(response, 'id="grid"')
        self.assertContains(response, 'id="project-search-form"')
        self.assertContains(response, 'value="portfolio"')

    def test_projects_json_endpoint_filters_and_exposes_star_fields(self):
        Project.objects.create(
            title="Unrelated Project",
            description="Another project.",
            tech_stack="Python",
        )
        response = self.client.get(
            reverse("main:get_projects_json"),
            {"title": "portfolio"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["pk"], str(self.project.id))
        self.assertEqual(data[0]["fields"]["title"], self.project.title)
        self.assertEqual(data[0]["fields"]["star_count"], 0)
        self.assertFalse(data[0]["fields"]["is_starred"])
        self.assertEqual(data[0]["fields"]["starred_by_names"], "")

    def test_create_project_with_form(self):
        response = self.client.get(reverse("main:create_project"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")
        self.assertContains(response, "Nama Proyek")

        response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "Security Lab",
                "description": "A small project for security practice.",
                "tech_stack": "Python",
                "project_url": "",
                "project_image_url": "",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Project.objects.filter(title="Security Lab").exists())
        self.assertContains(response, "Proyek baru berhasil ditambahkan!")

    def test_create_project_rejects_invalid_form(self):
        response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "",
                "description": "",
                "tech_stack": "",
                "project_url": "",
                "project_image_url": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")
        self.assertEqual(Project.objects.count(), 1)
        self.assertTrue(response.context["form"].errors)

    def test_update_project_with_form(self):
        response = self.client.get(
            reverse("main:update_project", args=[self.project.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")
        self.assertContains(response, self.project.title)
        self.assertNotContains(
            response,
            f'action="{reverse("main:create_project")}"',
        )

        response = self.client.post(
            reverse("main:update_project", args=[self.project.id]),
            {
                "title": "Updated Portfolio Website",
                "description": self.project.description,
                "tech_stack": self.project.tech_stack,
                "project_url": self.project.project_url,
                "project_image_url": "",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Updated Portfolio Website")
        self.assertContains(response, "Proyek berhasil diperbarui!")

    def test_update_project_rejects_invalid_form(self):
        response = self.client.post(
            reverse("main:update_project", args=[self.project.id]),
            {
                "title": "",
                "description": "",
                "tech_stack": "",
                "project_url": "",
                "project_image_url": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")
        self.assertEqual(Project.objects.count(), 1)
        self.assertTrue(response.context["form"].errors)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio Website")

    def test_delete_project_requires_post(self):
        get_response = self.client.get(
            reverse("main:delete_project", args=[self.project.id])
        )
        self.assertEqual(get_response.status_code, 302)
        self.assertTrue(Project.objects.filter(pk=self.project.id).exists())

        post_response = self.client.post(
            reverse("main:delete_project", args=[self.project.id])
        )
        self.assertEqual(post_response.status_code, 302)
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_project_writes_require_login(self):
        self.client.logout()

        for url in [
            reverse("main:create_project"),
            reverse("main:update_project", args=[self.project.id]),
            reverse("main:delete_project", args=[self.project.id]),
        ]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse("main:login")))

    def test_project_writes_forbidden_for_regular_user(self):
        self.client.force_login(self.user)

        for url in [
            reverse("main:create_project"),
            reverse("main:update_project", args=[self.project.id]),
            reverse("main:delete_project", args=[self.project.id]),
        ]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 403)

    def test_project_write_controls_only_for_superuser(self):
        owner_response = self.client.get(reverse("main:show_projects"))
        self.assertContains(owner_response, 'id="add-project-modal"')
        self.assertContains(owner_response, "Tambah Proyek")

        self.client.force_login(self.user)
        viewer_response = self.client.get(reverse("main:show_projects"))
        self.assertNotContains(viewer_response, "Tambah Proyek")
        self.assertNotContains(viewer_response, 'id="add-project-modal"')

    def test_toggle_star_adds_and_removes(self):
        star_url = reverse("main:toggle_star", args=[self.project.id])
        self.client.force_login(self.user)

        self.client.post(star_url)
        self.assertIn(self.user, self.project.starred_by.all())

        self.client.post(star_url)
        self.assertNotIn(self.user, self.project.starred_by.all())

    def test_toggle_star_requires_login(self):
        star_url = reverse("main:toggle_star", args=[self.project.id])
        self.client.logout()

        response = self.client.post(star_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("main:login")))
        self.assertEqual(self.project.starred_by.count(), 0)

    def test_projects_json_reports_user_star_status(self):
        self.project.starred_by.add(self.user)
        self.client.force_login(self.user)
        response = self.client.get(reverse("main:get_projects_json"))
        data = json.loads(response.content)

        self.assertEqual(data[0]["fields"]["star_count"], 1)
        self.assertTrue(data[0]["fields"]["is_starred"])
        self.assertEqual(data[0]["fields"]["starred_by_names"], "visitor")

    def test_create_project_ajax_creates_project_for_superuser(self):
        response = self.client.post(
            reverse("main:create_project_ajax"),
            {
                "title": "AJAX Project",
                "description": "Made via AJAX.",
                "tech_stack": "Django",
                "project_url": "",
                "project_image_url": "",
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Project.objects.filter(title="AJAX Project").exists())
        self.assertEqual(
            json.loads(response.content)["message"],
            "Proyek berhasil ditambahkan.",
        )

    def test_create_project_ajax_requires_post(self):
        response = self.client.get(reverse("main:create_project_ajax"))
        self.assertEqual(response.status_code, 405)

    def test_create_project_ajax_forbidden_for_anonymous(self):
        self.client.logout()
        response = self.client.post(
            reverse("main:create_project_ajax"),
            {
                "title": "Nope",
                "description": "",
                "tech_stack": "",
                "project_url": "",
                "project_image_url": "",
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertFalse(Project.objects.filter(title="Nope").exists())

    def test_create_project_ajax_forbidden_for_regular_user(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("main:create_project_ajax"),
            {
                "title": "Nope",
                "description": "",
                "tech_stack": "",
                "project_url": "",
                "project_image_url": "",
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Project.objects.filter(title="Nope").exists())

    def test_create_project_ajax_rejects_invalid_form(self):
        response = self.client.post(
            reverse("main:create_project_ajax"),
            {
                "title": "   ",
                "description": "",
                "tech_stack": "",
                "project_url": "not-a-url",
                "project_image_url": "",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", json.loads(response.content))


class ProjectFormTest(TestCase):
    def test_form_strips_html_tags_from_text_fields(self):
        form = ProjectForm(
            data={
                "title": "Halo <b>dunia</b>",
                "description": "Deskripsi <script>alert(1)</script>",
                "tech_stack": "Django <i>Python</i>",
                "project_url": "",
                "project_image_url": "",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["title"], "Halo dunia")
        self.assertEqual(form.cleaned_data["description"], "Deskripsi alert(1)")
        self.assertEqual(form.cleaned_data["tech_stack"], "Django Python")

    def test_form_rejects_title_made_only_of_tags(self):
        form = ProjectForm(
            data={
                "title": '<img src="x" onerror="alert(1)">',
                "description": "Valid description.",
                "tech_stack": "Django",
                "project_url": "",
                "project_image_url": "",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)


class CertificationTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="owner", password="ownerpass123"
        )
        self.user = User.objects.create_user(
            username="visitor", password="visitorpass123"
        )
        self.editor = User.objects.create_user(
            username="editor", password="editorpass123"
        )
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        editor_group.permissions.add(
            Permission.objects.get(codename="change_certification")
        )
        self.editor.groups.add(editor_group)
        self.client.force_login(self.admin)
        self.certification = Certification.objects.create(
            name="Web Security Fundamentals",
            issuing_organization="Security Academy",
            issue_date=date(2026, 9, 1),
            credential_id="SEC-2026-001",
            credential_url="https://example.com/verify/SEC-2026-001",
        )

    def test_certifications_page_uses_json_data(self):
        response = self.client.get(reverse("main:show_certifications"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "certifications.html")
        self.assertEqual(
            [item.name for item in response.context["certification_list"]],
            [self.certification.name],
        )
        self.assertContains(response, self.certification.name)
        self.assertContains(response, self.certification.issuing_organization)
        self.assertContains(response, "No expiration")
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_empty_certifications_page(self):
        Certification.objects.all().delete()
        response = self.client.get(reverse("main:show_certifications"))

        self.assertContains(response, "No certifications added yet.")

    def test_certifications_json_endpoint(self):
        response = self.client.get(reverse("main:get_certifications_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertEqual(data[0]["model"], "main.certification")
        self.assertEqual(data[0]["fields"]["name"], self.certification.name)

    def test_create_certification_with_form(self):
        response = self.client.post(
            reverse("main:create_certification"),
            {
                "name": "Python Certificate",
                "issuing_organization": "Python Institute",
                "issue_date": "2026-09-02",
                "expiration_date": "",
                "credential_id": "PY-001",
                "credential_url": "https://example.com/verify/PY-001",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Certification.objects.filter(name="Python Certificate").exists())
        self.assertContains(response, "Certification berhasil ditambahkan!")

    def test_update_certification_with_form(self):
        response = self.client.post(
            reverse("main:update_certification", args=[self.certification.id]),
            {
                "name": "Updated Web Security Fundamentals",
                "issuing_organization": "Security Academy",
                "issue_date": "2026-09-01",
                "expiration_date": "2028-09-01",
                "credential_id": self.certification.credential_id,
                "credential_url": self.certification.credential_url,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.certification.refresh_from_db()
        self.assertEqual(self.certification.name, "Updated Web Security Fundamentals")
        self.assertEqual(self.certification.expiration_date, date(2028, 9, 1))
        self.assertContains(response, "Certification berhasil diperbarui!")

    def test_delete_certification_only_on_post(self):
        get_response = self.client.get(
            reverse("main:delete_certification", args=[self.certification.id])
        )
        self.assertEqual(get_response.status_code, 302)
        self.assertTrue(Certification.objects.filter(pk=self.certification.id).exists())

        post_response = self.client.post(
            reverse("main:delete_certification", args=[self.certification.id])
        )
        self.assertEqual(post_response.status_code, 302)
        self.assertFalse(Certification.objects.filter(pk=self.certification.id).exists())

    def test_certification_writes_require_login(self):
        self.client.logout()

        for url in [
            reverse("main:create_certification"),
            reverse("main:update_certification", args=[self.certification.id]),
            reverse("main:delete_certification", args=[self.certification.id]),
        ]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse("main:login")))

    def test_regular_user_forbidden_from_certification_writes(self):
        self.client.force_login(self.user)

        for url in [
            reverse("main:create_certification"),
            reverse("main:update_certification", args=[self.certification.id]),
            reverse("main:delete_certification", args=[self.certification.id]),
        ]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 403)

    def test_editor_can_update_but_not_create_or_delete(self):
        self.client.force_login(self.editor)

        self.assertEqual(
            self.client.get(
                reverse("main:update_certification", args=[self.certification.id])
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(reverse("main:create_certification")).status_code, 403
        )
        self.assertEqual(
            self.client.get(
                reverse("main:delete_certification", args=[self.certification.id])
            ).status_code,
            403,
        )

    def test_editor_can_save_certification_update(self):
        self.client.force_login(self.editor)

        response = self.client.post(
            reverse("main:update_certification", args=[self.certification.id]),
            {
                "name": "Editor Updated Certificate",
                "issuing_organization": self.certification.issuing_organization,
                "issue_date": "2026-09-01",
                "expiration_date": "",
                "credential_id": self.certification.credential_id,
                "credential_url": self.certification.credential_url,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.certification.refresh_from_db()
        self.assertEqual(self.certification.name, "Editor Updated Certificate")
        self.assertContains(response, "Certification berhasil diperbarui!")

    def test_certification_controls_follow_permissions(self):
        owner = self.client.get(reverse("main:show_certifications"))
        self.assertContains(owner, reverse("main:create_certification"))
        self.assertContains(
            owner,
            reverse("main:update_certification", args=[self.certification.id]),
        )
        self.assertContains(
            owner,
            reverse("main:delete_certification", args=[self.certification.id]),
        )

        self.client.force_login(self.user)
        viewer = self.client.get(reverse("main:show_certifications"))
        self.assertNotContains(viewer, "Add Certification")
        self.assertNotContains(
            viewer,
            reverse("main:update_certification", args=[self.certification.id]),
        )
        self.assertNotContains(
            viewer,
            reverse("main:delete_certification", args=[self.certification.id]),
        )

        self.client.force_login(self.editor)
        editor_view = self.client.get(reverse("main:show_certifications"))
        self.assertNotContains(editor_view, "Add Certification")
        self.assertContains(
            editor_view,
            reverse("main:update_certification", args=[self.certification.id]),
        )
        self.assertNotContains(
            editor_view,
            reverse("main:delete_certification", args=[self.certification.id]),
        )

    def test_toggle_star_certification_adds_and_removes(self):
        star_url = reverse(
            "main:toggle_star_certification", args=[self.certification.id]
        )
        self.client.force_login(self.user)

        self.client.post(star_url)
        self.assertIn(self.user, self.certification.starred_by.all())
        self.assertEqual(self.certification.starred_by.count(), 1)

        self.client.post(star_url)
        self.assertNotIn(self.user, self.certification.starred_by.all())
        self.assertEqual(self.certification.starred_by.count(), 0)

    def test_toggle_star_certification_requires_login(self):
        star_url = reverse(
            "main:toggle_star_certification", args=[self.certification.id]
        )
        self.client.logout()

        response = self.client.post(star_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("main:login")))
        self.assertEqual(self.certification.starred_by.count(), 0)

    def test_certification_star_count_and_status_in_template(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse("main:toggle_star_certification", args=[self.certification.id])
        )
        response = self.client.get(reverse("main:show_certifications"))

        self.assertContains(response, "Unstar")
        self.assertContains(response, '<span class="star-count">1</span>', html=True)

    def test_certifications_json_uses_natural_keys_for_stars(self):
        self.certification.starred_by.add(self.user)
        response = self.client.get(reverse("main:get_certifications_json"))
        data = json.loads(response.content)

        self.assertEqual(data[0]["fields"]["starred_by"], [["visitor"]])


class AuthenticationTest(TestCase):
    def test_register_creates_account_and_redirects_to_login(self):
        response = self.client.get(reverse("main:register"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

        response = self.client.post(
            reverse("main:register"),
            {
                "username": "newcomer",
                "password1": "a-very-strong-pass-123",
                "password2": "a-very-strong-pass-123",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="newcomer").exists())
        self.assertContains(response, "Akun berhasil dibuat. Silakan login.")

    def test_register_rejects_mismatched_passwords(self):
        response = self.client.post(
            reverse("main:register"),
            {
                "username": "newcomer",
                "password1": "a-very-strong-pass-123",
                "password2": "different-pass-123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newcomer").exists())
        self.assertTrue(response.context["form"].errors)

    def test_login_sets_session_and_last_login_cookie(self):
        User.objects.create_user(username="visitor", password="visitorpass123")

        response = self.client.post(
            reverse("main:login"),
            {"username": "visitor", "password": "visitorpass123"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("main:show_main"))
        self.assertIn("sessionid", response.cookies)
        self.assertIn("last_login", response.cookies)

    def test_login_rejects_wrong_password(self):
        User.objects.create_user(username="visitor", password="visitorpass123")

        response = self.client.post(
            reverse("main:login"),
            {"username": "visitor", "password": "wrong-pass"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertNotIn("sessionid", response.cookies)

    def test_main_shows_last_login_cookie(self):
        self.client.cookies["last_login"] = "2026-09-20 10:30:00"

        response = self.client.get(reverse("main:show_main"))

        self.assertContains(response, "2026-09-20 10:30:00")

    def test_main_without_cookie_shows_default(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertContains(response, "Belum ada sesi login")

    def test_logout_clears_session_and_last_login_cookie(self):
        User.objects.create_user(username="visitor", password="visitorpass123")
        self.client.login(username="visitor", password="visitorpass123")
        self.client.cookies["last_login"] = "2026-09-20 10:30:00"

        response = self.client.get(reverse("main:logout"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.cookies["last_login"].value, "")

        home = self.client.get(reverse("main:show_main"))
        self.assertContains(home, reverse("main:login"))
        self.assertContains(home, reverse("main:register"))

    def test_navbar_shows_username_when_logged_in(self):
        User.objects.create_user(username="visitor", password="visitorpass123")
        self.client.login(username="visitor", password="visitorpass123")

        response = self.client.get(reverse("main:show_main"))

        self.assertContains(response, '<span class="nav-user">visitor</span>')
        self.assertContains(response, reverse("main:logout"))
