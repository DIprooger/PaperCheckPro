# Generated by Django 4.2.10 on 2024-02-24 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_work', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentwork',
            name='image_work',
            field=models.ImageField(upload_to='image'),
        ),
    ]
