def notifications_processor(request):
    if request.user.is_authenticated:
        latest_notifications = request.user.notifications.all()[:10]
        unread_count = request.user.notifications.filter(is_read=False).count()
        return {
            'latest_notifications': latest_notifications,
            'unread_notifications_count': unread_count,
        }
    return {}
