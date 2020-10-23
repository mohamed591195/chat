from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .decorators import is_ajax_authenticated_post
from .forms import SearchUsersForm
from django.contrib.auth import get_user_model
from django.db.models import Q
from .utils import send_notification, send_updated_message_status
from .models import Thread, Message
from .serializers import MessageSerializer


User = get_user_model()


class HomeView(LoginRequiredMixin, View):

    login_url = reverse_lazy('login_view')

    def get(self, request, *args, **kwargs):

        return render(request, 'conversations/home.html', {'form': SearchUsersForm()})

    def post(self, request, *args, **kwargs):

        form = SearchUsersForm(request.POST)

        users = []

        if form.is_valid():

            query = form.cleaned_data['query'].lower()

            users = User.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            ).exclude(id=request.user.id)

        return render(request, 'conversations/list-users.html', {'form': form, 'users': users})

@is_ajax_authenticated_post
def message_request(request):

    user = request.user

    data = request.POST
    data_to_return = {}

    user_id = data.get('userId')

    request_status = data.get('status')

    target_user = User.objects.filter(id=user_id).first()

    if not target_user:
        return JsonResponse(data={}, status=400)
    
    if request_status == 'message-request':
        
        # if the current user didn't receive previous request 
        # from target user he want to send request to
        if not user.received_message_requests.filter(user_from=target_user).exists():

            user.sent_message_requests.get_or_create(
                user_to=target_user
            )

            notification = target_user.received_notifications.create(
                sender=user, verb="message request"
            )

            send_notification(notification)

            data_to_return = {'status': 'created'}

    elif request_status == 'cancel':
        
        #  if the current request is pending, the only choice is to cancel it
        user.sent_message_requests.filter(
            user_to=target_user,
            status="PEN"
        ).delete()

        target_user.received_notifications.filter(
            sender=user, verb="message request", 
        ).delete()

        data_to_return = {'status': 'canceled'}

    elif request_status == 'accept':

        message_request = user.received_message_requests.filter(
            user_from=target_user,
            status="PEN",
        )

        if message_request.exists():

            message_request = message_request.first()
            message_request.status = "ACT"
            message_request.save()

            thread = user.threads.create()  
            thread.users.add(target_user)
            
            notification = target_user.received_notifications.create(
                sender=user, verb="accepted message request", 
            )

            send_notification(notification)

            data_to_return = {'status': 'accepted'}

    return JsonResponse(data_to_return)


def get_thread_messages(request):
    
    user = request.user

    if user.is_authenticated:
        
        data = request.GET

        thread_id = data.get('id')
        thread = Thread.objects.filter(id=thread_id).first()

        if thread:
            
            messages = thread.messages.exclude(Q(sender=user) | Q(status='SEN'))

            if messages.exists():
                
                for message in messages:
                    message.status = 'SEN'
                    message.viewers.add(user)
                    message.save()
    
                # we send the status of the last message so all of the above messages 
                # appears as sent 
                last_message = thread.messages.last()
                serialized_message = MessageSerializer(last_message)
                # we send the new status to message sender
                send_updated_message_status(last_message.sender, serialized_message)

            messages = MessageSerializer(thread.messages.all(), many=True)

            return JsonResponse({'messages': messages.data})

    return JsonResponse(data={}, status=400)


    

        
            
                