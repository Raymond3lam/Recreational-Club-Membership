from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title