# Generated by Django 4.2.11 on 2024-03-23 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="data",
            name="order",
            field=models.IntegerField(default=0),
        ),
    ]