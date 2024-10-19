from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from agent.models import Agent
from user_profile.models import Profile
from user_admin.models import UserExtended,Notification
from .models import AgnetBalance

from datetime import datetime

def user_type(request):
    if request.user.is_authenticated:
        if Agent.objects.filter(user=request.user).exists():
            print('agent')
            return {'usertype': 'agent'}
        else:
            print('user')
            return {'usertype': 'user'}
    else:
        return {'usertype': 'anonymous'}

def user_profile(request):
    if request.user.is_authenticated:
        if Agent.objects.filter(user=request.user).exists():
            
            profile = Agent.objects.get(user=request.user)
            agent_balance = AgnetBalance.objects.get(agent=profile.user)
            print(profile.address)
            return {'profile': profile,'agent_balance':agent_balance}

        elif Profile.objects.filter(user=request.user).exists():

            profile = Profile.objects.get(user=request.user)
            return {'profile': profile}
        else:
            return {'usertype': 'admin'}
    else:
        return {'usertype': 'anonymous'}

def profile_admin(request):
    if request.user.is_authenticated:
        if UserExtended.objects.filter(user=request.user).exists():
            photo_admin = UserExtended.objects.get(user=request.user)
            return {'profile_admin': photo_admin}

    return ''

def get_notification(request):
    notification_list = Notification.objects.filter(duration__gte=datetime.now())
    notification_count = len(notification_list)
    context ={
        'notification_object':{
            'notification_list':notification_list,

            'notification_count':notification_count,
        }
       
    }
    return context	