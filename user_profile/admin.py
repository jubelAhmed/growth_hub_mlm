from django.contrib import admin

# Register your models here.
from .models import Package,UsePositionStatus,Profile, Sponsor
# Register your models here.

# admin.site.register(UsePositionStatus)

# admin.site.register(Sponsor)

class ProfileAdmin(admin.ModelAdmin):
    list_display  = ['full_name','mobile_no']
    # readonly_fields = ['current_wallet','registration_wallet','sponsor_wallet','founder_wallet']

class PackageAdmin(admin.ModelAdmin):
    list_display  = ['display_package_name','package_amount']
    readonly_fields = ['package_name']
    
admin.site.register(Package,PackageAdmin)

class SponsorAdmin(admin.ModelAdmin):
    list_display = ['sponsor','reg_user']
    # readonly_fields = ['current_wallet','registration_wallet','sponsor_wallet','founder_wallet'] 

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Sponsor, SponsorAdmin)