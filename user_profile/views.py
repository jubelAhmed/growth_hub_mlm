from organization.models import UserDashboardContent
from user_admin.models import Notification
from agent.models import Agent
from django.contrib.auth.backends import UserModel
from django.core import exceptions
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Package, Profile, Sponsor,Month
from .functions import validateSponsorID, password_check, emailValidator, is_top_hundered, is_total_two_sponsor,get_notification,get_percentage
from django.contrib import auth
from django.contrib.auth.models import User
from .utils import create_new_ref_number
from .forms import InfoProfileForm,ProfileForm
from datetime import datetime
from datetime import date
from django.contrib.auth.decorators import login_required
from account.context import user_type
from django.urls import reverse_lazy
from django.db.models import Q
from django.db.models import Sum
from account.models import AgnetBalance
from django.contrib import messages
# Create your views here.


@login_required(login_url='/home/profile/login/')
def home(request):
	user_dasboard_content = UserDashboardContent.objects.all()
	if Package.objects.filter(package_name='Primary').exists():
		primary_package_id= Package.objects.get(package_name='Primary')
	if Package.objects.filter(package_name='Premium').exists():
		premium_package_id= Package.objects.get(package_name='Premium')
	
	primary_user_list = []
	premium_user_list = []
	winner_list = []
 
	winner_list = Profile.objects.filter(user_current_status='WINNER', updated_date__startswith = date.today())
 
	if winner_list.count() <= 0:
		winner_list = Profile.objects.filter(user_current_status='WINNER', updated_date__lte = date.today()).order_by('updated_date')[0:2]
		
	if primary_package_id:
		primary_user_list = Profile.objects.filter(user_current_status='TOP_HUNDRED',package_id=primary_package_id).order_by('updated_date')
	if premium_package_id:
		premium_user_list = Profile.objects.filter(user_current_status='TOP_HUNDRED',package_id=premium_package_id).order_by('updated_date')
	
 
	notification_context = get_notification(request)
	context = {
		'notification_object': notification_context,
		'primary_user_list': primary_user_list,
		'premium_user_list': premium_user_list,
		'winner_list': winner_list,
		'user_dasboard_content':user_dasboard_content,

	}
	return render(request, 'users/index.html',context=context)

@login_required(login_url='/home/profile/login/')
def downline_network(request):
	
	all_downline_list = []
	userType = user_type(request)
	print(userType)
	if userType['usertype'] == 'agent':
		if Profile.objects.filter(agent= request.user).exists():
			sponsor_list = Profile.objects.filter(agent= request.user).order_by('created_date')
			all_downline_list.extend(sponsor_list)
	else:
    
		# print(Profile.objects.filter(sponsor=request.user).exists())
		if Profile.objects.filter(user=request.user).exists():  
			own_profile = Profile.objects.get(user=request.user)
			print(own_profile)
			# profile = Profile.objects.raw('SELECT * FROM user_profile_profile')
			profile = own_profile.my_custom_sql() 
			print(profile)
			for p in profile:
				all_downline_list.append(Profile.objects.get(user_id=p['user_id']))
			
	context = {
		'all_downline_list' : all_downline_list
	}

	return render(request, 'users/user_profile/downline_network.html',context=context)

@login_required(login_url='/home/profile/login/')
def stair_reports(request):
    	
	stair_list = []

	userType = user_type(request)

	if userType['usertype'] == 'agent':
		if Profile.objects.filter(agent= request.user).exists():
			stair_list = Profile.objects.filter(agent= request.user).order_by('created_date')
	else:
		if Profile.objects.filter(sponsor=request.user).exists():
			stair_list = Profile.objects.filter(sponsor=request.user).order_by('created_date')
	
	context = {
		'stair_list' : stair_list
	}

	return render(request, 'users/reports/stair_reports.html',context=context)

@login_required(login_url='/home/profile/login/')
def sponsor_reports(request):
	userType = user_type(request)
	print(userType)
	sponsor_list = []
	if userType['usertype'] == 'agent':
		if Profile.objects.filter(agent= request.user).exists():
			sponsor_list = Profile.objects.filter(agent= request.user)
		
	return render(request,'users/reports/sponsor_reports.html',{"sponsor_list":sponsor_list})
	

@login_required(login_url='/home/profile/login/')
def profile(request):
	if request.user.is_staff:
		return redirect('admin_dashboard')
	# profile_data = Profile.objects.get(user=request.user)
	# context = {
	# 	'profile_data': profile_data,
	# }
	notification_list = Notification.objects.filter(duration__gte=datetime.now())
	notification_count = len(notification_list)
	print(notification_count)
	context ={
		'notification_list':notification_list,

		'notification_count':notification_count,
		}
	return render(request, 'users/user_profile/profile.html',context)

@login_required(login_url='/home/profile/login/')
def update_profile(request):
	#selected_package = None
	package_id = Package.objects.all()
	
	if request.method == "POST":
		
		try:
			profile = Profile.objects.get(id=request.user.id)
			
		
			#user = User.objects.get(username = request.POST['username'],email = request.POST['email'])
			full_name = request.POST.get('full_name')
			address = request.POST.get('address')
			country = request.POST.get('country')
			#tnx_no = create_new_ref_number() #request.POST.get('tnx_no')
			 #request.POST.get('agent_id')
				#package_id =Package.objects.get(id)
			photo = request.FILES.get('photo')	
			#pk_id = request.POST.get('package_name')
			#package_id =Package.objects.get(id=pk_id)
			#print(package_id)

			mobile_no = request.POST.get('mobile_no')
			birth_date = request.POST.get('birth_date')
			#profile = Profile(full_name=full_name,photo=photo,address=address,country=country,mobile_no=mobile_no,birth_date=birth_date, )
			profile.full_name=full_name
			profile.address = address
			
			profile.mobile_no = mobile_no
			if photo:
				profile.photo = photo
				
			profile.save()
			return render(request, 'users/user_profile/profile.html')
		except User.DoesNotExist:		
			
				#auth.login(request,user)
				#return render(request, 'users/user_profile/signup.html')
			return render(request, 'users/user_profile/update_profile.html')

	else:
		context ={
			     #'selected_package':selected_package,
			'package_id': package_id,
					}
		return render(request, 'users/user_profile/update_profile.html',context)

	
@login_required(login_url='/home/profile/login/')
def registration(request):
	#selected_package = None
	packages = Package.objects.all()

	 
	
	if request.method == "POST":
		#profile_form = UserProfileForm(request.POST)
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
		if request.POST['username'] and request.POST['password'] == request.POST['password2']:

			if User.objects.filter(username=request.POST['username']).exists():
				return render(request, 'users/account/registration.html',{ 'packages': packages,'form_field':form_field, 'error': "username has already taken"})
			else:
				
				username = request.POST.get('username')
				email = request.POST.get('email')

				password=request.POST.get('password')
				repassword = request.POST.get('repassword')

				full_name = request.POST.get('full_name')
				address = request.POST.get('address')
				country = request.POST.get('country')
				tnx_no = create_new_ref_number()  
				 
				sponsor = request.POST.get('sponsor_id')

				pk_id = request.POST.get('package_name')
				package_id =Package.objects.get(id=pk_id)

				

				mobile_no = request.POST.get('mobile_no')
				birth_date = request.POST.get('birth_date')

				AgentProfile = Agent.objects.get(user=request.user)

				agent_balance  = AgnetBalance.objects.get(agent=request.user)

				if agent_balance.amount >= package_id.package_amount:
				# Check sponsor 
					if validateSponsorID(sponsor):
						# password_check
						if emailValidator(email):
							if password_check(password):
								user = User.objects.create_user(username=username, password=password, email=email)
								user.save()
								
								SponsorUser = User.objects.get(username=sponsor) if sponsor else ''
									
								SponsorProfile = Profile.objects.get(user=SponsorUser) if SponsorUser else ''
		
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
								newprofile.agent = request.user
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
								agent_balance.amount = float(agent_balance.amount) - float(package_id.package_amount)

								agent_balance.save()
								
								return render(request, 'users/account/registration.html',{'packages': packages, 'agent': AgentProfile.full_name, 'package': package_id.package_name, 'accountCreated': "Account Created!", 'user_name': username, 'pass': password, 'sponsor': SponsorProfile.full_name if SponsorProfile else ''})
							else:
								return render(request, 'users/account/registration.html',{'packages': packages,'form_field':form_field, 'error': "Password is not strong enough you can use generator!"})
						else:
							return render(request, 'users/account/registration.html',{'packages': packages,'form_field':form_field, 'error': "Another user already using this email or this email not valid!"})	
					else:
						return render(request, 'users/account/registration.html',{'packages': packages,'form_field':form_field, 'error': "Sponsor id not valid or this sponsor already has 3 user!"})
				else:
					return render(request, 'users/account/registration.html',{'packages': packages,'form_field':form_field,  'error': "Your does not have any enough balance for registration."})	

		else:
			return render(request, 'users/account/registration.html', {'packages': packages,'form_field':form_field, 'error': "You must fill up all input currectly!"})
	
	
	else:
		return render(request, 'users/account/registration.html', {'packages': packages})



#login code
def login(request):
	if request.user.is_authenticated:
		return redirect('profile')
 
	if request.method == 'POST':
		username = str(request.POST['username'])
		password = str(request.POST['password'])
		user = auth.authenticate(username=username,password=password)
		if user is not None:
		#if not request.user.is_authenticated:
			
			auth.login(request, user)

			return redirect('profile')
			# notification_list = Notification.objects.filter(duration__gte=datetime.now())
			# notification_count = len(notification_list)
			# print(notification_count)
			# context ={
			# 	'notification_list':notification_list,
	
			# 	'notification_count':notification_count,
			# 	}
			# return render(request, 'users/user_profile/profile.html',context)
		else:
			messages.error(request, 'You must provide right user name and password')
			return redirect('login')

	else:
		return render(request,'users/account/login.html')

@login_required(login_url='/home/profile/login/')
def logout(request):
	auth.logout(request)
	return redirect(reverse_lazy('login')) 







