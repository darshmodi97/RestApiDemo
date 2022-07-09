from rest_framework import serializers

from account.serializers import UserSerializer
from article.models import Article


class ShowArticleSerializer(serializers.HyperlinkedModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(view_name='article-detail', lookup_field='pk')

    class Meta:
        model = Article
        fields = ('id', 'title', 'detail_url')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        depth = 1
