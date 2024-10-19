from django.db.models.fields import DecimalField, FloatField
from agent.forms import UpdateAgentForm
from django.shortcuts import render
from django.contrib.auth.models import User
from agent.models import Agent
from django.http.response import HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .utils import create_new_ref_number
from django.urls import reverse_lazy
from account.models import AgnetBalance,UserBalanceWithdraw
from user_profile.functions import password_check, emailValidator
from django.contrib import messages

# Create your views here.
def agent(request):

	return render(request, 'users/agent/agent.html')

def agent_list(request):
	#selected_package = None
	all_agent = Agent.objects.all()
	context={
		'all_agent':all_agent,
	}
	return render(request,'admin/agent/agent_list.html',context)

#adding agent by form  
def add_agent(request):

	if request.method == "POST":
		username = request.POST.get('username')
		email = request.POST.get('email')
		password=request.POST.get('password')
		repassword = request.POST.get('password2')
		full_name = request.POST.get('full_name')
		address = request.POST.get('address')
		country = request.POST.get('country')			
		district = request.POST.get('district')
		division = request.POST.get('division')
		mobile_no = request.POST.get('mobile_no')
		birth_date = request.POST.get('birth_date')
		
		thana =request.POST.get('thana')
		#this form system has used because we want that if any reason form can not submit then the input 
		 #filed will not empty and it will be fill up by the data what he has filled previously for submit.
		form_field = {
		"username" : username,
		"email" : email,
		"password" : password,
		"password2" : repassword,
		"full_name" : full_name,
		"address" : address,
		'country' : country,
		'district' :  district,
		'division' : division,
		'mobile_no' : mobile_no,
		
		'thana':thana,
		'birth_date' : birth_date
			}
		#profile_form = UserProfileForm(request.POST)
		if request.POST['username'] and request.POST['password'] == request.POST['password2']:

			if User.objects.filter(username=request.POST['username']).exists():
				return render(request, 'admin/agent/add_agent.html',{ 'form_field':form_field, 'error': "username has already taken"})
				
			else:
    			
				username = request.POST['username']
				email = request.POST['email']
				password=request.POST['password']

				if emailValidator(email):
					if password_check(password):
						user = User.objects.create_user(username = request.POST['username'],email = request.POST['email'],password=request.POST['password'])
						full_name = request.POST.get('full_name')
						address = request.POST.get('address')
						country = request.POST.get('country')
						tnx_no = create_new_ref_number() #request.POST.get('tnx_no')
						mobile_no =request.POST.get('mobile_no')#request.POST.get('agent_id')
						#package_id =Package.objects.get(id)
						division = request.POST.get('division')
						district = request.POST.get('district')
						thana =request.POST.get('thana')
						
						birth_date = request.POST.get('birth_date')
						agent = Agent(full_name=full_name,thana=thana,division=division,district =district,tnx_no=tnx_no,address=address,country=country,mobile_no=mobile_no,birth_date=birth_date, user=user)
						
						agent.save()
						# Now Creating Balance System for Agent
						abl = AgnetBalance()
						abl.agent = user
						abl.save()
						return redirect(reverse_lazy('agent_list'))
					else:
						return render(request, 'admin/agent/add_agent.html',{'form_field':form_field,  'error': "Password is not strong enough"})
				else:
					return render(request, 'admin/agent/add_agent.html',{'form_field':form_field,  'error': "Another user already using this email or this email is not given or valid!"})		
		
		else:
			return render(request, 'admin/agent/add_agent.html', { 'form_field':form_field,'error': "You must fill up all input currectly!"})
	else:

		return render(request,'admin/agent/add_agent.html')



#update agent details by his id 
def agent_update(request,pk):
	agent = Agent.objects.get(id=pk)
	form = UpdateAgentForm(instance=agent)

	if request.method == 'POST':
		
		form = UpdateAgentForm(request.POST,request.FILES, instance=agent)
		if form.is_valid():
			
			
			form.save()
			return redirect(reverse_lazy('agent_list'))
	context ={
		'form': form,
		'agent':agent,
	}
	return render(request,'admin/agent/agent_update.html',context)


#delete agent by his id
def delete_agent(request, pk):
	del_agent = Agent.objects.get(id=pk)
	if request.method == "POST":
		del_agent.delete()
		return redirect(reverse_lazy('agent_list'))
	context = {
		'del_agent': del_agent,
	}
	return render(request, 'admin/agent/agent_list.html', context)


# here showing all the user who withdraw balance
def user_withdraw_list(request):
	user_list = UserBalanceWithdraw.objects.all()
	
	context ={
		'user_list':user_list,

	}
	return render(request, "users/agent/user_withdraw_list.html",context)

def change_user_status(request,pk):
	member_user = UserBalanceWithdraw.objects.get(id=pk)
	if request.method == "POST":
		#status = request.POST.get('status')
		if request.POST.get('user_status-'+pk):
			status = request.POST.get('user_status-'+pk)	
			if member_user.status == 'PENDING' or member_user.status == 'REJECTED':
				if status == 'success':
					agent_balance = AgnetBalance.objects.get(agent=request.user)
					agent_balance.amount = agent_balance.amount + float(member_user.amount)   						
					agent_balance.save()
					member_user.status = 'DONE'
					member_user.save()
					messages.success(request, 'You are successfully Added balance & Your Balance is  $ '+ str(agent_balance.amount))
						# Done
					return redirect('user_withdraw_list')
				elif status == 'rejected':
					member_user.status = 'REJECTED'
					member_user.save()

	return redirect(reverse_lazy('user_withdraw_list'))