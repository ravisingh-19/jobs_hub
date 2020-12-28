from django.conf import settings
from django.core.mail import send_mail 
from django.shortcuts import render, redirect
from common_webapp.models import Account
from .models import *
from admin_webapp.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, 'user_webapp/index.html')
    
class RegisterView(View):
    def get(self, request):
        return render(request, 'user_webapp/register.html')
    
    def post(self, request):
        register_user_exist = Account.objects.filter(email=request.POST.get('email'))
        if register_user_exist:
            messages.info(request, 'Email id already exist please use another email id')
            return redirect('register')
        else:
            register_obj = Account()
            register_obj.account_type = request.POST.get('account_type')
            username = request.POST.get('name')
            register_obj.name = username
            register_obj.email = request.POST.get('email')
            register_obj.countrycode = request.POST.get('countrycode')
            register_obj.is_active = True
            register_obj.set_password(request.POST.get('password'))
            register_obj.profile_photo = request.POST.get('profile_photo')
            register_obj.save()
            messages.success(request, f'Registration was successful {username}!')
            return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'user_webapp/login.html')
    
    def post(self, request):
        em = request.POST.get('email')
        pw = request.POST.get('password')
        active_user = Account.objects.filter(email=em).first()
        user = authenticate(request, email=em, password=pw)
        if user is not None:
            request.session['email'] = em
            login(request, user)
            # messages.success(request, f'Welcome {active_user.name}!!')    
            return redirect('index')
        elif(active_user is not None):
            messages.error(request, f'You are entered wrong password!')
            return redirect('login')
        else:
            messages.error(request, f'This user is not exist')
            return redirect('login')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')

class ForgotPassView(View):
    def get(self, request):
        return render(request, 'user_webapp/forgot-password.html')
    
    def post(self, request):
        em = request.POST.get('email')
        user_exist = Account.objects.filter(email=em)
        if user_exist:
            active_user_exist = Account.objects.get(email=em)
            if active_user_exist.is_active == True:
                request.session['email'] = em
                active_user_exist.send_otp()
                active_user_exist.save()
                
                otp = active_user_exist.otp
                subject = "Django mails!"
                message = f'http://127.0.0.1:8000/enter-forgot-otp/?otp={otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [em,]
                send_mail(subject, message, email_from, recipient_list)
                
                messages.success(request, f'Otp sent to the e-mail!')
                return redirect('forgot-password')
        else:
            messages.info(request, 'please contact to the owner')
            return redirect('login')

class EnterForgotOtp(View):
    def get(self, request):
        otp = request.GET.get('otp')
        return render(request, 'user_webapp/enter-forgot-otp.html', {'otp':otp})
    
    def post(self, request):
        user = Account.objects.get(email=request.session['email'])
        if user.otp == request.POST.get('otp'):
            current_time = datetime.now(timezone.utc)
            sent_time = user.otp_created
            time_difference = current_time - sent_time
            if(time_difference.total_seconds() <= 30):
                return redirect('recover-password')
            else:
                user.otp = 'None'
                user.save()
                return redirect('enter-forgot-otp')
        else:
            return redirect('enter-forgot-otp')
                
class ResendForgotOtp(View):
    def get(self, request):
        return redirect('forgot-password')
    

class RecoverPassView(View):
    def get(self, request):
        if 'email' in request.session:
            return render(request, 'user_webapp/recover-password.html')
        return redirect('forgot-password')
    
    def post(self, request):
        user = Account.objects.get(email=request.session['email'])
        if request.POST.get('password1') == request.POST.get('password2'):
            user.set_password(request.POST.get('password1'))
            user.save()
            del request.session['email']
            messages.success(request, 'Your password successfully recovered!')
            return redirect('login')        
        else:
            messages.error(request, 'Your password does not match!')
            return redirect('recover-password')

class ResetPassView(View):
    def get(self, request):
        return render(request, 'user_webapp/reset-password.html')

    def post(self, request):
        em = request.POST.get('email')
        user_exist = Account.objects.filter(email=em)
        if user_exist:
            active_user_exist = Account.objects.get(email=em)
            if active_user_exist.is_active==True:
                request.session['email'] = em
                active_user_exist.send_otp()
                active_user_exist.save()

                otp = active_user_exist.otp
                subject = "Django mails!"
                message = f'http://127.0.0.1:8000/enter-reset-otp/?otp={otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.POST.get('email'),]
                send_mail(subject, message, email_from, recipient_list)

                messages.success(request, f'Otp sent to the e-mail!')
                return redirect('reset-password')
        else:
            messages.info(request, 'please contact to the owner')
            return redirect('login')

class EnterResetOtp(View):
    def get(self, request):
        otp = request.GET.get('otp')
        return render(request, 'user_webapp/enter-reset-otp.html', {'otp':otp})
    
    def post(self, request):
        user = Account.objects.get(email=request.session['email'])
        if user.otp == request.POST.get('otp'):
            current_time = datetime.now(timezone.utc)
            sent_time = user.otp_created
            time_difference = current_time - sent_time
            if(time_difference.total_seconds() <= 30):
                return redirect('recover-new-password')
            else:                
                user.otp='None'
                user.save()
                return redirect('enter-reset-otp')               
        else:
            return redirect('enter-reset-otp')

class ResendResetOtp(View):
    def get(self, request):
        return redirect('reset-password')

class RecoverNewPassView(View):
    def get(self, request):
        return render(request, 'user_webapp/recover-new-password.html')

    def post(self, request):
        user = Account.objects.get(email=request.session['email'])
        print(user.check_password(request.POST.get('old_password')))
        if user.check_password(request.POST.get('old_password')):
            if request.POST.get('password1') == request.POST.get('password2'):
                user.set_password(request.POST.get('password1'))
                user.save()
                messages.success(request, 'Your password successfully changed!')
                return redirect('login')
        else:
            messages.error(request, 'Old password is wrong!')
            return redirect('recover-new-password')


class PostAJobView(View):
    def get(self, request):
        return render(request, 'user_webapp/post-a-job.html')
    
    def post(self, request):

        job_cat_obj = JobCategory()
        job_cat_obj.job_category_name = request.POST.get('job_cat')
        job_cat_obj.save()

        job_sub_obj = JobSubCategory()
        job_sub_obj.job_sub_category = request.POST.get('job_sub')
        job_sub_obj.save()

        job_post_obj = PostAJob()
        job_post_obj.job_type = request.POST.get('job_type')
        job_post_obj.job_title = request.POST.get('job_title')
        job_post_obj.company_name = request.POST.get('company_name')
        job_post_obj.age_limit = request.POST.get('age_limit')
        job_post_obj.uniform = request.POST.get('uniform')
        job_post_obj.pay_type = request.POST.get('pay_type')
        job_post_obj.pay_rate = request.POST.get('pay_rate')
        job_post_obj.date_of_birth = request.POST.get('date_of_birth')
        job_post_obj.no_of_openning = request.POST.get('no_of_openning')
        job_post_obj.location = request.POST.get('location')
        job_post_obj.location_instructor = request.POST.get('location_instructor')
        job_post_obj.parking = request.POST.get('parking')
        job_post_obj.break_time = request.POST.get('break_time')
        job_post_obj.bio = request.POST.get('bio')
        job_post_obj.preference = request.POST.get('preference')
        job_post_obj.appearance_preference = request.POST.get('appearance_preference')
        job_post_obj.gender = request.POST.get('gender')
        job_post_obj.view_applicants = request.POST.get('view_applicants')
        job_post_obj.save()

        return redirect('post-a-job')
    




class JobSearchlistView(View):
    def get(self, request):
        job_category_data = JobCategory.objects.all().order_by('id')
        custom_filter = {}
        if request.GET.get('jobcategory'):
            custom_filter.update({"job_category__job_category_value": request.GET.get('jobcategory')})
        info = PostAJob.objects.filter(**custom_filter).order_by('id')
        paginator = Paginator(info, 1)
        page_number = request.GET.get('page', 1)
        try:
            job_data = paginator.page(page_number)
        except PageNotAnInteger:
            job_data = paginator.page(1)
        except EmptyPage:
            job_data = paginator.page(paginator.num_pages)
        print('job_data:', job_category_data)
        
        return render(request, 'user_webapp/jobs-search-list.html', 
        {'job_category_data': job_category_data, 'job_data': job_data})

class JobDetailView(View):
    def get(self, request):
        return render(request, 'user_webapp/job-detail.html')

class UserProfileView(View):
    def get(self, request):
        return render(request, 'user_webapp/user-profile.html')
    
    def post(self, request):

        gernal_obj = GernalInfo()
        gernal_obj.first_name = request.POST.get('first_name')
        gernal_obj.middle_name = request.POST.get('middle_name')
        gernal_obj.last_name = request.POST.get('last_name')
        gernal_obj.zip_code = request.POST.get('zip_code')
        gernal_obj.date_of_birth = request.POST.get('dateOfbirth')
        gernal_obj.gender = request.POST.get('gender')
        gernal_obj.email = request.POST.get('email')
        gernal_obj.nationality = request.POST.get('nationality')
        gernal_obj.user_id_proof = request.POST.get('id_proof')
        gernal_obj.save()

        education_obj = EducationInfo()
        education_obj.education = request.POST.get('education')
        education_obj.course = request.POST.get('course')
        education_obj.university_name = request.POST.get('university_name')
        education_obj.college_name = request.POST.get('college_name')
        education_obj.course_type = request.POST.get('course_type')
        education_obj.passing_out_year = request.POST.get('passing_out_year')
        education_obj.grading_system = request.POST.get('grading_system')
        education_obj.save()

        experience_obj = ExperienceInfo()
        experience_obj.organisation_name = request.POST.get('org_name')
        experience_obj.position = request.POST.get('position')
        experience_obj.starting_date = request.POST.get('starting_date')
        experience_obj.ending_date = request.POST.get('ending_date')
        experience_obj.bio = request.POST.get('bio')
        experience_obj.upload_documents = request.POST.get('upload_documents')
        experience_obj.save()

        job_obj = JobPreference()
        job_obj.job_category = request.POST.get('job_category')
        job_obj.location_range = request.POST.get('area')
        job_obj.own_reliable_transportation = request.POST.get('transpotation')
        job_obj.preferred_pay_rate_for_different_job_positions = request.POST.get('pay')
        job_obj.save()

        cert_obj = CertificationInfo()
        cert_obj.title = request.POST.get('title')
        cert_obj.description = request.POST.get('description')
        cert_obj.image = request.POST.get('image')
        cert_obj.save()

        language_obj = Language()
        language_obj.lanuage = request.POST.get('language')
        language_obj.spoken = request.POST.get('spoken')
        language_obj.written = request.POST.get('written')
        language_obj.save()

        return redirect('user-profile')
        
class HowItWorksView(View):
    def get(self, request):
        return render(request, 'user_webapp/how-it-works.html')

class BlogsView(View):
    def get(self, request):
        custom_filter = {}
        if request.GET.get('category'):
            custom_filter.update({"blog_category__blog_category_value": request.GET.get('category')})
            print('custom_filter',custom_filter)
        blog_data = Blog.objects.filter(**custom_filter).order_by('id')
        page = request.GET.get('page', 1)
        paginator = Paginator(blog_data, 1)
        try:
            blog_data = paginator.page(page)
        except PageNotAnInteger:
            blog_data = paginator.page(1)
        except EmptyPage:
            blog_data = paginator.page(paginator.num_pages)
        
        blog_category=[]
        for i in BlogCategory.objects.all().order_by('id'):
              blog = Blog.objects.filter(blog_category=i).order_by('id')
              blog_category.append({
                "name": i.blog_category_name,
                "count": len(blog),
                "val": i.blog_category_value,
            })
        print("blo_data:", blog_data)
        return render(request, 'user_webapp/blogs.html', {'blog_data': blog_data, 'blog_category': blog_category})

class BlogDetailView(View):
    def get(self, request):
        return render(request, 'user_webapp/blog-detail.html')
               