from rest_framework.permissions import BasePermission
from .models import UserProfile

class IsAbleToSeeFullProfile(BasePermission):
    message = "This profile is private and its owner doesn't follow you."
    def has_permission(self, request, view):
        try:
            userProfile = UserProfile.objects.get(user__username=view.kwargs.get('username'))
        except UserProfile.DoesNotExist:
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