from django.forms import DateInput, ModelForm, TextInput, Textarea, URLInput

from main.models import Certification, Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/DevCoder-7/myportofolio",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }


class CertificationForm(ModelForm):
    class Meta:
        model = Certification
        fields = [
            "name",
            "issuing_organization",
            "issue_date",
            "expiration_date",
            "credential_id",
            "credential_url",
        ]

        labels = {
            "name": "Certification Name",
            "issuing_organization": "Issuing Organization",
            "issue_date": "Issue Date",
            "expiration_date": "Expiration Date",
            "credential_id": "Credential ID",
            "credential_url": "Credential URL",
        }

        widgets = {
            "name": TextInput(attrs={"placeholder": "Google Cybersecurity Certificate"}),
            "issuing_organization": TextInput(attrs={"placeholder": "Coursera"}),
            "issue_date": DateInput(attrs={"type": "date"}),
            "expiration_date": DateInput(attrs={"type": "date"}),
            "credential_id": TextInput(attrs={"placeholder": "ABC-123-XYZ"}),
            "credential_url": URLInput(attrs={"placeholder": "https://example.com/verify"}),
        }
