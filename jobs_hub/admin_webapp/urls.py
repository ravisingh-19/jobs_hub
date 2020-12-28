from django.urls import path
from admin_webapp import views

urlpatterns = [
    path('', views.dashboardView.as_view(), name="dashboard"),
    path('dashboard-login/', views.DashLoginView.as_view(), name="dashboard-login"),
    path('admin-logout/', views.LogoutView.as_view(), name="admin-logout"),
    path('dashboard-pagination/', views.DashboardPagination.as_view(), name="dashboard-pagination"),
    path('dashboard-manage-company/', views.DashManageCompany.as_view(), name="dashboard-manage-company"),
    path('dashboard-manage-users/', views.DashManageUser.as_view(), name="dashboard-manage-users"),
    path('dashboard-messages/', views.DashMessages.as_view(), name="dashboard-messages"),
    path('dashboard-notification/', views.DashNotification.as_view(), name="dashboard-notification"),
    path('dashboard-manage-blogs/', views.DashManageBlog.as_view(), name="dashboard-manage-blogs"),
    path('dashboard-add-blog/', views.DashAddBlog.as_view(), name="dashboard-add-blog"),
    path('dashboard-settings/', views.DashSettings.as_view(), name="dashboard-settings"),

]
