from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers
from api.models import Author, Article


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'picture']


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'author', 'category', 'title', 'summary']

    def to_representation(self, instance):
        representation = super(
            ArticleSerializer, self).to_representation(instance)
        representation['author'] = AuthorSerializer(instance.author).data
        return representation


class ArticleDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'author', 'category', 'title',
                  'summary', 'firstParagraph', 'body']

    def __init__(self, *args, **kwargs):
        anonymous_user = kwargs.get('context', {}).get('anonymous_user', None)
        if anonymous_user:
            self.fields.pop('body')

        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        representation = super(ArticleDetailsSerializer,
                               self).to_representation(instance)
        representation['author'] = AuthorSerializer(instance.author).data
        return representation
