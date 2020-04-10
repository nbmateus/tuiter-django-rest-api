from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import UserProfileSerializer
from .models import UserProfile
from .permissions import IsAbleToSeeFullProfile
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView


@api_view()
def registrationCompleteView(request):
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def userProfileView(request, username):
    try:
        userProfile = UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer = UserProfileSerializer(userProfile, context={'request':request})
        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAbleToSeeFullProfile])
def profileFollowerListView(request, username):
    try:
        userProfile = UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        followers = UserProfile.objects.filter(user__in=userProfile.followers.all())
        result_page = paginator.paginate_queryset(followers, request)
        serializer = UserProfileSerializer(result_page, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAbleToSeeFullProfile])
def profileFollowingListView(request, username):
    try:
        userProfile = UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        following = UserProfile.objects.filter(user__in=userProfile.following.all())
        result_page = paginator.paginate_queryset(following, request)
        serializer = UserProfileSerializer(result_page, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST','DELETE'])
@csrf_exempt
@permission_classes([IsAuthenticated ,IsAbleToSeeFullProfile])
def doFollowOrUnfollowView(request, username):
    try:
        userProfileToBeFollowed = UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    followerUserProfile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST' and not request.user in userProfileToBeFollowed.followers.all() and request.user != userProfileToBeFollowed.user:
        userProfileToBeFollowed.followers.add(request.user)
        followerUserProfile.following.add(userProfileToBeFollowed.user)
        userProfileToBeFollowed.save()
        followerUserProfile.save()
        return Response(status=status.HTTP_200_OK)
        
    
    if request.method == 'DELETE' and request.user in userProfileToBeFollowed.followers.all():
        userProfileToBeFollowed.followers.remove(request.user)
        followerUserProfile.following.remove(userProfileToBeFollowed.user)
        userProfileToBeFollowed.save()
        followerUserProfile.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT',])
@permission_classes([IsAuthenticated])
def updateProfile(request, username):
    try:
        userProfile = UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method=='PUT' and request.user == userProfile.user:
        serializer = UserProfileSerializer(userProfile, data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def userProfileListView(request):
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        userProfileList = UserProfile.objects.all()
        result_page = paginator.paginate_queryset(userProfileList, request)
        serializer = UserProfileSerializer(result_page, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileListView(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter,]
    search_fields = ['user__username','fullname']

