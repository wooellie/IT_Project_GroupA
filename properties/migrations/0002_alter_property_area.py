from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("properties", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="property",
            name="area",
            field=models.CharField(
                blank=True, default="Unknown", max_length=100, null=True
            ),
        ),
    ]
