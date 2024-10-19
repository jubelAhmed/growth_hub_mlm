from django.contrib.auth.forms import UserChangeForm
from user_admin.utils import create_new_ref_number
from django.core.checks import messages
from agent.models import Agent
from django.http import request
from user_profile.models import Package, Profile, Sponsor
from user_admin.forms import AdminPhotoForm, EditAdminForm, NotificationForm, EditProfileForm
from django.shortcuts import get_object_or_404, redirect, render
from user_profile.functions import validateSponsorID, password_check, emailValidator, is_top_hundered, is_total_two_sponsor,get_notification,get_percentage

from django.contrib.auth.models import User, UserManager
from .models import Notification, UserExtended
from django.db.models import Count  
from django.utils import timezone 
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from datetime import datetime
from django.urls import reverse_lazy
# Create your views here.	

#showing all notification list in smadmin and adding new notification by form
@login_required(login_url='/home/profile/login/')
def notification_list7(request):

	notification_all = Notification.objects.all()
	if request.method=='POST':
	
		form = NotificationForm(request.POST)
		if form.is_valid():
			ce = form.save(commit=False)
			ce.title = request.POST.get('title')
			ce.body = request.POST.get('body')
			ce.member_type = request.POST.get('member_type')
			ce.duration = request.POST.get('duration')
			ce.save()
			return redirect(reverse_lazy('notification_list7'))
		else:
			return render(request,'admin/notification/notification_list7.html')  
	else:
		form = NotificationForm
	context={
		
		'form':form,
		'notification_all':notification_all,
	}
	#context.update(notificaation_context)
	return render(request,'admin/notification/notification_list7.html',context)




# def notification_update(request,id):
# 	obj = get_object_or_404(Notification, id=id)
# 	form = UpdateForm(request.POST or None, instance=obj)
# 	if form.is_valid():
# 		form.save()
# 		return render(request, 'admin/notification/notification_update.html')
# 	context ={
# 		'form': form,
# 	}
# 	return render(request, 'admin/notification/notification_update.html',context)




# def notification_update(request,slug):
# 	obj = Notification.objects.filter(slug=slug)
	
# 	form = UpdateForm(request.POST)
# 	if request.method == 'POST':
# 		if form.is_valid():
# 			form.save()
# 			return render(request, 'admin/notification/notification_update.html',{'obj':obj,})
# 	else:
# 		form = UpdateForm

# 	return render(request, 'admin/notification/notification_update.html',{'form': form,'obj':obj,})
#updating notification 
@login_required(login_url='/home/profile/login/')
def notification_update(request, pk):
	(request)
	notification = Notification.objects.get(id=pk)
	print(notification)
	form = NotificationForm(instance=notification)

	if request.method == 'POST':
		form = NotificationForm(request.POST, instance=notification)
		if form.is_valid():
			form.save()
			return redirect(reverse_lazy('notification_list7'))

	context ={
		'form': form,
		'notification':notification,
		
	}

	return render(request, 'admin/notification/notification_update.html',context)
#deleting all notification by the id and redirect the list pages
@login_required(login_url='/home/profile/login/')
def delete_notification(request, pk):
	del_notification = Notification.objects.get(id=pk)
	if request.method == "POST":
		del_notification.delete()
		return redirect(reverse_lazy('notification_list7'))
	context = {
		'del_notification': del_notification,
	}
	return render(request, 'admin/notification/notification_list7.html', context)






#adding member in smadmin 	
@login_required(login_url='/home/profile/login/')
def add_member(request):
	#selected_package = None
	packages = Package.objects.all()

	 
	
	if request.method == "POST":
		username = request.POST.get('username')
		email = request.POST.get('email')
		password=request.POST.get('password')
		repassword = request.POST.get('password2')
		full_name = request.POST.get('full_name')
		address = request.POST.get('address')
		country = request.POST.get('country')			
		sponsor = request.POST.get('sponsor_id')
		pk_id = request.POST.get('package_name')
		mobile_no = request.POST.get('mobile_no')
		birth_date = request.POST.get('birth_date')
		"""#form_filed has used because if submit the form and in any case it failed then we want to keep data in the input filed so
		user don't have to fillup again the form"""	
		form_field = {
		"username" : username,
		"email" : email,
		"password" : password,
		"password2" : repassword,
		"full_name" : full_name,
		"address" : address,
		'country' : country,
		'sponsor_id' :  sponsor,
		'package_name' : pk_id,
		'mobile_no' : mobile_no,
		'birth_date' : birth_date
			}

		#profile_form = UserProfileForm(request.POST)
		if request.POST['username'] and request.POST['password'] == request.POST['password2']:
    	


			if User.objects.filter(username=request.POST['username']).exists():
				return render(request, 'admin/member/add_member.html',{ 'packages': packages,'form_field':form_field, 'error': "username has already taken"})
			else:
				 
				username = request.POST.get('username')
				email = request.POST.get('email')

				password=request.POST.get('password')
				repassword = request.POST.get('password2')

				full_name = request.POST.get('full_name')
				address = request.POST.get('address')
				country = request.POST.get('country')
				tnx_no = create_new_ref_number()  
				 
				sponsor = request.POST.get('sponsor_id')

				pk_id = request.POST.get('package_name')
				package_id =Package.objects.get(id=pk_id)
			 

				mobile_no = request.POST.get('mobile_no')
				birth_date = request.POST.get('birth_date')

				# AgentProfile = Agent.objects.get(user=request.user)
				
				if emailValidator(email):
					if password_check(password):
						user = User.objects.create_user(username=username, password=password, email=email)
						user.save()

						SponsorUser = User.objects.get(username=sponsor) if sponsor else ''
							
						SponsorProfile = Profile.objects.get(user=SponsorUser) if SponsorUser else ''
						# sponsor getting percentage registering by  sposnor id
						if SponsorProfile:
							SponsorProfile.current_wallet = SponsorProfile.current_wallet + get_percentage(package_id.package_amount,15)
							SponsorProfile.sponsor_wallet = SponsorProfile.sponsor_wallet + get_percentage(package_id.package_amount,15)
							SponsorProfile.save()

						# Now create user profile
						newprofile = Profile()
						newprofile.user = user
						newprofile.full_name = full_name
						newprofile.address = address
						newprofile.tnx_no = tnx_no
						newprofile.country = country
						newprofile.mobile_no = mobile_no
						# newprofile.agent = request.user
						if SponsorUser:
							newprofile.sponsor = SponsorUser

						newprofile.package_id = package_id

						newprofile.registration_wallet = package_id.package_amount if package_id else 0

						newprofile.current_wallet = package_id.package_amount if package_id else 0

						try:
							newprofile.save()
						except e :
							print(e)

						# Changing Sponsor Profile Setting
						if sponsor and is_total_two_sponsor(sponsor):
							if is_top_hundered(sponsor):
								SponsorProfile.user_current_status = 'TOP_HUNDRED'
								SponsorProfile.save()
							else:
								SponsorProfile.user_current_status = 'ON_HOLD'
								SponsorProfile.save()
						# Now add data to sponsors table
						getSponsorUser = User.objects.get(username=sponsor) if sponsor else ''

						newSponsor = Sponsor()
						if getSponsorUser:
							newSponsor.sponsor = getSponsorUser 
						newSponsor.reg_user = user
						newSponsor.save()
						return render(request, 'admin/member/add_member.html',{'packages': packages,'package': package_id.package_name, 'accountCreated': "Account Created!", 'user_name': username, 'pass': password, 'sponsor': SponsorProfile.full_name if SponsorProfile else ''})
					else:
						return render(request, 'admin/member/add_member.html',{'packages': packages, 'form_field':form_field,  'error': "Password is not strong enough you can use generator!"})
				else:
					return render(request, 'admin/member/add_member.html',{'packages': packages, 'form_field':form_field, 'error': "Another user already using this email or this email is not given or valid!"})

		else:
			
			return render(request, 'admin/member/add_member.html', {'packages': packages,'form_field':form_field, 'error': "You must fill up all input currectly!"})
	
	
	else:
		return render(request, 'admin/member/add_member.html', {'packages': packages})


@login_required(login_url='/home/profile/login/')
def add_member1(request):
	#selected_package = None
	package_id = Package.objects.all()
	
	if request.method == "POST":
		#profile_form = UserProfileForm(request.POST)
		if request.POST['password'] == request.POST['password2']:
			try:
				user = User.objects.get(username=request.POST['username'])
				return render(request, 'admin/member/add_member.html',{'error': "username has already taken"})
			except User.DoesNotExist:
				user = User.objects.create_user(username = request.POST['username'],email = request.POST['email'],password=request.POST['password'])
				full_name = request.POST.get('full_name')
				address = request.POST.get('address')
				country = request.POST.get('country')
				tnx_no = create_new_ref_number() #request.POST.get('tnx_no')
				#agent_id =Agent.objects.get(id=2) #request.POST.get('agent_id')
				#package_id =Package.objects.get(id)
				user_current_status =request.POST.get('user_current_status')
				pk_id = request.POST.get('package_name')
				package_id =Package.objects.get(id=pk_id)
				print(user_current_status)

				mobile_no = request.POST.get('mobile_no')
				#birth_date = request.POST.get('birth_date')
				profile = Profile(full_name=full_name,user_current_status=user_current_status,package_id =package_id,tnx_no=tnx_no,address=address,country=country,mobile_no=mobile_no, user=user)
				
				profile.save()
				
			
				#auth.login(request,user)
				#return render(request, 'users/user_profile/signup.html')
				return redirect(reverse_lazy('new_member'))

		else:
			return render(request, 'admin/member/add_member.html')
	
	
	else:
		#return render(request, 'users/user_profile/signup.html')
		
		context ={
			     #'selected_package':selected_package,
				 'package_id': package_id,
					}
		return render(request, 'admin/member/add_member.html',context)
#new member list
@login_required(login_url='/home/profile/login/')
def new_member(request):
	new_profile = Profile.objects.filter(user_current_status='NEW_USER',status=True).order_by('-updated_date')
	context={
		'new_profile':new_profile,
	}
	return render(request, 'admin/member/new_member.html',context)
#hide member from smadmin by partial delte using js
@login_required(login_url='/home/profile/login/')
def hide_new(request,pk):
	membernew_all = Profile.objects.get(id=pk)
	if request.method == "POST":
		del_new_member = request.POST.get('del_new_member')
		if del_new_member == "partial":
			if membernew_all.status == True:
				membernew_all.status = False
				membernew_all.save()
		elif del_new_member == "permanent":
			membernew_all.delete()
	return redirect(reverse_lazy('new_member'))



#hold line list 
@login_required(login_url='/home/profile/login/')
def holdline_list(request):
	hold_profiles = Profile.objects.filter(user_current_status='ON_HOLD',status=True)
	context ={
		'hold_profiles': hold_profiles,
	}

	return render(request,'admin/member/holdline_list.html',context)
#hide hold line  member from smadmin by partial delte using js
@login_required(login_url='/home/profile/login/')
def hide_hold(request,pk):
	memberhold_all = Profile.objects.get(id=pk)
	if request.method == "POST":
		del_hold_member = request.POST.get('del_hold_member')
		if del_hold_member == "partial":
			if memberhold_all.status == True:
				memberhold_all.status = False
				memberhold_all.save()
		elif del_hold_member == "permanent":
				memberhold_all.delete()
	return redirect(reverse_lazy('holdline_list'))


@login_required(login_url='/home/profile/login/')
def pakage_line_member(request):
	package_profiles = Profile.objects.filter(user_current_status='TOP_HUNDRED', status=True)
	
	context ={
		
		'package_profiles':package_profiles,
	}
	return render(request,'admin/member/pakage_line_member.html',context)
#hide   member from smadmin by partial delte using js
@login_required(login_url='/home/profile/login/')
def hide_member(request, pk):
	member = Profile.objects.get(id=pk)
	
	if request.method == "POST":
		delete_status = request.POST.get('delete_status')
		print(delete_status)
		if delete_status == "partial":

			if member.status == True:
				member.status = False
				member.save()
		elif delete_status == "permanent":
			member.delete()
	return redirect(reverse_lazy('pakage_line_member'))

#edit new member
@login_required(login_url='/home/profile/login/')
def edit_member(request,pk,member_type):
	edit_new_member = Profile.objects.get(id=pk)
	
	form = EditProfileForm(instance=edit_new_member)
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=edit_new_member)
		if form.is_valid():
			form.save()
			print("submitted,,,,,,,,,,,,,,,,")
			if member_type == "new":
				return redirect(reverse_lazy('new_member')) 
			elif member_type == "hold":
				return redirect(reverse_lazy('holdline_list')) 
			elif member_type == "top":
				return redirect(reverse_lazy('pakage_line_member')) 
	context ={
		'form': form,
		'edit_new_member':edit_new_member,
	}
	return render(request, 'admin/member/new_edit_member.html',context)

@login_required(login_url='/home/profile/login/')
def new_edit_member(request,pk):
	return edit_member(request,pk,"new")
	#return render(request, 'admin/member/new_edit_member.html')

@login_required(login_url='/home/profile/login/')
def hold_edit_member(request,pk):
	return edit_member(request,pk,"hold")
	#return render(request, 'admin/member/new_edit_member.html')

@login_required(login_url='/home/profile/login/')
def top_edit_member(request,pk):
	return edit_member(request,pk,"top")
	#return render(request, 'admin/member/new_edit_member.html')


# super admin profile edit here
@login_required(login_url='/home/profile/login/')
def edit_admin(request):

	user_admin = User.objects.get(id= request.user.id)
	photo_admin = ''
	if UserExtended.objects.filter(user=user_admin).exists():
		photo_admin = UserExtended.objects.get(user=user_admin)

	print(request.user.id)
	print(user_admin)
	if request.method == 'POST':
		form = EditAdminForm(request.POST, instance=request.user)
		profile_form = AdminPhotoForm(request.POST,request.FILES)

		if form.is_valid() and profile_form.is_valid:
			
			form.save()
			p = profile_form.save()
			print(p)
			p.user = user_admin
			p.save()
			return redirect(reverse_lazy('admin_dashboard')) 
	context ={
		'photo_admin':photo_admin,
		'user_admin':user_admin,
	}
	return render(request,'admin/user_admin/edit_admin.html',context)
