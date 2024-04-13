from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.dispatch import receiver
from django.db.models.signals import post_save

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        permissions = [
            ('manage_coaches', 'Can manage coaches'),
            ('manage_finances', 'Can manage finances')
        ]

    def payment_count(self):
        return self.payment_set.count()
    
    def practice_count(self):
        return self.member_practices.count()
    
class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    practice = models.ForeignKey('Practice', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'date', 'practice')
        
class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    paid = models.BooleanField(default=False)
    due = models.DateTimeField(default=timezone.now)
    notes = models.TextField()
    category = models.CharField(max_length=100)

class Practice(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    coach = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser, related_name='member_practices', blank=True)
    date = models.DateTimeField(default=None, blank=True, null=True)
    def __str__(self):
        return self.name
    
    def paid (self, user):
        return self.payment_set.filter(user=user).exists()

# Create your models here.
class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    target = models.ManyToManyField(CustomUser, related_name='targeted_users', blank=True)
    target_practices = models.ManyToManyField(Practice, related_name='targeted_practices', blank=True)

    def __str__(self):
        return self.title
    
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        treasurer_group, created = Group.objects.get_or_create(name='Treasurer')
        treasurer_group.permissions.add(Permission.objects.get(codename='manage_coaches'))
        treasurer_group.permissions.add(Permission.objects.get(codename='manage_finances'))
        treasurer_group.permissions.add(Permission.objects.get(codename='add_practice'))
        treasurer_group.permissions.add(Permission.objects.get(codename='view_customuser'))
        treasurer_group.permissions.add(Permission.objects.get(codename='add_announcement'))
        coach_group, created = Group.objects.get_or_create(name='Coach')
        coach_group.permissions.add(Permission.objects.get(codename='change_practice'))
        coach_group.permissions.add(Permission.objects.get(codename='add_announcement'))
        member_group, created = Group.objects.get_or_create(name='Member')
        member_group.permissions.add(Permission.objects.get(codename='add_payment'))
        instance.groups.add(member_group)