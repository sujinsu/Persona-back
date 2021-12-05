from rest_framework import serializers
from .models import Guild,GuildArticle,GuildUser,GuildSignup,GuildTag,GuildArticleCount,AritcleLike



class AritcleLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AritcleLike
        fields ='__all__'

class GuildArticleCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuildArticleCount
        fields = '__all__' 
class GuildSerializer(serializers.ModelSerializer):
    # users = serializers.PrimaryKeyRelatedField(read_only=True)
    # tags = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Guild
        # fields = '__all__'
        fields = ('id','name','guild_image','profile_content','created_at','is_open',)

class GuildUserSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = GuildUser
        fields = '__all__'      


class GuildTagSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = GuildTag
        fields = '__all__'

class GuildArticleSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = GuildArticle
        # fields = ('img','content','user',)
        fields = '__all__'

class GuildSignupSerializer(serializers.ModelSerializer):
    state = serializers.BooleanField(default=True,read_only=True)
    class Meta:
        model = GuildSignup
        fields = '__all__' 