from django.shortcuts import redirect, render
from agent.models import Agent
from user_profile.models import Profile, Package
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.contrib.auth.models import User

@login_required(login_url='/profile/login/')
def ChangePassword(request):
    package_id = Package.objects.all()
    context ={'package_id': package_id}

    wrongpassContext = {'package_id': package_id, 'wrongpass': 'Your old password not correct!'}
    passwordResetSuccess = {'package_id': package_id, 'passResetsuccess': 'Password Reset Success!'}
    wronginput = {'package_id': package_id, 'wrongpass': 'New password not matched!'}

    if request.method == "POST":
        
        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')
        newpassagain = request.POST.get('anewpass')

        


        # print("isValid" + isValid)
        print("Username" + request.user.username)
        print("oldpass" + oldpass)
        print("newpass" + newpass)
        

        if oldpass and newpass and newpass == newpassagain:
            saveuser = User.objects.get(id=request.user.id)

            if saveuser.check_password(oldpass):
                saveuser.set_password(newpass)
                saveuser.save()
                return render(request, 'users/user_profile/update_profile.html', passwordResetSuccess)
            else:
                return render(request, 'users/user_profile/update_profile.html', wrongpassContext)
        else:
            return render(request, 'users/user_profile/update_profile.html', wronginput)

    else:
        return redirect('update_profile')