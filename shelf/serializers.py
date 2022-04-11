from rest_framework import serializers

from .models import Author
from .models import Book


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150, required=True)
    country = serializers.CharField(
        max_length=100,
        required=False,
        allow_null=True,
        allow_blank=True
    )

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.country = validated_data.get('country', instance.country)
        instance.save()

        return instance

    def create(self, validated_data):
        return Author.objects.create(**validated_data)


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150, required=True)
    annotation = serializers.CharField(max_length=1500, required=False)
    circulation = serializers.IntegerField(
        required=False,
        allow_null=True
    )
    published = serializers.IntegerField(
        required=False,
        allow_null=True
    )

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.annotation = validated_data.get('annotation', instance.annotation)
        instance.circulation = validated_data.get('circulation', instance.circulation)
        instance.published = validated_data.get('published', instance.published)
        instance.save()

        return instance

    def create(self, validated_data):
        return Book.objects.create(**validated_data)
