from django.shortcuts import render

# Create your views here.
def account(request):

	return render(request, 'users/account/account.html')