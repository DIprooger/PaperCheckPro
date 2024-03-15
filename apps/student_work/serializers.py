from rest_framework import serializers
from apps.student_work.models import (
    StudentWork,
    Example,

)


class StudentWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentWork
        fields = '__all__'


class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = '__all__'
