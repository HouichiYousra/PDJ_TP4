# Generated by Django 3.0.3 on 2020-06-13 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bill', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lignefacture',
            name='prix',
            field=models.IntegerField(default=1),
        ),
    ]
