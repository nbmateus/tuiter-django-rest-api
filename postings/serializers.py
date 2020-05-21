from rest_framework import serializers
from .models import Post
from rest_framework.reverse import reverse

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','user','timestamp','text','image','likesCount','sharedCount', 'commentsCount', 'mainPost', 'rePost', 'comments', 'usersThatLiked','usersThatShared']

    user = serializers.StringRelatedField(many=False)
    likesCount = serializers.SerializerMethodField()
    sharedCount = serializers.SerializerMethodField()
    commentsCount = serializers.SerializerMethodField()
    mainPost = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False, allow_null=True, default=None)
    rePost = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False, allow_null=True, default=None)
    comments = serializers.SerializerMethodField()
    usersThatLiked = serializers.SerializerMethodField()
    usersThatShared = serializers.SerializerMethodField()

    def get_likesCount(self, obj):
        return obj.likes.count()
    
    def get_sharedCount(self, obj):
        return Post.objects.filter(rePost=obj).count()
    
    def get_commentsCount(self, obj):
        return Post.objects.filter(mainPost=obj).count()
    
    def get_comments(self, obj):
        return reverse('comment_list', args=[obj.id], request=self.context['request'])
    
    def get_usersThatLiked(self, obj):
        return reverse('post_likes_detail', args=[obj.id], request=self.context['request'])
    
    def get_usersThatShared(self, obj):
        return reverse('post_shared_detail', args=[obj.id], request=self.context['request'])

    