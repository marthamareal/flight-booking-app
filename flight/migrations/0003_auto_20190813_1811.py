# Generated by Django 2.2.2 on 2019-08-13 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0002_auto_20190813_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='number',
            field=models.SlugField(max_length=25, unique=True),
        ),
    ]