# Generated by Django 3.0.3 on 2020-06-08 02:28
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Bill', '0002_client_tel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facture',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factures', to='Bill.Client'),
        ),
    ]
