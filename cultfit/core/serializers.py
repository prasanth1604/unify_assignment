from rest_framework import serializers
from .models import FitnessClass
class RegisterClientSerializer(serializers.Serializer):
    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'time', 'Instructor', 'total_slots', 'registered_clients']