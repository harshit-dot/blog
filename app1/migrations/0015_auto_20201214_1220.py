# Generated by Django 3.1.3 on 2020-12-14 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0014_auto_20201214_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(default='', upload_to=''),
        ),
    ]
