from django.shortcuts import render, get_list_or_404
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .forms import UserRegisterationForm
from django.contrib.auth import authenticate, login
from .models import User, Notification
from django.http import JsonResponse


class UserRegisterationView(FormView):
    form_class = UserRegisterationForm
    template_name = 'accounts/register.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        cleaned_data = form.cleaned_data
        user = authenticate(
            request=self.request, email=cleaned_data['email'], password=cleaned_data['password2']
        )
        if user:
            login(self.request, user)
        return super().form_valid(form)

class UserDetialView(TemplateView):
    template_name = 'accounts/user-detail.html'

    def get_context_data(self, **kwargs):
        
        kwargs = super().get_context_data(**kwargs)

        user_id = self.kwargs.get('user_id')

        requested_user = User.objects.filter(id=user_id)

        if requested_user.exists():

            kwargs['requested_user'] = requested_user.first()

        return kwargs

def set_notficiatons_seen(request):

    if request.is_ajax():

        if request.method == 'POST':

            user = request.user
            data = request.POST

            last_notification_id = data['id']
            notifications_num = int(data['loadedNotificationsCount'])
            
            last_read_notification = user.received_notifications.filter(
                id=last_notification_id
            ).first()

            if last_read_notification:

                seen_notifications = user.received_notifications.filter(
                    created_at__lte=last_read_notification.created_at,
                    seen=False
                )[:notifications_num]
                
                for n in seen_notifications:
                    n.seen = True
                    n.save()

                return JsonResponse({})

    return JsonResponse(
        data={},
        status=400
    )
