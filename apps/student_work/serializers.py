from rest_framework import serializers
from apps.student_work.models import StudentWork


class StudentWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentWork
        fields = '__all__'
