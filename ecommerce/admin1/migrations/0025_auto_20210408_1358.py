# Generated by Django 3.1.7 on 2021-04-08 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin1', '0024_auto_20210408_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
