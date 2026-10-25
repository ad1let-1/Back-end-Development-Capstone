from datetime import date

from django.db import migrations


def add_demo_concert(apps, schema_editor):
    concert = apps.get_model("concert", "Concert")
    concert.objects.get_or_create(
        concert_name="Djirection Live in Almaty",
        defaults={"duration": 3, "city": "Almaty", "date": date(2026, 11, 21)},
    )


class Migration(migrations.Migration):
    dependencies = [("concert", "0001_initial")]
    operations = [migrations.RunPython(add_demo_concert, migrations.RunPython.noop)]
