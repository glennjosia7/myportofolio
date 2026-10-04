import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.forms import CertificationForm, ProjectForm
from main.models import Achievement, Certification, Experience, Project


def show_main(request):
    last_login = request.COOKIES.get(
        "last_login", "Belum ada sesi login / Cookie tidak ditemukan"
    )
    context = {
        "name": "Glenn Josia Devano",
        "npm": "2506614712",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems student at Universitas Indonesia, working on web security, "
            "digital forensics, and CTF challenge development. "
            "Active in RISTEK's NetSOS SIG and the COMPFEST 18 CTF Scientific Committee."
        ),
        "experience_list": Experience.objects.order_by("-started_at", "title")[:3],
        "achievement_list": Achievement.objects.exclude(evidence_image="").order_by("pk"),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Glenn Josia Devano",
        "experience_list": Experience.objects.order_by("-started_at", "title"),
    }
    return render(request, "experience.html", context)


def show_achievements(request):
    context = {
        "name": "Glenn Josia Devano",
        "achievement_list": Achievement.objects.order_by("pk"),
    }
    return render(request, "achievements.html", context)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related("starred_by").all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star.
    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )
        starred_by_names = ", ".join([user.username for user in starred_users])
        data.append(
            {
                "pk": str(project.id),
                "fields": {
                    "title": project.title,
                    "description": project.description,
                    "tech_stack": project.tech_stack,
                    "project_url": project.project_url,
                    "project_image_url": project.project_image_url,
                    "star_count": starred_users.count(),
                    "is_starred": is_starred,
                    "starred_by_names": starred_by_names,
                },
            }
        )

    return JsonResponse(data, safe=False)


def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Glenn Josia Devano",
        "title_query": title_query,
        "form": ProjectForm(),
    }
    return render(request, "project.html", context)


@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Glenn Josia Devano",
        "form": form,
        "form_title": "Add New Project",
        "submit_label": "Tambah Project",
    }
    return render(request, "projects_form.html", context)


@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)

    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@login_required(login_url="/login/")
def update_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:show_projects")

    context = {
        "name": "Glenn Josia Devano",
        "form": form,
        "form_title": "Edit Project",
        "submit_label": "Simpan Perubahan",
    }
    return render(request, "projects_form.html", context)


@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")


def get_certifications_json(request):
    name_query = request.GET.get("name", "").strip()
    certifications = Certification.objects.prefetch_related("starred_by").order_by(
        "-issue_date", "name"
    )

    if name_query:
        certifications = certifications.filter(
            Q(name__icontains=name_query)
            | Q(issuing_organization__icontains=name_query)
        )

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star.
    data = []
    for certification in certifications:
        starred_users = certification.starred_by.all()
        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )
        data.append(
            {
                "pk": certification.id,
                "fields": {
                    "name": certification.name,
                    "issuing_organization": certification.issuing_organization,
                    "issue_date": certification.issue_date.isoformat(),
                    "expiration_date": (
                        certification.expiration_date.isoformat()
                        if certification.expiration_date
                        else None
                    ),
                    "credential_id": certification.credential_id,
                    "credential_url": certification.credential_url,
                    "star_count": starred_users.count(),
                    "is_starred": is_starred,
                    "starred_by_names": ", ".join(
                        user.username for user in starred_users
                    ),
                },
            }
        )

    return JsonResponse(data, safe=False)


def show_certifications(request):
    context = {
        "name": "Glenn Josia Devano",
        "name_query": request.GET.get("name", "").strip(),
        "form": CertificationForm(),
    }
    return render(request, "certifications.html", context)


@require_POST
def create_certification_ajax(request):
    if not request.user.has_perm("main.add_certification"):
        return JsonResponse(
            {
                "message": "Hanya pengguna dengan izin menambah yang dapat "
                "menambahkan certification."
            },
            status=403,
        )

    form = CertificationForm(request.POST)

    if form.is_valid():
        certification = form.save()
        return JsonResponse(
            {
                "message": "Certification berhasil ditambahkan.",
                "pk": certification.id,
            },
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@login_required(login_url="/login/")
def create_certification(request):
    if not request.user.has_perm("main.add_certification"):
        raise PermissionDenied

    form = CertificationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Certification berhasil ditambahkan!")
        return redirect("main:show_certifications")

    context = {
        "name": "Glenn Josia Devano",
        "form": form,
        "form_title": "Add Certification",
        "submit_label": "Add Certification",
    }
    return render(request, "certification_form.html", context)


@login_required(login_url="/login/")
def update_certification(request, certification_id):
    if not request.user.has_perm("main.change_certification"):
        raise PermissionDenied

    certification = get_object_or_404(Certification, pk=certification_id)
    form = CertificationForm(request.POST or None, instance=certification)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Certification berhasil diperbarui!")
        return redirect("main:show_certifications")

    context = {
        "name": "Glenn Josia Devano",
        "form": form,
        "form_title": "Edit Certification",
        "submit_label": "Save Changes",
    }
    return render(request, "certification_form.html", context)


@login_required(login_url="/login/")
def delete_certification(request, certification_id):
    if not request.user.has_perm("main.delete_certification"):
        raise PermissionDenied

    certification = get_object_or_404(Certification, pk=certification_id)

    if request.method == "POST":
        certification.delete()
        messages.success(request, "Certification berhasil dihapus!")

    return redirect("main:show_certifications")


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Glenn Josia Devano",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie(
            "last_login",
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        return response

    context = {
        "name": "Glenn Josia Devano",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response


# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star.
@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")


# Editor dan pemilik punya hak pengguna biasa, jadi sama-sama boleh memberi star.
@login_required(login_url="/login/")
def toggle_star_certification(request, certification_id):
    certification = get_object_or_404(Certification, pk=certification_id)

    if request.method == "POST":
        if request.user in certification.starred_by.all():
            certification.starred_by.remove(request.user)
        else:
            certification.starred_by.add(request.user)

    return redirect("main:show_certifications")
