from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from myapp.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import Http404

from django.db.models import Q 

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            messages.warning(request, "Both username and password are required")
            return render(request, "admin_panel/pages_login.html")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)  # Ensure user is logged in
            if user.usertype == 'job_admin':
                messages.success(request, "Login Successfully")
                return redirect("main_admin")  # Use URL name for redirection

            elif user.usertype == "Job_seckeer":
                messages.success(request, "Login Successfully")
                return redirect("homePage")
        else:
            messages.warning(request, "Invalid username or password")

    return render(request, "admin_panel/pages_login.html")



def signupPage(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        usertype = request.POST.get("usertype")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not all([username, email, usertype, password, confirm_password]):
            messages.warning(request, "All fields are required")
            return render(request, "admin_panel/pages_register.html")

        try:
            validate_email(email)
        except ValidationError:
            messages.warning(request, "Invalid email format")
            return render(request, "admin_panel/pages_register.html")

        if password != confirm_password:
            messages.warning(request, "Passwords do not match")
            return render(request, "admin_panel/pages_register.html")

        if len(password) < 8:
            messages.warning(request, "Password must be at least 8 characters long")
            return render(request, "admin_panel/pages_register.html")

        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            messages.warning(request, "Password must contain both letters and numbers")
            return render(request, "admin_panel/pages_register.html")

        try:
            user = Custom_User.objects.create_user(
                username=username,
                email=email,
                usertype=usertype,
                password=password
            )
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("loginPage")
        except IntegrityError:
            messages.warning(request, "Username or email already exists")
            return render(request, "admin_panel/pages_register.html")

    return render(request, "admin_panel/pages_register.html")


def logoutPage(request):


    logout(request)
    messages.success(request, "You have been logged out successfully.")
    
    
    return redirect("homePage")

def homePage(request):
    
    
    return render(request,"index.html")

def about(request):
    
    
    return render(request,"common/about.html")

@login_required
def blog(request):
   
    
    return render(request,"common/blog.html")
@login_required
def contact(request):
    
    
    return render(request,"common/contact.html")


def createBasicInfo(request):
    if request.user.usertype == 'Job_seckeer':
        current_user = request.user
        
        if request.method == 'POST':
            resume, created = Profile_Info.objects.get_or_create(user=current_user)
            
            resume.contact_No = request.POST.get("contact_No")
            resume.Designation = request.POST.get("Designation")
            resume.Profile_Pic = request.FILES.get("Profile_Pic")
            resume.Carrer_Summary = request.POST.get("Carrer_Summary")
            resume.Age = request.POST.get("Age")
            resume.Gender = request.POST.get("Gender")
            resume.save()
            
            current_user.first_name = request.POST.get("first_name")
            current_user.last_name = request.POST.get("second_name")
            current_user.save()
            
            messages.success(request, "Resume created successfully.")
            return redirect('MySettingsPage')  
        
        return render(request, "createBasicInfo.html")
    elif request.user.usertype == 'job_admin':
        messages.warning(request, "You are not authorized to access this page.")
        return render(request, "createBasicInfo.html") 
def admin_basic_info(request):
    if request.user.usertype == 'job_admin':
        user = request.user
        
        if request.method == 'POST':
            print("POST request received")
            profile, created = Profile_Info.objects.get_or_create(user=user)
            print("Profile retrieved or created:", profile)
            
            profile.Profile_Pic = request.FILES.get("Profile_Pic")
            profile.fullName = request.POST.get("fullName")
            profile.about = request.POST.get("about")
            profile.profession = request.POST.get("profession")
            profile.location = request.POST.get("location")
            profile.date_of_birth = request.POST.get("date_of_birth")
            profile.gender_type = request.POST.get("gender_type")
            profile.phone_number = request.POST.get("phone_number")
            profile.twitter_url = request.POST.get("twitter")
            profile.facebook_url = request.POST.get("facebook")
            profile.instagram_url = request.POST.get("instagram")
            profile.linkedin_url = request.POST.get("linkedin")

            profile.save()
            print("Profile saved")

            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            
            if not first_name or not last_name:
                messages.error(request, "First name and last name are required.")
                return render(request, "admin_panel/admin_basic_info.html")

            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            print("User details saved")

            messages.success(request, "Profile updated successfully.")
            return redirect('admin_profile')
        
        return render(request, "admin_panel/admin_basic_info.html")
    else:
        messages.warning(request, "You are not authorized to access this page.")
        return render(request, "admin_panel/admin_basic_info.html")


def job_details(request, job_id):
    job_post = get_object_or_404(Jobpost, id=job_id)  # Retrieve the job post or return 404 if not found

    context = {
        'job_post': job_post,
    }
  
    return render(request,"common/job_details.html",context)
def job_listing(request):
    jobs = Jobpost.objects.all()  # Fetch all jobs

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Only fetch applied jobs if the user is authenticated
        applied_jobs = JobApplication.objects.filter(user=request.user).values_list('job_id', flat=True)
    else:
        applied_jobs = []  # If not authenticated, return an empty list

    context = {
        'jobs': jobs,
        'applied_jobs': applied_jobs,  # Pass the list of applied job IDs to the template
    }

    return render(request, "common/job_listing.html", context)
def single_blog(request):

    
    
    return render(request,"common/single_blog.html")





def blog_post(request):
    if request.user.usertype == 'Job_seckeer' :




        return render(request,"common/blog_post.html")
    else:
        return HttpResponse("You are not authorized to access this page")

@login_required
def profile(request):
    if request.user.usertype == 'Job_seckeer' :
        return render(request,"common/profile.html")
    
   
    
    else:
        return HttpResponse("You are not authorized to access this page")
@login_required
def admin_profile(request):
    if request.user.usertype == 'job_admin' :
        return render(request,"admin_panel/admin-profile.html")
    
   
    
    else:
        return HttpResponse("You are not authorized to access this page")

    



@login_required
def main_admin(request):
    if request.user.usertype == 'job_admin':

        
        return render( request,"admin_panel/main_admin.html")
    else:
        return HttpResponse("You are not authorized to access this page")





@login_required
def job_post(request):
    if request.user.usertype == 'job_admin':

        if request.method == 'POST':
            # Create a new Jobpost instance and populate it with form data
            job_post = Jobpost(
                job_titel=request.POST.get('job_title'),
                company_name=request.POST.get('com_name'),
                company_email=request.POST.get('com_email'),
                company_web=request.POST.get('com_web'),
                company_location=request.POST.get('com_location'),
                company_logo=request.FILES.get('com_logo'),  # Handle file upload
                sallary=request.POST.get('Salary'),
                job_description=request.POST.get('job_Description'),
                required_knowledge=request.POST.get('Required_Knowledge_Skills_and_Abilities'),
                Education_Experience=request.POST.get('Education_Experience'),
                post_date=request.POST.get('post_date'),
                Application_date=request.POST.get('Application_date'),
                Vacancy=request.POST.get('vacancy'),
                job_type=request.POST.get('job_type')  # Ensure this handles single selection
            )
            
            # Save the job post to the database
            job_post.user = request.user  # Assign the logged-in user to the job post
            job_post.save()

            return redirect('job_listing')  # Redirect to a success page or job listing page
        
        return render(request, 'admin_panel/job_post.html')  # Render the form template if GET request

    else:
        messages.warning(request, "You are not authorized to access this page")

@login_required
def edit_job_post(request, job_id):
    job_post = get_object_or_404(Jobpost, id=job_id)  # Get the job post or return a 404 if not found

    if request.method == 'POST':
        # Update the Jobpost instance with form data
        job_post.job_titel = request.POST.get('job_title')
        job_post.company_name = request.POST.get('com_name')
        job_post.company_email = request.POST.get('com_email')
        job_post.company_web = request.POST.get('com_web')
        job_post.company_location = request.POST.get('com_location')
        
        if request.FILES.get('com_logo'):
            job_post.company_logo = request.FILES.get('com_logo')  # Update only if a new file is uploaded
        
        job_post.sallary = request.POST.get('Salary')
        job_post.job_description = request.POST.get('job_Description')
        job_post.required_knowledge = request.POST.get('Required_Knowledge_Skills_and_Abilities')
        job_post.Education_Experience = request.POST.get('Education_Experience')
        job_post.post_date = request.POST.get('post_date')
        job_post.Application_date = request.POST.get('Application_date')
        job_post.Vacancy = request.POST.get('vacancy')
        job_post.job_type = request.POST.get('job_type')  # Ensure this handles single selection

                                  
        job_post.save()  # Save the updated job post to the database
        
        return redirect('job_listing')  # Redirect to the job listing page or any other page

    context = {
        'job_post': job_post}  # Pass the current job post to the template for pre-filling the form

    return render(request, 'admin_panel/Jobs_editors.html', context)  # Render the edit form template


@login_required
def delete_job_post(request, job_id):
    Job = get_object_or_404(Jobpost, id=job_id, user=request.user)
    Job.delete()
    messages.success(request, 'Job deleted successfully.')
    return redirect('job_listing')

@login_required
def apply_job(request,job_id):
    if request.user.usertype == 'Job_seckeer':
        job_post = get_object_or_404(Jobpost, id=job_id)
        if request.method == 'POST':
            
            resume = request.FILES.get('resume'),
            apply_date = request.FILES.get('apply_date'),
            cover_letter = request.FILES.get('cover_letter'),
            application = JobApplication(
                user=request.user,
                job=job_post,
                resume=resume,
                cover_letter=cover_letter,
                applied_on=apply_date)
            application.save()
            return redirect('job_listing')

        return render(request,'common/applyjobs.html',{'job_post': job_post})
            
    
    else:
        messages.warning(request, "You are not authorized to access this page")

    

@login_required
def users_profile(request):
    if request.user.usertype == 'job_admin':

        
        return render( request,"admin_panel/users-profile.html")
    else:
        return HttpResponse("You are not authorized to access this page")



@login_required
def pages_contact (request):
    if request.user.usertype == 'job_admin':

        
        return render( request,"admin_panel/pages-contact.html")
    else:
        return HttpResponse("You are not authorized to access this page")



