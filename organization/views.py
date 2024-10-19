from django.shortcuts import render, redirect
from account.models import AgnetBalance, AgentBalanceExchange, AgentBalanceWithdraw, AgentBalanceAdd,UserBalanceWithdraw,AdminAccount
from agent.models import Agent
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from agent.models import Agent
from user_profile.models import Profile
from .models import About, CompanyAddress, Marketing, Package, Question,TermsCondition, navbarSupportedContent, Contact
from .forms import ContactForm
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from growth_hub_mlm.settings import EMAIL_HOST, EMAIL_HOST_USER
from django.contrib import messages
# here all the landing page dynamic work has done

def landing_home(request):
    landing_banner_content = navbarSupportedContent.objects.all()[:1]
    company_address = CompanyAddress.objects.all()
    all_about = About.objects.all()
    marketing_text = Marketing.objects.all()
    all_question =  Question.objects.all()
    all_package = Package.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            c=form.save(commit=False)
            c.name  = request.POST.get('name')
            c.phone = request.POST.get('phone')
             
            c.address =  request.POST.get('address')
            #subject = form.cleaned_data['subject']
            email =  form.cleaned_data['email']
            message= form.cleaned_data['message']
            email_to = EMAIL_HOST_USER
               
            #send_mail( message, email_from, [email_to,], fail_silently=False)

            email = EmailMessage(body=message,to=[email_to,],reply_to=[email],)
            form.save()
            c.save()
            email.send()
            return render(request, 'landing/index.html', {'form': form})
    form = ContactForm()
    context ={
        'landing_banner_content':landing_banner_content,
        'company_address':company_address,
        'form': form,
        'all_question':all_question,
        'all_about':all_about,
        'marketing_text':marketing_text,
        'all_package':all_package,
    }
    
    return render(request, 'landing/index.html',context)

@login_required(login_url='/profile/login/')
def sponsor_reports(request):
    return render(request,'users/reports/sponsor_reports.html')

@login_required(login_url='/profile/login/')
def exchange_reports(request):
    return render(request,'users/reports/exchange_reports.html')

@login_required(login_url='/profile/login/')
def transfer_reports(request):
    return render(request,'users/reports/transfer_report.html')

@login_required(login_url='/profile/login/')
def balance_add(request):
    return render(request,'users/balance/balance_add.html')

@login_required(login_url='/profile/login')
def agent_balance_add_history(request):
    balance = AgnetBalance.objects.get(agent=request.user)
    history = AgentBalanceAdd.objects.filter(agent=request.user)
    return render(request,'users/balance/agent_balance_add_history.html', {'balance': balance, 'history': history})

@login_required(login_url='/profile/login/')
def balance_withdrow(request):
    balance = AgnetBalance.objects.get(agent=request.user)
    history = AgentBalanceWithdraw.objects.filter(agent=request.user)
    admin_account = AdminAccount.objects.filter()[0:1][0]
    print(admin_account)
    if request.method == "POST":
        amount = request.POST['wamount']
        pin = request.POST['wpin']
        
        if amount and pin:
            agentbal = AgnetBalance.objects.get(agent=request.user)
            agent = Agent.objects.get(user=request.user)
            if str(agent.tnx_no) == str(pin):
                if agentbal.amount >= float(amount):
                    # Adding Request to agentBalanceWithdraw Table (Admin can take action later)
                    agw = AgentBalanceWithdraw()
                    agw.agent = request.user
                    agw.amount = float(amount)
                    agw.accountIdentifier = admin_account.btc_address if admin_account.btc_address else 0
                    agw.transection_id = pin
                    agw.save()
                    # Now minus balance from agent account
                    agentbal.amount = float(agentbal.amount) - float(amount)
                    agentbal.save()

                    if admin_account:
                        admin_account.amount = float(admin_account.amount) + float(amount)
                        admin_account.save()
                    # Done
                    messages.success(request, 'Your balance withdrawal request created Successfully.')
                            # Done
                    return redirect('balance_withdrow')
                    # return render(request,'users/balance/balance_withdrow.html', {'balance': balance, 'history': history, 'success': 'Your balance withdrawal request created Successfully.'})
                else:
                    return render(request,'users/balance/balance_withdrow.html', {'balance': balance, 'history': history, 'admin_account':admin_account, 'error': 'You does not have enough balance. Please request less amount.'})  
            else:
                return render(request,'users/balance/balance_withdrow.html', {'balance': balance, 'history': history, 'admin_account':admin_account, 'error': 'Please Provide the Correnct Transaction Number.'})  
        else:
           return render(request,'users/balance/balance_withdrow.html', {'balance': balance, 'history': history,  'admin_account':admin_account,'error': 'You must fill up withdraw request correctly!'}) 
    else:
        return render(request,'users/balance/balance_withdrow.html', {'balance': balance,  'admin_account':admin_account, 'history': history,})


#user balance withdrwa by a  agent

@login_required(login_url='/profile/login/')
def user_balance_withdrow(request):
    userProfile = Profile.objects.get(user=request.user)

    # checking user balance withdraw histor by query
    history = UserBalanceWithdraw.objects.filter(user=request.user)
    #only user can withdraw if he is winner.so we need to check the status
    valid_status = 'valid' if userProfile.user_current_status == 'WINNER' else 'invalid'
    context ={
        'valid_status':valid_status,
        'history':history,
        'userProfile':userProfile,
    }
    if request.method == "POST":
        amount = request.POST['wamount']
        agent_user_name = request.POST['agent_user_name']
        pin = request.POST['wpin']
        
        if userProfile.user_current_status == 'WINNER':
            if amount and agent_user_name and pin:
                if str(userProfile.tnx_no) == str(pin):
                    if Agent.objects.filter(user__username = agent_user_name).exists():
                        
                        if userProfile.current_wallet >= float(amount):
                            # Adding Request to agentBalanceWithdraw Table (Admin can take action later)
                            agw = UserBalanceWithdraw()
                            agw.user = request.user
                            agw.agent = User.objects.get(username=agent_user_name)
                            agw.amount = float(amount)
                           
                            agw.save()
                            # Now minus balance from agent account

                            userProfile.current_wallet =  userProfile.current_wallet - float(amount)
                           
                            userProfile.save()
                            # Now add blnc agent account
                           
                            # agent_balance = AgnetBalance.objects.get(agent=User.objects.get(username=agent_user_name))
                            # agent_balance.amount = agent_balance.amount + float(amount)   
                                                
                            # agent_balance.save()
                            
                            messages.success(request, 'You are successfully withdraw balance')
                            # Done
                            return redirect('user_balance_withdrow')
                        else:
                            messages.warning(request, 'You does not have enough balance. Please request less amount')
                            return redirect('user_balance_withdrow') 
                    else:
                        messages.warning(request, 'Please Provide the Valid Agent User Name')
                        return redirect('user_balance_withdrow')
                else:
                    messages.warning(request, 'Please Provide Valid Transation Number')
                    return redirect('user_balance_withdrow')
            else:
                messages.warning(request, 'You must fill up withdraw request correctly!')
                return redirect('user_balance_withdrow')
        else:
            messages.warning(request, 'You Must Need to be Winner For withdraw money')
            return redirect('user_balance_withdrow')
    else:
        return render(request,'users/balance/user_balance_withdrow.html', context)

@login_required(login_url='/profile/login/')
def transfer_action(request, username, trid, extype):
 
    if extype == 'accept':
        currentExchange = AgentBalanceExchange.objects.get(pk=trid)
        sender = currentExchange.sender
        receiver = currentExchange.receiver

        if username == currentExchange.receiver.username:
            currentExchange.status = "DONE"
            currentExchange.save()
            ab = AgnetBalance.objects.get(agent=currentExchange.receiver)
            ab.amount = ab.amount +  currentExchange.amount
            ab.save()
            
            return redirect('balance_transfer')
        else:
            return redirect('balance_transfer')
    elif extype == 'reject':
        currentExchange = AgentBalanceExchange.objects.get(pk=trid)
        sender = currentExchange.sender
        receiver = currentExchange.receiver
        if username == currentExchange.receiver.username:

            currentExchange.status = "REJECTED"
            currentExchange.save()

            ab = AgnetBalance.objects.get(agent=currentExchange.sender)
            ab.amount = ab.amount +  currentExchange.amount
            ab.save()
            return redirect('balance_transfer')
        else:
            return redirect('balance_transfer')
    else:
        return redirect('balance_transfer')



# Agent balance transfer has done dynamically here
@login_required(login_url='/profile/login/')
def balance_transfer(request):
    
    balance = AgnetBalance.objects.get(agent=request.user)

    history = AgentBalanceExchange.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    context = {'balance': balance, 'history' : history}
    useragent_object = Agent.objects.get(user=request.user)
    print(useragent_object)
    if request.method == "POST":
        agent = request.POST['agentusername']
        amount = request.POST['amount']
        pin = request.POST['pin']
        print(pin)
        print(useragent_object.tnx_no)
        if agent and amount and pin :
            agentUser = User.objects.get(username=agent)
            currentUserBalance = AgnetBalance.objects.get(agent=request.user)
            #check pin with agent trasaction pin.if match then it will go inside
            if str(useragent_object.tnx_no) == str(pin):
                if Agent.objects.filter(user=agentUser).exists():
                    if currentUserBalance.amount >= float(amount):
                        abe = AgentBalanceExchange()
                        abe.sender = request.user
                        abe.receiver = agentUser
                        abe.amount = amount
                        abe.save()
                        currentUserBalance.amount = currentUserBalance.amount - float(amount)
                        currentUserBalance.save()
                         # Now add blnc agent account
                        # agent_balance = AgnetBalance.objects.get(agent=User.objects.get(username=agentUser))
                        # agent_balance.amount = agent_balance.amount + float(amount)   
                                                
                        # agent_balance.save()                        

                        messages.success(request, 'Successfully created exchage request.')
                            # Done
                        return redirect('balance_transfer')
                        # return render(request,'users/balance/balance_transfar.html', {'balance': balance, 'history' : history, 'success': 'Successfully created exchage request'})
                    else:
                        return render(request,'users/balance/balance_transfar.html', {'balance': balance, 'history' : history, 'error': 'You do not have enough account balance!'})
                else:
                    return render(request,'users/balance/balance_transfar.html', {'balance': balance, 'history' : history, 'error': 'Agent with this username not exists!'})
            else:
                return render(request,'users/balance/balance_transfar.html', {'balance': balance, 'history' : history,'error': 'Please fill valid transaction pin!'})
        else:
            return render(request,'users/balance/balance_transfar.html', {'balance': balance, 'history' : history, 'error': 'Please fill up all field currectly!'})
    else:
        return render(request,'users/balance/balance_transfar.html', context)



#landing page about details has done dynamically here

def about(request):
    all_about = About.objects.all()[:1]
    context ={
        'all_about':all_about,
    }
    return render(request,"landing/about.html",context)

#landing page marketing details has done dynamically here
def market(request):
    marketing_text = Marketing.objects.all()[:1]
    context ={
        'marketing_text':marketing_text,
    }
    return render(request,"landing/marketing_policy.html",context)

#landing page terns and condition
def condition(request):
    marketing_text = TermsCondition.objects.all()[:1]
    print(marketing_text)
    context ={
        'terms_condition':marketing_text,
    }
    return render(request,"landing/terms_and_condition.html",context)

#landing page contact .info send to the admin mail by the contact form
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST,instance=Contact)
        if form.is_valid():
            print(form)
            full_name   = form.cleaned_data['full_name']
            phone = form.cleaned_data['phone']
            email =  form.cleaned_data['email'] 
            address =  form.cleaned_data['address'] 
            subject = form.cleaned_data['subject']
            
            message= form.cleaned_data['message']
            email_to = EMAIL_HOST_USER   
            # send_mail(subject, message, email_from, [email_to,], fail_silently=False)
            try:
                email = EmailMessage(full_name=full_name,phone =phone,address=address,body=message,from_email=email,to=[email_to,],reply_to=[email],)
                email.save()
                email.send()
            except:
                print('send fail')
           
            messages.success(request, 'You will get your response in you email')
            return render(request, 'landing/index.html', {'form': form})
    form = ContactForm()
    return render(request, 'landing/index.html', {'form': form})



# user dashboard content

