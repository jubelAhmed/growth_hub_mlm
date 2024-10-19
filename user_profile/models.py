import agent.models
from .utils import create_new_ref_number
from django.db import models
from django.contrib.auth.models import User
from agent.models import Agent
from django.db import connection
from django.db.models import Func


USER_STATUS_CHOICES = [
    ("NEW_USER", "new"),
    ("ON_HOLD", "hold"),
    ("TOP_HUNDRED", 'tophundred'),
    ("WINNER", 'winner'),
   
]

USER_POSITION_CHOICES = [
    ("ACTIVE", "Active"),
    ("DEACTIVE", "Deactive"),
    ("OFFER_SHOWABLE", 'Offer_Showable'),
    ("TODAY_WINNER", 'Today_Winner')
]

class Sponsor(models.Model):
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="sponsor")
    reg_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="reguser")
    
    def __str__(self):
        return self.reg_user.username

class Package(models.Model):
    package_name = models.CharField(max_length=200,default='Primary',unique=True)
    package_amount = models.FloatField(default=0)
    display_package_name = models.CharField(max_length=200,default='Primary')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=300,null=True,blank=True)
    def __str__(self):
        return self.package_name
        
class UsePositionStatus(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    status_id = models.CharField(max_length=250,unique=True)
    def __str__(self):
        return self.name
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True, blank=True)
    #user_id = models.CharField(max_length=250,unique=True)
    full_name= models.CharField(max_length=200,null=True,blank=True)
    address = models.TextField(max_length=300,null=True,blank=True)
    country = models.CharField(max_length=200,null=True,blank=True)
    division = models.CharField(max_length=200,null=True,blank=True)
    district = models.CharField(max_length=200,null=True,blank=True)
    thana = models.CharField(max_length=200,null=True,blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d',null=True,blank=True, default="../static/profile.jpg")
    #password 
    mobile_no = models.CharField(max_length=20,null=True,blank=True)
    tnx_no =  models.CharField(max_length = 10,null=True,blank=True)    
    package_id = models.ForeignKey(Package, on_delete=models.CASCADE)
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True, related_name="profile_sponsor")
    agent = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True, related_name="profile_agent")
    user_position_status = models.CharField(max_length=25, choices=USER_POSITION_CHOICES, default="Active")
    status = models.BooleanField(default=True)
    birth_date = models.DateTimeField(null=True,blank=True)

    current_wallet = models.FloatField(default=0)
    registration_wallet = models.FloatField(default=0)
    sponsor_wallet = models.FloatField(default=0)
    founder_wallet = models.FloatField(default=0)

    # Some Update: Himel
    user_current_status = models.CharField(max_length=11, choices=USER_STATUS_CHOICES, default="NEW_USER")

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.full_name
    @property
    def sponsor_count(self):
        count = 0;
        for obj in Profile.objects.all() :
            if obj.sponsor == self.user:
                count +=1
        
        return count
        
    def my_custom_sql(self):
        with connection.cursor() as cursor:
            
            cursor.execute("""
			WITH RECURSIVE hierarchy AS (
				SELECT t.id,
						t.user_id,
						t.full_name,
						t.sponsor_id,
                        t.created_date
					FROM user_profile_profile t
				WHERE t.sponsor_id = %s
				UNION ALL
				SELECT x.id,
						x.user_id,
						x.full_name,
						x.sponsor_id,
                        x.created_date

					FROM user_profile_profile x
					JOIN hierarchy y ON y.user_id = x.sponsor_id
				)
				SELECT *
				FROM hierarchy ORDER BY created_date ASC
            """,[self.user.id])
           

            row = dictfetchall(cursor)

        return row

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()