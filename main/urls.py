from django.urls import path

from main.views import (
    show_main,
    show_experience,
    show_achievements,
    show_projects,
    create_project,
    create_project_ajax,
    update_project,
    get_projects_json,
    delete_project,
    toggle_star,
    register,
    login_user,
    logout_user,
    show_certifications,
    create_certification,
    update_certification,
    delete_certification,
    toggle_star_certification,
    get_certifications_json,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("achievements/", show_achievements, name="show_achievements"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
    path("projects/<uuid:project_id>/update/", update_project, name="update_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path(
        "projects/<uuid:project_id>/star/",
        toggle_star,
        name="toggle_star",
    ),
    path("certifications/", show_certifications, name="show_certifications"),
    path("certifications/add/", create_certification, name="create_certification"),
    path("certifications/<int:certification_id>/update/", update_certification, name="update_certification"),
    path("certifications/<int:certification_id>/delete/", delete_certification, name="delete_certification"),
    path(
        "certifications/<int:certification_id>/star/",
        toggle_star_certification,
        name="toggle_star_certification",
    ),
    path("certifications/json/", get_certifications_json, name="get_certifications_json"),
]
