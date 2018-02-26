# Generated by Django 2.0.1 on 2018-02-14 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('produits', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('produits', models.ManyToManyField(blank=True, to='produits.Produit')),
            ],
        ),
    ]
