import json

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.staticfiles import finders

from main.models import Achievement, Experience, Project


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
        routes = ["show_main", "show_experience", "show_achievements", "show_projects"]
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
        self.project = Project.objects.create(
            title="Portfolio Website",
            description="A personal portfolio built with Django.",
            tech_stack="Django, Python, HTML, CSS",
            project_url="https://github.com/glennjosia7/myportofolio",
        )

    def test_projects_page_uses_json_data_and_title_filter(self):
        other_project = Project.objects.create(
            title="Unrelated Project",
            description="Another project.",
            tech_stack="Python",
        )
        response = self.client.get(
            reverse("main:show_projects"),
            {"title": "portfolio"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project.html")
        self.assertEqual(
            [project.title for project in response.context["project_list"]],
            [self.project.title],
        )
        self.assertContains(response, self.project.title)
        self.assertNotContains(response, other_project.title)
        self.assertContains(response, 'value="portfolio"')

    def test_projects_json_endpoint_serializes_projects(self):
        response = self.client.get(reverse("main:get_projects_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["model"], "main.project")
        self.assertEqual(data[0]["fields"]["title"], self.project.title)

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
