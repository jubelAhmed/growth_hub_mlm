
from account.context import user_type
from user_profile.models import Package, Profile, Sponsor
from organization.models import CompanyAddress, Contact
from agent.models import Agent
from user_admin.forms import  ContactForm
from django.shortcuts import  redirect, render
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.decorators import login_required
from user_admin.forms import AdminPhotoForm, EditAdminForm, NotificationForm, EditProfileForm
from datetime import datetime
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
"""contact list showing by the function.here all the contact info showing from the landing pages contact"""
def admin_contact(request):
    all_contact = Contact.objects.all().order_by('-created_at')
    
    context ={
      
       'all_contact':all_contact, 
    }
    return render(request,'admin/user_admin/contact_list.html',context)

#delete contact by admin
def delete_contact(request, pk):
	del_contact = Contact.objects.get(id=pk)
	if request.method == "POST":
		del_contact.delete()
		return redirect(reverse_lazy('admin_contact'))
	context = {
		'del_contact': del_contact,
	}
	return render(request, 'admin/user_admin/contact_list.html', context)

#view contact by the id in admin
def contact_view(request, id):
    contacts = Contact.objects.get(id=id)
    if request.method == "POST":
        contacts.delete()
        return redirect(reverse_lazy('admin_contact'))
    context ={
  
        'contacts':contacts,
        }
    return render(request, 'admin/user_admin/contact_view.html',context)

#here showing all agent  list in smadmin
def agent_user_list(request, pk):

    agent_details = Profile.objects.order_by('agent')
    #blog_list = Profile.objects.filter(agent__full_name='full_name')
    #user = User.objects.get(id=pk)
    agent = Agent.objects.get(id=pk)
    user_list = Profile.objects.filter(agent__username = agent.user.username)
    # if list is None:
    #     agent_list = Profile.objects.get()
    # else:
    #     agent_list = Profile.objects.filter(agent_details=list)
 
  

    
    context ={
        #'agent_list':agent_list,
        'agent_details':agent_details,
        'user_list':user_list,
    }
    return render(request,'admin/user_admin/agent_user_list.html',context)

#showing winner list in smadmin by winner status from profile
@login_required(login_url='/home/profile/login/')
def winner_List(request):
	winner_profiles = Profile.objects.filter(user_current_status='WINNER', status=True)
	
	context ={
		
		'winner_profiles':winner_profiles,
	}
	return render(request,'admin/member/winner_list.html',context)
#checking winner details and delte it
def winner_list_view(request, id):
    winner = Profile.objects.get(id=id)
    if request.method == "POST":
        winner.delete()
        return redirect(reverse_lazy('winner_List'))
    context ={
  
        'winner':winner,
        }
    return render(request, 'admin/member/winner_list_view.html',context)
#delete winner from the list pages
def delete_winner(request, pk):
	del_winner = Profile.objects.get(id=pk)
	if request.method == "POST":
		del_winner.delete()
		return redirect(reverse_lazy('winner_List'))
	context = {
		'del_winner': del_winner,
	}
	return render(request, 'admin/member/winner_list_view.html', context)