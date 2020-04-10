from django.urls import path
from .views import  (
    mainPostListView, likedPostsListView, doLikeOrUnlike,
    commentsListView, createPost, postDetail, indexMainPostListView,
    usersThatLikedView, usersThatSharedView

)

urlpatterns = [
    path('create-post/',createPost, name='create_post'),
    path('post-detail/<int:postId>/',postDetail, name='post_detail'),
    path('post-detail/<int:postId>/like/', doLikeOrUnlike, name='like_or_unlike'),
    path('post-detail/<int:postId>/users-that-liked/',usersThatLikedView, name='post_likes_detail'),
    path('post-detail/<int:postId>/users-that-shared/',usersThatSharedView, name='post_shared_detail'),
    path('post-detail/<int:postId>/comments/',commentsListView, name='comment_list'),
    path('index-main-post-list/', indexMainPostListView, name='main_post_list'),
    path('main-post-list/<str:username>/', mainPostListView, name='main_post_list'),
    path('liked-post-list/<str:username>/', likedPostsListView, name='liked_post_list'),
    

    
    
    
]