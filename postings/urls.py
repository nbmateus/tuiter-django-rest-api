from django.urls import path
from .views import  mainPostListView, likedPostsListView, doLikeOrUnlike, commentsListView, createPost, postDetail, indexMainPostListView

urlpatterns = [
    path('main-post-list/<str:username>/', mainPostListView, name='main_post_list'),
    path('liked-post-list/<str:username>/', likedPostsListView, name='liked_post_list'),
    path('do-like-or-unlike/<int:postId>/', doLikeOrUnlike, name='like_or_unlike'),
    path('comment-list/<int:postId>/',commentsListView, name='comment_list'),
    path('create-post/',createPost, name='create_post'),
    path('post-detail/<int:postId>/',postDetail, name='post_detail'),
    path('main-post-list/', indexMainPostListView, name='index_mainpost_list'),
]