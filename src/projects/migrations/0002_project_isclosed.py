# Generated by Django 3.2 on 2021-04-25 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='isClosed',
            field=models.BooleanField(default=False),
        ),
    ]
