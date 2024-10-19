from django.urls import path
from . import views
from . import views_dashboard as views2
from . import views1 as views1

urlpatterns = [
	path('', views2.admin_dashboard, name ='admin_dashboard'),
	path('edit_admin/',views.edit_admin, name='edit_admin'),
	path('notification_list7/', views.notification_list7, name='notification_list7'),
	path('admin_contact/', views1.admin_contact, name='admin_contact'),
	path('delete_contact/<str:pk>/', views1.delete_contact, name='delete_contact'),
	path('contact_view/<str:id>/', views1.contact_view, name='contact_view'),
	path('agent_user_list/<str:pk>/', views1.agent_user_list, name='agent_user_list'),
	path('winner_List/',views1.winner_List, name='winner_List'),
	path('winner_list_view/<str:id>/', views1.winner_list_view, name='winner_list_view'),
	path('delete_winner/<str:pk>/', views1.delete_winner, name='delete_winner'),

	path('notification_update/<str:pk>/', views.notification_update, name='notification_update'),
	path('holdline_list/',views.holdline_list, name='holdline_list'),
	path('delete_notification/<str:pk>/', views.delete_notification, name='delete_notification'),
	path('new_member/',views.new_member, name='new_member'),
	path('add_member/',views.add_member, name='add_member'),
	path('pakage_line_member/',views.pakage_line_member, name='pakage_line_member'),

	path('hide_member/<str:pk>/',views.hide_member, name='hide_member'),
	path('hide_hold/<str:pk>/',views.hide_hold, name='hide_hold'),
	path('hide_new/<str:pk>/',views.hide_new, name='hide_new'),
	path('edit_member/<str:pk>/new',views.new_edit_member, name='new_edit_member'),
	path('edit_member/<str:pk>/hold',views.hold_edit_member, name='hold_edit_member'),
	path('edit_member/<str:pk>/top',views.top_edit_member, name='top_edit_member'),
	path('user_update/<str:pk>/hold', views2.hold_user_update, name='hold_update'),
	path('give_agent_money/', views2.give_agent_money, name='give_agent_money'),
	path('agent_account_balance/', views2.agent_account_balance, name='agent_account_balance'),
	path('admin_account_balance/', views2.admin_account_balance, name='admin_account_balance'),
	path('agent_money_withdraw/', views2.agent_money_withdraw, name='agent_money_withdraw'),
	path('user_money_withdraw/', views2.user_money_withdraw, name='user_money_withdraw'),
	path('dashboard/memberchart/', views2.member_chart, name='member_chart'),
	

]