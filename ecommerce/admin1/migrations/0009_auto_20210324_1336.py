# Generated by Django 3.1.7 on 2021-03-24 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin1', '0008_auto_20210324_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='mobile',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='pin_code',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
