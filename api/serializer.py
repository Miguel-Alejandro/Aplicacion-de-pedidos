from rest_framework import serializers
from .models import hoyRX, item

class hoyRXSerializer(serializers.ModelSerializer):
    class Meta:
        model = hoyRX
        fields = '__all__'


class itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = item
        fields = '__all__'