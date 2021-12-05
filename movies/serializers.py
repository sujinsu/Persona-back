from rest_framework import serializers
from .models import Collection, Movie, Review, Form, Tag
from accounts.serializers import UserSerializer


class MovieSerializer(serializers.ModelSerializer):
    like_users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = '__all__'


class MovieUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'overview', 'poster_path', 'release_date')


class ReviewSerializer(serializers.ModelSerializer):
    like_users = UserSerializer(read_only=True, many=True)
    
    class Meta:
        model = Review
        fields = '__all__'


class FormSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Form
        fields = '__all__' 


class CollectionSerializer(serializers.ModelSerializer):
    like_users = UserSerializer(read_only=True, many=True)
    movies = MovieSerializer(read_only=True, many=True)
    
    class Meta: 
        model = Collection
        fields = '__all__'


class CollectionUpdateSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Collection
        fields = ('title', 'content', 'movies')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'