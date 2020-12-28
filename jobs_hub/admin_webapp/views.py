from django.shortcuts import render, redirect
from common_webapp.models import Account
from .models import Blog
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class dashboardView(View):
    def get(self, request):
        return render(request, 'admin_webapp/dashboard.html')

class DashLoginView(View):
    def get(self, request):
        return render(request, 'admin_webapp/dashboard-login.html')
    
    def post(self, request):
        em = request.POST.get('email')
        pw = request.POST.get('password')
        active_user = Account.objects.filter(email=em).first()
        user = authenticate(request, email=em, password=pw)
        if user is not None:
            request.session['email'] = em
            login(request, user)
            # messages.success(request, f'Welcome {active_user.name}!!')    
            return redirect('dashboard')
        elif(active_user is not None):
            messages.error(request, f'You are entered wrong password!')
            return redirect('dashboard-login')
        else:
            messages.error(request, f'This user is not exist')
            return redirect('dashboard-login')

class DashboardPagination(View):
    def get(self, request):
        return render(request, 'admin_webapp/dashboard-pagination.html')

class DashManageCompany(View):
    def get(self, request):
        return render(request, 'admin_webapp/dashboard-manage-company.html')

class DashManageUser(View):
    def get(self, request):
        return render(request, 'admin_webapp/dashboard-manage-users.html')

class DashMessages(View):
    def get(self, request):
        return render(request, 'admin_webapp/dashboard-messages.html')

class DashNotification(View):
    def get(self, request):
        return render(request, 'admin_webapp/dashboard-notification.html')

class DashManageBlog(View):
    def get(self, request):
        return render(request, 'admin_webapp/dashboard-manage-blogs.html')

class DashAddBlog(View):
    def get(self, request):
        return render(request, 'admin_webapp/dashboard-add-blog.html')

    def post(self, request):

        blog_obj = Blog()
        blog_obj.upload_feature_image = request.POST.get('feature_image')
        blog_obj.title = request.POST.get('title')
        blog_obj.paragraph_content = request.POST.get('editor')
        blog_obj.blog_category_name = request.POST.get('category')
        blog_obj.tags = request.POST.get('tags')
        blog_obj.author_name = request.POST.get('author_name')
        blog_obj.published_date = request.POST.get('published_date')
        blog_obj.save()
        return redirect('dashboard')

class DashSettings(View):
    def get(self, request):
        return render(request, 'admin_webapp/dashboard-settings.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('dashboard')