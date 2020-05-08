from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='postsImages/', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='likedPosts', blank=True)
    shared = models.ManyToManyField(User, related_name='sharedPosts', blank=True)
    mainPost = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name='comments')# Equals to null if self it's a main post. Instance of Post if self it's a commentary.
    rePost = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name='retuits')#Instance of Post if self it's a rePost.

    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return self.text
                