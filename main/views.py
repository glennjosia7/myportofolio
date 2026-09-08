from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Glenn Josia Devano",
        "npm": "2506614712",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems student at Universitas Indonesia with a strong focus on "
            "Cybersecurity, Tech Consulting, and Project Management. "
            "Passionate about solving complex problems through secure, systems-based solutions."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Glenn Josia Devano",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)
