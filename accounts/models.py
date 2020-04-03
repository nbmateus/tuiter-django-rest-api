from django.db import models
from django.contrib.auth.models import User
from postings.models import Post

class UserProfile(models.Model):
    user                = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    fullname            = models.CharField(max_length=30, blank=True)
    description         = models.CharField(max_length=200, blank=True)
    profilePicture      = models.ImageField(blank=True)
    birthdate           = models.DateField(blank=True, null=True)
    followers           = models.ManyToManyField(User, related_name='following', blank=True)
    following           = models.ManyToManyField(User, related_name='followers', blank=True)
    isPrivate            = models.BooleanField(default=False)
    postsLiked          = models.ManyToManyField(Post, related_name='likedby', blank=True)
    postsShared         = models.ManyToManyField(Post, related_name='sharedby', blank=True)

    def __str__(self):
        return self.fullname