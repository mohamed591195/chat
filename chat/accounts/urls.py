from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# regular patterns

regular_patterns = [
     path('register/', views.UserRegisterationView.as_view(), name='register_view'),
     path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'),
         name='login_view'),
     path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'),
         name='logout_view'),
     
     path('<int:user_id>/', views.UserDetialView.as_view(), name='user_detail_view')

]

# ajax patterns
ajax_patterns = [
     path('set-notifications-seen/', views.set_notficiatons_seen),

]

urlpatterns = regular_patterns + ajax_patterns
