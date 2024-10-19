from django.contrib import admin
from .models import Notification,PackageBalance,UserExtended

admin.site.site_header = 'iTrader-Uk' 
admin.site.site_title = 'iTrader-Uk' 
admin.site.index_title = 'iTrader-Uk'

# Register your models here.
admin.site.register(Notification)
admin.site.register(PackageBalance)
admin.site.register(UserExtended)
