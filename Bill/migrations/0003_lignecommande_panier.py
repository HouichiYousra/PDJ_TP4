# Generated by Django 3.0.4 on 2020-07-04 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Bill', '0002_panier'),
    ]

    operations = [
        migrations.AddField(
            model_name='lignecommande',
            name='panier',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='lignes_com', to='Bill.Panier'),
        ),
    ]
