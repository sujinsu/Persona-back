from .models import BalanceGame
from rest_framework import serializers

class BalanceGameSerializer(serializers.ModelSerializer):

    class Meta:
        model=BalanceGame
        fields='__all__'
