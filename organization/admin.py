from organization.models import About, Contact, Marketing,Question,Package,CompanyAddress,TermsCondition,navbarSupportedContent,UserDashboardContent
from django.contrib import admin

# Register your models here.
admin.site.register(About)
admin.site.register(Marketing)
admin.site.register(Question)
admin.site.register(Package)
admin.site.register(Contact)
admin.site.register(CompanyAddress)
admin.site.register(TermsCondition)
admin.site.register(UserDashboardContent)
admin.site.register(navbarSupportedContent)