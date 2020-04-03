from django.urls import path
from .views import  mainPostListView

urlpatterns = [
    path('mainpostslist/<str:username>/', mainPostListView),
    
    
]