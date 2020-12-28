from django.urls import path
from user_webapp import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('forgot-password/', views.ForgotPassView.as_view(), name="forgot-password"),
    path('enter-forgot-otp/', views.EnterForgotOtp.as_view(), name="enter-forgot-otp"),
    path('resend-forgot-otp/', views.ResendForgotOtp.as_view(), 
    name="resend-forgot-otp"),
    path('recover-password/', views.RecoverPassView.as_view(), name="recover-password"),
    path('reset-password/', views.ResetPassView.as_view(), name="reset-password"),
    path('enter-reset-otp/', views.EnterResetOtp.as_view(), name="enter-reset-otp"),
    path('resend-reset-otp/', views.ResendResetOtp.as_view(), 
    name="resend-reset-otp"),
    path('recover-new-password/', views.RecoverNewPassView.as_view(), name="recover-new-password"),
    path('post-a-job/', views.PostAJobView.as_view(), name="post-a-job"),
    path('jobs-search-list/', views.JobSearchlistView.as_view(), name="jobs-search-list"),
    # path('jobs-search-list/<int:id>/', views.JobSearchlistView.as_view(), name="jobs-search-listid"),
    path('job-detail/', views.JobDetailView.as_view(), name="job-detail"),
    path('user-profile/', views.UserProfileView.as_view(), name="user-profile"),
    path('how-it-works/', views.HowItWorksView.as_view(), name="how-it-works"),
    path('blogs/', views.BlogsView.as_view(), name='blogs'),
    path('blog-detail/', views.BlogDetailView.as_view(), name="blog-detail"),
]
