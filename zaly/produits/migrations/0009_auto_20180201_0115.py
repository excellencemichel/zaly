# Generated by Django 2.0.1 on 2018-02-01 01:15

import django.core.files.storage
from django.db import migrations, models
import produits.models


class Migration(migrations.Migration):

    dependencies = [
        ('produits', '0008_produit_media'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='media',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/home/michel/zaly/static_cdn/protected'), upload_to=produits.models.download_media_location),
        ),
    ]
