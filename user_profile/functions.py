from django.contrib.auth.models import User
from .models import Sponsor, Profile
import re
from user_admin.models import Notification
from datetime import datetime

#  Sponsor validation
def validateSponsorID(sponsorname):
    # Return true when no sponsor
    if sponsorname == '':
        return True
    # Sponsor is exists
    if User.objects.filter(username=sponsorname).exists():
        # Getting user object
        selectedSponsor = User.objects.get(username=sponsorname)
        # if it is User can be a sponsor
        if Profile.objects.filter(user=selectedSponsor).exists():
            # A user can be maximum of 3 other user sponsor
            total_sponsors = Sponsor.objects.filter(sponsor=selectedSponsor).count()
            if total_sponsors < 3:
                
                return True
            else:
                # Selected user has more than 3 sponsor
                return False
        else:
            # Agent can't be a sponsor
            return False
    else:
        # User does not exitsts! Wrong sponsor name
        return False

#  Email address validation
def emailValidator(email):
    # Regex fo validating email
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if(re.search(regex,email)):  
        if User.objects.filter(email=email).exists():
            # Email Already Exists
            return False
        else:
            return True
    else:  
        # Email not valid
        return False

#  Password strength check
def password_check(passwd): 
      
    SpecialSym =['$', '@', '#', '%'] 
    val = True
      
    if len(passwd) < 8: 
        # print('length should be at least 6') 
        val = False
          
    if len(passwd) > 20: 
        # print('length should be not be greater than 19') 
        val = False
          
    if not any(char.isdigit() for char in passwd): 
        # print('Password should have at least one numeral') 
        val = False
          
    # if not any(char.isupper() for char in passwd): 
    #     # print('Password should have at least one uppercase letter') 
    #     val = False
          
    if not any(char.islower() for char in passwd): 
        # print('Password should have at least one lowercase letter') 
        val = False
          
    # if not any(char in SpecialSym for char in passwd): 
    #     # print('Password should have at least one of the symbols $@#') 
    #     val = False
    if val: 
        return val 

def is_top_hundered(name):
    totalTopHundred = Profile.objects.filter(user_current_status='TOP_HUNDRED').count()
    print("Total totalTopHundred Count ======================= " + str(totalTopHundred))
    if totalTopHundred < 100:
        return True
    else:
        return False

def is_total_two_sponsor(name):
    sponsorUser = User.objects.get(username=name)
    count = Sponsor.objects.filter(sponsor=sponsorUser).count()
    print("Total Sponsor Count ======================= " + str(count))
    if count == 2:
        return True
    else:
        return False


    
def get_notification(request):
    notification_list = Notification.objects.filter(duration__gte=datetime.now())
    notification_count = len(notification_list)
    context ={
        'notification_list':notification_list,
        'notification_count':notification_count,
    }
    return context	

def get_percentage(main_number,percentage) : 
    return (main_number*percentage)/100
