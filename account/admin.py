from django.contrib import admin
from .models import AgnetBalance, AgentBalanceAdd, AgentBalanceExchange, AgentBalanceWithdraw, UserBalanceWithdraw,AdminAccount
# Register your models here.
admin.site.register(AdminAccount)
admin.site.register(AgnetBalance)
admin.site.register(AgentBalanceAdd)
admin.site.register(AgentBalanceExchange)
admin.site.register(AgentBalanceWithdraw)
admin.site.register(UserBalanceWithdraw)