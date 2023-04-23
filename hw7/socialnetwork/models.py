from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.CharField(max_length=200)
    creation_time = models.DateTimeField()

class Comment(models.Model):
    text = models.CharField(max_length=200)
    creation_time = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='creator')
    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='post')
    
class Profile(models.Model):
    bio = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50)
    following = models.ManyToManyField(User, related_name="followers")
