from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer
from .models import Post
from accounts.models import UserProfile
from accounts.permissions import IsAbleToSeeFullProfile
from django.contrib.auth.models import User

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAbleToSeeFullProfile])
def mainPostListView(request, username):
    if request.method == 'GET':
        queryset = Post.objects.filter(user__username=username)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)
