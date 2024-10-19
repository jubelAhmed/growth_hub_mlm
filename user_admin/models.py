from user_profile.models import Profile
from agent.models import Agent
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import DateTimeField
import datetime
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth import get_user_model
from user_profile.models import Package
# Create your models here.
USER_STATUS_CHOICES = [
    ("ALL_MEMBER", "all_member"),
    ("AGENT", "agent"),
    ("MEMBERS", 'members'),
    ("WINNER", 'winner')
]
class Notification(models.Model): 
    member_type = models.CharField(max_length=20, choices=USER_STATUS_CHOICES, default="all_member")
    created_at = models.DateTimeField(auto_now_add=True)
    #created_at.editable=True
    updated_at = models.DateTimeField(auto_now=True)
    #updated_at.editable=True
    duration = models.DateField(null=True)
    title= models.CharField(max_length=200,null=True,blank=True)
    slug = models.SlugField(max_length=100,unique=True, null=True, blank=True)
    body = models.TextField(max_length=300,null=True,blank=True)
    status = models.BooleanField(default=True)
    class Meta:
        ordering=['-created_at']
        verbose_name = 'Notification'   
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('notification_update',kwargs={ 'slug': self.slug})


        
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Notification.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug
    
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    pre_save.connect(pre_save_post_receiver, Notification)

class PackageBalance(models.Model):
    package = models.OneToOneField(Package,on_delete=models.CASCADE,related_name="package",
        primary_key=True)
    profit_percentage = models.FloatField(default=2.5)
    sponsor_percentage = models.FloatField(default=15.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.package.package_name

class UserExtended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d',null=True,blank=True, default="../static/profile.jpg")
      
        
    def __str__(self):
        return f'{self.user}'