from rest_framework import serializers
from .models import Ad, Review


class ReviewSerializer(serializers.ModelSerializer):
    author_email = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'author_email', 'ad', 'created_at']
        read_only_fields = ['author', 'created_at']


class AdSerializer(serializers.ModelSerializer):
    author_email = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Ad
        fields = ['id', 'title', 'price', 'description', 'author', 'author_email', 'is_active', 'created_at']
        read_only_fields = ['author', 'created_at']


class AdDetailSerializer(AdSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta(AdSerializer.Meta):
        fields = AdSerializer.Meta.fields + ['reviews']