from django.db import models
import ckeditor
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class About(models.Model):

    about_text = RichTextUploadingField()
 

class Marketing(models.Model):
    market_text = RichTextUploadingField()

class TermsCondition(models.Model):
    condition_text = RichTextUploadingField()
   
class Question(models.Model):
    add_question = models.CharField(max_length=300,null=True,blank=True)
    question_details = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.add_question
class Package(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    discount = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    message =models.TextField(max_length=500,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class CompanyAddress(models.Model):
    address = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.phone

class navbarSupportedContent(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True)
    body = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.title

class UserDashboardContent(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True)
   

    def __str__(self):
        return self.title
