from django.contrib import admin

from myapp.models import *

class Custom_User_Display(admin.ModelAdmin):
    list_display = ('username', 'email', 'usertype')
admin.site.register(Custom_User,Custom_User_Display)


class Jobpost_Display(admin.ModelAdmin):
    list_display = ('company_name', 'job_titel', 'job_type','sallary', 'post_date')
admin.site.register(Jobpost,Jobpost_Display)




admin.site.register(Profile_Info)
admin.site.register(JobApplication)
admin.site.register(UserProfile)
admin.site.register(AdminProfile)


