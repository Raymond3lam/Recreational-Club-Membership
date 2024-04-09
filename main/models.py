from django.db import models
from django.contrib.auth.models import User

class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    practices = models.ManyToManyField('Practice') 
    def __str__(self):
        return self.user.username


class Practice(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    members = models.ManyToManyField(Member)
    
    def __str__(self):
        return self.name
    
# Create your models here.
class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title