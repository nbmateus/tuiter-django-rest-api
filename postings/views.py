from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer
from .models import Post
from accounts.models import UserProfile
from accounts.permissions import IsAbleToSeeFullProfile
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAbleToSeeThePost
from rest_framework.pagination import PageNumberPagination
from accounts.serializers import UserProfileSerializer
from django.db.models import Q

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAbleToSeeFullProfile])
def mainPostListView(request, username):
    try:
        userProfile = UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        mainPostList = Post.objects.filter(user__username=username, mainPost=None).order_by('-timestamp')
        result_page = paginator.paginate_queryset(mainPostList, request)
        serializer = PostSerializer(result_page, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAbleToSeeFullProfile])
def likedPostsListView(request, username):
    try:
        userProfile = UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        userProfile = UserProfile.objects.get(user__username=username)
        result_page = paginator.paginate_queryset(userProfile.postsLiked.all().order_by('-timestamp'), request)
        serializer = PostSerializer(result_page, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST','DELETE'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def doLikeOrUnlike(request, postId):
    try:
        post = Post.objects.get(pk=postId)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    userProfile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        if not request.user in post.likes.all():
            post.likes.add(request.user)
            userProfile.postsLiked.add(post)
            post.save()
            userProfile.save()
            return Response(status=status.HTTP_200_OK)  

    if request.method == 'DELETE':
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            userProfile.postsLiked.remove(post)
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAbleToSeeThePost])
def commentsListView(request, postId):
    try:
        mainPost = Post.objects.get(pk=postId)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        comments = Post.objects.filter(mainPost=mainPost).order_by('timestamp')
        result_page = paginator.paginate_queryset(comments, request)
        serializer = PostSerializer(result_page, many=True, context={'request':request})
        return paginator.get_paginated_response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
@csrf_exempt
def createPost(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            rePostId = serializer.data.get('rePost')
            if rePostId is not None:
                sharedPost = Post.objects.get(pk=rePostId)
                sharedPost.shared.add(request.user)
                sharedPost.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','DELETE'])
@csrf_exempt
@permission_classes([IsAbleToSeeThePost,])
def postDetail(request, postId):
    try:
        post = Post.objects.get(pk=postId)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post, context={'request':request})
        return Response(serializer.data)

    if request.method == 'DELETE':
        if request.user.is_authenticated and request.user == post.user:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def indexMainPostListView(request):
    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10

        userProfile = UserProfile.objects.get(user=request.user)
        mainPostList = Post.objects.filter(Q(user__in=userProfile.following.all(), mainPost=None) | Q(user=request.user, mainPost=None)).order_by('-timestamp')

        result_page = paginator.paginate_queryset(mainPostList, request)

        serializer = PostSerializer(result_page, many=True, context={'request':request})

        return paginator.get_paginated_response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAbleToSeeThePost])
def usersThatLikedView(request, postId):
    try:
        post = Post.objects.get(pk=postId)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10

        userProfileList = UserProfile.objects.filter(user__in=post.likes.all())

        result_page = paginator.paginate_queryset(userProfileList, request)

        serializer = UserProfileSerializer(result_page, many=True, context={'request':request})

        return paginator.get_paginated_response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAbleToSeeThePost])
def usersThatSharedView(request, postId):
    try:
        post = Post.objects.get(pk=postId)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        paginator = PageNumberPagination()
        paginator.page_size = 10

        userProfileList = UserProfile.objects.filter(user__in=post.shared.all())

        result_page = paginator.paginate_queryset(userProfileList, request)

        serializer = UserProfileSerializer(result_page, many=True, context={'request':request})

        return paginator.get_paginated_response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
@permission_classes([IsAuthenticated])
def didILikePost(request, postId):
    if request.method == 'GET':
        try:
            post = Post.objects.get(pk=postId)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
  
        return Response({"didILikePost":request.user in post.likes.all()})
        
    return Response(status=status.HTTP_400_BAD_REQUEST)