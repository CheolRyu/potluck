# Generated by Django 4.1.2 on 2022-12-13 22:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_remove_entertainment_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entertainment',
            name='owner',
        ),
    ]
