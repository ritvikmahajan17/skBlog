from rest_framework import serializers
from .models import post


class PostSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField("get_username")
    likes = serializers.SerializerMethodField('get_likes')
    likes_list = serializers.SerializerMethodField('get_likes_list')

    class Meta:
        model = post
        fields = ['title', 'type', 'content',
                  'img', 'date_posted', 'username', 'likes', 'likes_list']

    def get_username(self, blog_post):
        username = blog_post.author.username
        return username

    def get_likes(self, blog_post):
        likes = blog_post.likes.count()
        return likes

    def get_likes_list(self, blog_post):
        like_list = blog_post.likes.all().values_list('username', flat=True)
        return like_list
