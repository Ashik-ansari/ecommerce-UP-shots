# Generated by Django 3.1.7 on 2021-03-24 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin1', '0007_address_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='mobile',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='address',
            name='pin_code',
            field=models.IntegerField(null=True),
        ),
    ]
