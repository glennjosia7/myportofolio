from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_alter_experience_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="experience",
            name="logo",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
