from rest_framework import serializers
from .models import UserProfile
from rest_auth.registration.serializers import RegisterSerializer

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
         'followersCount', 'followingCount']
    
    user = serializers.StringRelatedField(many=False)
    followersCount = serializers.SerializerMethodField()
    followingCount = serializers.SerializerMethodField()
    
    def get_followersCount(self, obj):
        return obj.followers.count()
    
    def get_followingCount(self, obj):
        return obj.following.count()

