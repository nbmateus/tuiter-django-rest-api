from rest_framework.permissions import BasePermission
from accounts.models import UserProfile
from .models import Post

class IsAbleToSeeThePost(BasePermission):
    message = "This post belongs to a private profile and its owner doesn't follow you."
    def has_permission(self, request, view):
        try:
            post = Post.objects.get(pk=view.kwargs.get('postId'))
            userProfile = UserProfile.objects.get(user=post.user)
        except Post.DoesNotExist:
            return True

        permission = True
        if userProfile.isPrivate:
            if request.user.is_authenticated:
                if userProfile.user != request.user:
                    authenticatedUSerProfile = UserProfile.objects.get(user__username=request.user.username) 
                    permission = authenticatedUSerProfile.followers.filter(username=userProfile.user).exists()

            else:
                permission = False
                
        return permission