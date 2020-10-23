from django.template import Library
from conversations.models import MessageRequest


register = Library()


@register.filter
def relation_status(user, target_user):

    sent_request = MessageRequest.objects.filter(
        user_from=user, user_to=target_user
    ).first()

    if sent_request:
        if sent_request.status == 'PEN':
            return 'pending'
        else:
            return 'friend'

    received_request = MessageRequest.objects.filter(
        user_from=target_user, user_to=user
    ).first()

    if received_request:
        if received_request.status == 'PEN':
            return 'accept'
        else:
            return 'friend'

    return 'message-request'



@register.filter
def get_other_side(thread, current_user):
        
    return thread.users.exclude(id=current_user.id).first()

@register.filter
def has_unseen_message(thread, user):

    last_received_message = thread.messages.exclude(sender=user).last()

    if last_received_message:

        return last_received_message.status != 'SEN'
        
    return False
    


