# Generated by Django 3.1.7 on 2021-03-12 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin1', '0002_auto_20210312_0707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
