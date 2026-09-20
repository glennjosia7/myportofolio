from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import CertificationForm, ProjectForm
from main.models import Achievement, Certification, Experience, Project


def show_main(request):
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
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")


def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Glenn Josia Devano",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)


def create_project(request):
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


def update_project(request, project_id):
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


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")


def get_certifications_json(request):
    certifications = Certification.objects.order_by("-issue_date", "name")
    certifications_json = serializers.serialize("json", certifications)
    return HttpResponse(certifications_json, content_type="application/json")


def show_certifications(request):
    json_response = get_certifications_json(request)
    certifications = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    certifications = [item.object for item in certifications]

    context = {
        "name": "Glenn Josia Devano",
        "certification_list": certifications,
    }
    return render(request, "certifications.html", context)


def create_certification(request):
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


def update_certification(request, certification_id):
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


def delete_certification(request, certification_id):
    certification = get_object_or_404(Certification, pk=certification_id)

    if request.method == "POST":
        certification.delete()
        messages.success(request, "Certification berhasil dihapus!")

    return redirect("main:show_certifications")
