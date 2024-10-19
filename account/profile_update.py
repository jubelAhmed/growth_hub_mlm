from agent.models import Agent
from django.http.response import HttpResponse
from user_profile.models import Profile, Package
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

@login_required(login_url='/profile/login/')
def updateProfile(request):
    package_id = Package.objects.all()
    context ={'package_id': package_id}
    
    if request.method == "POST":
        usertype = request.POST['usertype']

        if usertype == 'agent':
            uprofile = Agent.objects.get(user=request.user)
            print("photo")
            print(request.FILES.get('photo'))
            if request.FILES.get('photo'):
                userphoto = request.FILES.get('photo')
            userphone = request.POST['phonenumber']
            useraddress = request.POST.get('useraddress')


            uprofile.mobile_no = userphone

            if request.FILES.get('photo'):
                uprofile.photo = userphoto
            uprofile.address = useraddress

            uprofile.save()
            return render(request, 'users/user_profile/update_profile.html',context)

        elif usertype == 'user':
            uprofile = Profile.objects.get(user=request.user)

            if request.FILES.get('photo') != "":
                userphoto = request.FILES.get('photo')
            userphone = request.POST['phonenumber']
            useraddress = request.POST.get('useraddress')


            uprofile.mobile_no = userphone

            if request.FILES.get('photo') != "":
                uprofile.photo = userphoto
            
            uprofile.address = useraddress

            uprofile.save()
            return render(request, 'users/user_profile/update_profile.html',context)
           
        else:
            return render(request, 'users/user_profile/update_profile.html',context)
    else:
        return render(request, 'users/user_profile/update_profile.html',context)