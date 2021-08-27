from django.urls import path
from . import views

# regular patterns

regular_patterns = [
    path('', views.HomeView.as_view(), name='home_view')
]

# ajax patterns
ajax_patterns = [
    path('send-message-request/', views.message_request,
         name='message_request_view'),

    path('thread-data/', views.get_thread_messages),
    path('threads-list/', views.get_threads)
]

urlpatterns = regular_patterns + ajax_patterns
