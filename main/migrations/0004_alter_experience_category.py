from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_achievement_evidence_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="experience",
            name="category",
            field=models.CharField(
                choices=[
                    ("internship", "Internship"),
                    ("research", "Research"),
                    ("volunteer", "Volunteer"),
                    ("part-time", "Part-Time"),
                    ("full-time", "Full-Time"),
                    ("freelance", "Freelance"),
                    ("organization", "Organization"),
                    ("committee", "Committee"),
                ],
                default="full-time",
                max_length=20,
            ),
        ),
    ]
