from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from jobportal.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('loginPage',loginPage,name="loginPage" ),
    path('signupPage',signupPage,name="signupPage" ),
    path('logoutPage',logoutPage,name="logoutPage" ),
    path('',homePage,name="homePage" ),
    path('about',about,name="about" ),
    path('blog',blog,name="blog" ),
    path('contact',contact,name="contact" ),
    path('job_details/<int:job_id>/',job_details,name="job_details" ),
    path('job_listing',job_listing,name="job_listing" ),
    path('single_blog',single_blog,name="single_blog" ),
    path('blog_post',blog_post,name="blog_post" ),
    path('profile',profile,name="profile" ),
    path('createBasicInfo',createBasicInfo,name="createBasicInfo" ),
    path('admin_basic_info',admin_basic_info,name="admin_basic_info" ),
    path('main_admin',main_admin,name="main_admin" ),
    path('admin_profile',admin_profile,name="admin_profile" ),
    path('job_post',job_post,name="job_post" ),
    path('users_profile',main_admin,name="users_profile" ),
    path('pages_contact',pages_contact,name="pages_contact" ),
    path('edit_job_post/<int:job_id>', edit_job_post,name="edit_job_post" ),
    path('delete_job_post<int:job_id>', delete_job_post, name="delete_job_post" ),
    path('apply_job<int:job_id>',apply_job,name="apply_job" ),


    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
