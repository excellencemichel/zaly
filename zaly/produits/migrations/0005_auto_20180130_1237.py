# Generated by Django 2.0.1 on 2018-01-30 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produits', '0004_auto_20180121_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
