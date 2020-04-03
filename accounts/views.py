from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import UserProfileSerializer
from .models import UserProfile
from .permissions import IsAbleToSeeFullProfile


@api_view()
def registrationCompleteView(request):
    return Response("Email account is activated.")

@api_view(['GET'])
def userProfileView(request, username):
    try:
        userProfile = UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer = UserProfileSerializer(userProfile)

        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAbleToSeeFullProfile])
def profileFollowersView(request, username):
    if request.method == 'GET':
        userProfile = UserProfile.objects.get(user__username=username)
        queryset = UserProfile.objects.filter(user__in=userProfile.followers.all())
        return Response(UserProfileSerializer(queryset, many=True).data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAbleToSeeFullProfile])
def profileFollowingView(request, username):
    if request.method == 'GET':
        userProfile = UserProfile.objects.get(user__username=username)
        queryset = UserProfile.objects.filter(user__in=userProfile.following.all())
        return Response(UserProfileSerializer(queryset, many=True).data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)
