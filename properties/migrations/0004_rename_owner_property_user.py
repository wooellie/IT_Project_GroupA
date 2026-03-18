from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("properties", "0003_alter_property_area"),
    ]

    operations = [
        migrations.RenameField(
            model_name="property",
            old_name="owner",
            new_name="user",
        ),
    ]
