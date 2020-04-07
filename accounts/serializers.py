from rest_framework import serializers
from .models import UserProfile
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.reverse import reverse

class UserRegisterSerializer(RegisterSerializer):
    def save(self, request):
        user = super().save(request)
        userProfile = UserProfile(user=user, fullname=user.username)
        userProfile.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'fullname', 'description', 'profilePicture', 'isPrivate', 'birthdate',
         'followersCount', 'followingCount', 'followers', 'following', 'mainPostList', 'likedPostList']
    
    user = serializers.StringRelatedField(many=False, read_only=True)
    followersCount = serializers.SerializerMethodField()
    followingCount = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    mainPostList = serializers.SerializerMethodField()
    likedPostList = serializers.SerializerMethodField()
    
    def get_followersCount(self, obj):
        return obj.followers.count()
    
    def get_followingCount(self, obj):
        return obj.following.count()
    
    def get_followers(self, obj):
        return reverse('profile_follower_list',args=[obj.user.username] , request=self.context['request'], format=None)

    def get_following(self, obj):
        return reverse('profile_following_list',args=[obj.user.username] , request=self.context['request'], format=None)
    
    def get_mainPostList(self, obj):
        return reverse('main_post_list',args=[obj.user.username] , request=self.context['request'], format=None)
    
    def get_likedPostList(self, obj):
        return reverse('liked_post_list',args=[obj.user.username] , request=self.context['request'], format=None)

