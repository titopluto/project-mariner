# Generated by Django 3.2.6 on 2023-04-20 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("permission", "0002_auto_20230420_0000"),
    ]

    operations = [
        migrations.AlterField(
            model_name="permission",
            name="description",
            field=models.TextField(blank=True, default=""),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="permission",
            name="name",
            field=models.CharField(blank=True, default=" ", max_length=100),
            preserve_default=False,
        ),
    ]