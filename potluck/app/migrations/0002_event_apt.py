# Generated by Django 4.1.2 on 2022-11-27 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='apt',
            field=models.CharField(default='', max_length=140),
        ),
    ]