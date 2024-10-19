from django.contrib import admin
from .models import Notification,PackageBalance,UserExtended

admin.site.site_header = 'Referral Boost' 
admin.site.site_title = 'Referral Boost' 
admin.site.index_title = 'Referral Boost'

# Register your models here.
admin.site.register(Notification)
admin.site.register(PackageBalance)
admin.site.register(UserExtended)
