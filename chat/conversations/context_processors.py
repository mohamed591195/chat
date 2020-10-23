
def notifications_context(request):

    user = request.user

    if user.is_authenticated:

        unseen_notifications_exists = user.received_notifications.first(
        ) and not user.received_notifications.first().seen

        return {
            'notifications': user.received_notifications.all()[:8],
            'unseen_notifications_exists': unseen_notifications_exists
        }

    return {
        'notifications': [],
    }
