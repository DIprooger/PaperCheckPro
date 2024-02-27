# Generated by Django 4.2.10 on 2024-02-26 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_merge_20240225_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='class_num',
            field=models.CharField(choices=[('05A', '5А'), ('05B', '5Б'), ('05C', '5В'), ('05D', '5Г'), ('05E', '5Д'), ('06A', '6А'), ('06B', '6Б'), ('06C', '6В'), ('06D', '6Г'), ('06E', '6Д'), ('07A', '7А'), ('07B', '7Б'), ('07C', '7В'), ('07D', '7Г'), ('07E', '7Д'), ('08A', '8А'), ('08B', '8Б'), ('08C', '8В'), ('08D', '8Г'), ('08E', '8Д'), ('09A', '9А'), ('09B', '9Б'), ('09C', '9В'), ('09D', '9Г'), ('09E', '9Д'), ('10A', '10А'), ('10B', '10Б'), ('10C', '10В'), ('10D', '10Г'), ('10E', '10Д'), ('11A', '11А'), ('11B', '11Б'), ('11C', '11В'), ('11D', '11Г'), ('11E', '11Д'), ('-', '-')], default='---', help_text='Enter class or a dash (-).', max_length=3, verbose_name='Class number'),
        ),
    ]
