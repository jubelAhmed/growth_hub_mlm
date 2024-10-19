from user_admin.utils import create_new_ref_number
from django.core.checks import messages
from agent.models import Agent
from django.http import request
from user_profile.models import Package, Profile
from user_admin.forms import NotificationForm, UpdateForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from .models import Notification, PackageBalance
from django.db.models import Count  
from django.utils import timezone 
from django.db.models import Sum
from user_profile.models import Month

from datetime import datetime
from django.urls import reverse_lazy
from django.db.models import Q
from datetime import date
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from account.models import AgentBalanceAdd, AgnetBalance, AgentBalanceWithdraw, UserBalanceWithdraw

@login_required(login_url='/home/profile/login/')
def admin_dashboard(request):
    # If user in not staff redirect to normal profile
    if not request.user.is_staff:
        return redirect('profile')

    if Package.objects.filter(package_name='Primary').exists():
        primary_package_id= Package.objects.get(package_name='Primary')
    if Package.objects.filter(package_name='Premium').exists():
        premium_package_id= Package.objects.get(package_name='Premium')
    primary_user_list = []
    premium_user_list = []
    winner_list = []
 
    winner_list = Profile.objects.filter(user_current_status='WINNER',status=True, updated_date__startswith = date.today())

    if winner_list.count() <= 0:
        winner_list = Profile.objects.filter(user_current_status='WINNER',status=True,  updated_date__lte = date.today()).order_by('updated_date')[0:2]
        
    if primary_package_id:
        primary_100_user_list = Profile.objects.filter(user_current_status='TOP_HUNDRED', status=True, package_id=primary_package_id)
        primary_hold_user_list = Profile.objects.filter(user_current_status='ON_HOLD', status=True, package_id=primary_package_id).order_by('updated_date')
        primary_new_user_list = Profile.objects.filter(user_current_status='NEW_USER', status=True, package_id=primary_package_id).order_by('updated_date')
        # primary_new_user_list1  = makeObject(request,list(primary_new_user_list))
    

    if premium_package_id:
        premium_100_user_list = Profile.objects.filter(user_current_status='TOP_HUNDRED', status=True,package_id=premium_package_id).order_by('updated_date')
        premium_hold_user_list = Profile.objects.filter(user_current_status='ON_HOLD', status=True,package_id=premium_package_id).order_by('updated_date')
        premium_new_user_list = Profile.objects.filter(user_current_status='NEW_USER', status=True,package_id=premium_package_id).order_by('updated_date')
       
    context = {
        'primary_100_user_list': primary_100_user_list,
        'primary_new_user_list': primary_new_user_list,
        'primary_hold_user_list': primary_hold_user_list,

        'premium_100_user_list': premium_100_user_list,  
        'premium_new_user_list': premium_new_user_list,
        'premium_hold_user_list': premium_hold_user_list,
        'winner_list': winner_list,

    }
    # member_chart(request)

    return render(request, 'admin/admin_index.html',context)

@login_required(login_url='/home/profile/login/')
def hold_user_update(request,pk):
    update_profile = Profile.objects.get(id=pk)
    if request.method == "POST":
        update_profile.user_current_status = 'TOP_HUNDRED'
        if Profile.objects.filter(user_current_status='TOP_HUNDRED',status=True,package_id=update_profile.package_id).count() == 2:
            package_balance = PackageBalance.objects.get(package=update_profile.package_id)
            winner_user = Profile.objects.filter(user_current_status='TOP_HUNDRED',package_id=update_profile.package_id).order_by('updated_date')[0]
            winner_user.user_current_status = 'WINNER'
            winner_user.current_wallet = winner_user.current_wallet + calculate_win_profit(package_balance)
            winner_user.save()

        update_profile.save()

    return redirect(reverse_lazy('admin_dashboard'))

@login_required(login_url='/home/profile/login/')
def calculate_win_profit(package_balance):
    profit = (package_balance.package.package_amount * package_balance.profit_percentage)/100
    return profit
    

    #  ("NEW_USER", "new"),
    # ("ON_HOLD", "hold"),
    # ("TOP_HUNDRED", 'tophundred'),
    # ("WINNER", 'winner')

@login_required(login_url='/home/profile/login/')
def agent_account_balance(request):
    history = AgnetBalance.objects.all()
    total_agent_amount = AgnetBalance.objects.all().aggregate(Sum('amount'))
    return render(request, 'admin/money/agent_money_list.html', {'history': history,'total_agent_amount':total_agent_amount})

@login_required(login_url='/home/profile/login/')
def admin_account_balance(request):
    total_agent_amount = AgnetBalance.objects.all().aggregate(Sum('amount'))
    total_agent_add_amount = AgentBalanceAdd.objects.all().aggregate(Sum('amount'))
    total_admin_balance =  AgentBalanceWithdraw.objects.all().aggregate(Sum('amount'))
    context = {
        'total_agent_amount':total_agent_amount,
        'total_agent_add_amount':total_agent_add_amount,
        'total_admin_balance':total_admin_balance
    }
    return render(request, 'admin/money/admin_account.html', context=context)

@login_required(login_url='/home/profile/login/')
def give_agent_money(request):

    history = AgentBalanceAdd.objects.all()
    total_done_amount = AgentBalanceAdd.objects.all().aggregate(Sum('amount'))
   

    if request.method == 'POST':
        username = request.POST['username']
        amount = request.POST['amount']
        if username and amount:
            # Check user is exists or not
            if User.objects.filter(username=username).exists():
                sendMoneyTo = User.objects.get(username=username)
                # Check is this user is an agent 
                if Agent.objects.filter(user=sendMoneyTo).exists():
                    #  Check Agent is exists if exists save money
                    agb = AgnetBalance.objects.get(agent=sendMoneyTo)
                    agb.amount = agb.amount + float(amount)
                    agb.save()

                    # Now create history
                    agba = AgentBalanceAdd()
                    agba.agent = sendMoneyTo
                    agba.amount = float(amount)
                    agba.save()

                    # Done let's return a success message
                    return render(request, 'admin/money/give_agent_money.html', {'history': history,'total_done_amount':total_done_amount, 'success': 'Account Reloaded!'})
                else:
                    return render(request, 'admin/money/give_agent_money.html', {'history': history,'total_done_amount':total_done_amount, 'error': 'Given username is not an Agent!'})
            else:
                return render(request, 'admin/money/give_agent_money.html', {'history': history,'total_done_amount':total_done_amount, 'error': 'Your given username is not valid!'})
        else:
            return render(request, 'admin/money/give_agent_money.html', {'history': history,'total_done_amount':total_done_amount, 'error': 'You must fill up all fields currectly!'})
    else:
        return render(request, 'admin/money/give_agent_money.html', {'history': history,'total_done_amount':total_done_amount})

@login_required(login_url='/home/profile/login/')
def agent_money_withdraw(request):
    history = AgentBalanceWithdraw.objects.all()
    total_done_amount = AgentBalanceWithdraw.objects.filter(status="DONE").aggregate(Sum('amount'))
    total_pending_amount = AgentBalanceWithdraw.objects.filter(~Q(status = "DONE") ).aggregate(Sum('amount'))
    if request.method == "POST":
        reqid = request.POST['reqid']
        agentName = request.POST['agentusername']
        trx = request.POST['trx']

        if reqid and agentName and trx:
            if User.objects.filter(username=agentName).exists():
                agentUser = User.objects.get(username=agentName)
                if AgentBalanceWithdraw.objects.filter(pk=reqid, agent=agentUser).exists():
                    agbw = AgentBalanceWithdraw.objects.get(pk=reqid, agent=agentUser)
                    agbw.transection_id = trx
                    agbw.status = 'DONE'
                    agbw.save()
                    return render(request, 'admin/money/agent_money_withdraw.html', {'history': history, 'total_done_amount':total_done_amount,'total_pending_amount':total_pending_amount, 'success': "Operation Successful. Withdrawal Successful!"})
                else:
                    return render(request, 'admin/money/agent_money_withdraw.html', {'history': history, 'total_done_amount':total_done_amount,'total_pending_amount':total_pending_amount, 'error': "No request found with your data! Check your fillup again!"})
            else:
                return render(request, 'admin/money/agent_money_withdraw.html', {'history': history,'total_done_amount':total_done_amount,'total_pending_amount':total_pending_amount, 'error': "No user found with this username!"})  
        else:
            return render(request, 'admin/money/agent_money_withdraw.html', {'history': history,'total_done_amount':total_done_amount,'total_pending_amount':total_pending_amount ,'error': "You must fill up this form currectly!"})


    else:
        return render(request, 'admin/money/agent_money_withdraw.html', {'history': history,'total_done_amount':total_done_amount,'total_pending_amount':total_pending_amount})


@login_required(login_url='/home/profile/login/')
def user_money_withdraw(request):
    history = UserBalanceWithdraw.objects.all()

    total_done_amount = UserBalanceWithdraw.objects.filter(status="DONE").aggregate(Sum('amount'))
    total_pending_amount = UserBalanceWithdraw.objects.filter(~Q(status = "DONE") ).aggregate(Sum('amount'))
    
    
    return render(request, 'admin/money/user_money_withdraw.html', {'history': history,'total_done_amount':total_done_amount,'total_pending_amount':total_pending_amount})

@login_required(login_url='/home/profile/login/')
def member_chart(request):
    # summary = Profile.objects.all().annotate(m=Month('created_date__month')).values('m').annotate(total=Count('id')).order_by()
    summery = Profile.objects.values('package_id__package_name','created_date__month','created_date__year').annotate(total_member=Count('created_date__month')).order_by('created_date__month')

    primary = summery.filter(Q(package_id__package_name='Primary'))
    premium = summery.filter(Q(package_id__package_name='Premium'))
    
    member_bar_chart = {
        'primary':list(primary),
        'premium':list(premium)
    }
    
    return JsonResponse(member_bar_chart)