# Generated by Django 4.2.9 on 2024-03-13 17:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0002_sсholclass_remove_user_is_staff_user_student_class'),
        ('student_work', '0002_alter_studentwork_assessment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentwork',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teacher', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='TypeStudentWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_work', models.CharField(max_length=55)),
                ('name_work', models.CharField(max_length=55)),
                ('writing_date', models.DateTimeField()),
                ('example', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student_work.example')),
                ('sсhol_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='school_class', to='user.sсholclass')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teacher_trainer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='studentwork',
            name='student_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='type_works', to='student_work.typestudentwork'),
        ),
    ]
