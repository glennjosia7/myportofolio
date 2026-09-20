from django.urls import path

from main.views import (
    show_main,
    show_experience,
    show_achievements,
    show_projects,
    create_project,
    update_project,
    get_projects_json,
    delete_project,
    show_certifications,
    create_certification,
    update_certification,
    delete_certification,
    get_certifications_json,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("achievements/", show_achievements, name="show_achievements"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/<uuid:project_id>/update/", update_project, name="update_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("certifications/", show_certifications, name="show_certifications"),
    path("certifications/add/", create_certification, name="create_certification"),
    path("certifications/<int:certification_id>/update/", update_certification, name="update_certification"),
    path("certifications/<int:certification_id>/delete/", delete_certification, name="delete_certification"),
    path("certifications/json/", get_certifications_json, name="get_certifications_json"),
]
