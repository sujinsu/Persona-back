from rest_framework import serializers
from django.contrib.auth import get_user_model
# from guilds.serializers import GuildSerializer


from guilds.serializers import GuildSerializer

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # my_guilds = GuildSerializer(many=True,read_only=True,required=False)
    class Meta:
        model= get_user_model()

        fields = ('id','username','nickname','password','image','profile_content','is_superuser')

