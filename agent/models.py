import user_profile.models 
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200,null=True,blank=True)
    address = models.TextField(max_length=300,null=True,blank=True)
    country = models.CharField(max_length=200,null=True,blank=True)
    photo = models.ImageField(upload_to='agent_photos/%Y/%m/%d',  default="../static/profile.jpg")
    #password
    mobile_no = models.CharField(max_length=200,null=True,blank=True)
    tnx_no  =  models.IntegerField(default=0)      
    division = models.CharField(max_length=200,null=True,blank=True)
    district = models.CharField(max_length=200,null=True,blank=True)
    thana = models.CharField(max_length=200,null=True,blank=True)
    #BTCAddress = models.CharField(max_length=200,unique=True,default='')
    transaction_id = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    birth_date = models.DateTimeField(default=0,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

