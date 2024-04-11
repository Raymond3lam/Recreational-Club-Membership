from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.dispatch import receiver
from django.db.models.signals import post_save

class CustomUser(AbstractUser):
    practices = models.ManyToManyField('Practice', related_name='user_practices')
    phone_number = models.CharField(max_length=15, null=True)
    address = models.TextField(null=True)
    paid = models.BooleanField(default=False)

class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    practice = models.ForeignKey('Practice', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'date', 'practice')
        
class Practice(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    coach = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser, related_name='member_practices')
    
    def __str__(self):
        return self.name


# Create your models here.
class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created and isinstance(instance, CustomUser):
        members_group, created = Group.objects.get_or_create(name='Members')
        instance.groups.add(members_group)