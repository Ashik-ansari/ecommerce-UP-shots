# Generated by Django 3.1.7 on 2021-04-01 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin1', '0017_auto_20210331_0603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='mobile',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
