from django.urls import path
from . import views
from account.profile_update import updateProfile
from account.change_password import ChangePassword
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
	path('profile/', views.profile, name='profile'),
	#path('edit_profile/', views.edit_profile, name='edit_profile'),
	#path('signup/', views.signup, name='signup'),
	path('update_profile/', updateProfile, name='update_profile'),
	path('registration/', views.registration, name='registration'),
	path('change_password/', ChangePassword, name='changepassword'),
	path('profile/login/', views.login, name='login'),
	path('logout/', views.logout, name='logout'),
	path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/user_profile/password_reset.html'), name='password_reset'),
	path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/user_profile/password_reset_done.html'), name='password_reset_done'),
	path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/user_profile/password_reset_confirm.html'), name='password_reset_confirm'),
	path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/user_profile/password_reset_complete.html'), name='password_reset_complete'),
	path('network/downline_network/', views.downline_network, name='downline_link'),
	path('reports/sponsor_reports/',views.sponsor_reports, name='sponsor_reports'),
	path('profile/stair/',views.stair_reports, name='stair_reports'),
]	