# Generated by Django 4.2.10 on 2024-02-25 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_album'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_work', models.ImageField(upload_to='student_works/')),
                ('text_work', models.TextField(blank=True, null=True)),
                ('proven_work', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
