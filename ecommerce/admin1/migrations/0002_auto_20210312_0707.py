# Generated by Django 3.1.7 on 2021-03-12 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin1', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='image',
            new_name='image1',
        ),
        migrations.AddField(
            model_name='products',
            name='image2',
            field=models.ImageField(default=0, upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='products',
            name='image3',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]