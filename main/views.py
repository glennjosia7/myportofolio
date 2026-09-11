from django.shortcuts import render

from main.models import Achievement, Experience


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
