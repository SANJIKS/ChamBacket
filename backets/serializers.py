from .models import Backet
from rest_framework import serializers

class BackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backet
        fields = '__all__'
        read_only_fields = ('id',)