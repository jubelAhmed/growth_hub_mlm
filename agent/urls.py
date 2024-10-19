from django.urls import path
from . import views


urlpatterns = [
	path('', views.agent, name = 'agent'),
	path('agent_list/',views.agent_list, name='agent_list'),
	path('add_agent/',views.add_agent, name='add_agent'),
	path('agent_update/<str:pk>/',views.agent_update, name='agent_update'),
	path('delete_agent/<str:pk>/', views.delete_agent, name='delete_agent'),
	path('user_withdraw_list/',views.user_withdraw_list, name='user_withdraw_list'),
	path('change_user_status/<str:pk>/',views.change_user_status, name='change_user_status'),
]