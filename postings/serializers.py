from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','user','timestamp','text','image','likesCount','sharedCount', 'mainPost', 'rePost']

    user = serializers.StringRelatedField(many=False)
    likesCount = serializers.SerializerMethodField()
    sharedCount = serializers.SerializerMethodField()
    mainPost = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False, allow_null=True, default=None)
    rePost = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False, allow_null=True, default=None)

    def get_likesCount(self, obj):
        return obj.likes.count()
    
    def get_sharedCount(self, obj):
        return obj.shared.count()