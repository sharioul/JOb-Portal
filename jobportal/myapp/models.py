from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Custom_User(AbstractUser):
    
    USER=[
        ('job_admin','Job_Admin'),
        ('Job_seckeer','Job_seckeer')
    ]
    
    usertype=models.CharField(choices=USER,null=True,max_length=100)
    check_box=models.BooleanField(default=False ,null=True)
    
    def __str__(self):
        return f"{self.username}- {self.first_name}- {self.last_name}"

class Jobpost(models.Model):
    
    user=models.ForeignKey("Custom_User", on_delete=models.CASCADE,null=True)
    job_titel=models.CharField(max_length=250,null=True,blank=True)
    company_name=models.CharField(max_length=100,null=True,blank=True)

    jobs=[
        ('fulltime','FullTime'),
        ('parttime','PartTime')
    ]
    
    job_type=models.CharField(choices=jobs,null=True,max_length=100,blank=True)
    post_date= models.DateField(null=True,blank=True)
    company_logo=models.ImageField(upload_to="Media/Profile_Pic",null=True,)
    company_location=models.CharField(max_length=50,null=True,blank=True)
    sallary=models.PositiveIntegerField(null=True,blank=True)
    
    Application_date=models.DateField(null=True,blank=True)
    job_description=models.TextField(null=True,blank=True)
    required_knowledge=models.TextField(null=True,blank=True)
    Education_Experience=models.TextField(null=True,blank=True)
    company_web=models.URLField(max_length=200,null=True,blank=True)
    company_email=models.EmailField(max_length=254,null=True,blank=True)
    Vacancy=models.CharField( max_length=50,null=True,blank=True)

    
    def __str__(self) -> str:

        return f"{self.company_name}"
class JobApplication(models.Model):
    job = models.ForeignKey(Jobpost, on_delete=models.CASCADE)
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(null=True,blank=True)
    applied_on = models.DateTimeField(auto_now_add=True,blank=True)

    
    def __str__(self):
        return f"{self.user.username} applied for {self.job.job_titel}"

class Profile_Info(models.Model):
    user = models.OneToOneField(Custom_User, null=True, on_delete=models.CASCADE)
    Profile_Pic = models.ImageField(upload_to="Media/Profile_Pic", null=True)
    fullName=models.CharField(max_length=250,null=True,blank=True)
    about=models.TextField(null=True,blank=True)
    profession=models.CharField(max_length=250,null=True,blank=True)
    location=models.CharField(max_length=250,null=True,blank=True)
    phone_number=models.CharField(max_length=15,null=True,blank=True)
    date_of_birth=models.DateField(null=True,blank=True)
    Gender=[
        ('male','Male'),
        ('female','Female'),
        ('other','Other')
    ]
    gender_type=models.CharField(choices=Gender,null=True,blank=True, max_length=50)
    twitter_url=models.URLField(null=True,blank=True,max_length=200)
    facebook_url=models.URLField(null=True,blank=True,max_length=200)
    instagram_url=models.URLField(null=True,blank=True,max_length=200)
    linkedin_url=models.URLField(null=True,blank=True,max_length=200)



class UserProfile(models.Model):
    user = models.OneToOneField(Custom_User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    job = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email_notifications = models.BooleanField(default=True)
    about = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)

    def __str__(self):
        return self.user.username


class AdminProfile(models.Model):
    user = models.OneToOneField(Custom_User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    job = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email_notifications = models.BooleanField(default=True)
    about = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)

    def __str__(self):
        return self.user.username
