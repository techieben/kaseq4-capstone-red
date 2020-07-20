from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from django.views.generic import View
from notification.models import Notification


# Create your views here.
@login_required
def NotificationView(request):
    html = 'notifications.html'
    notifications = Notification.objects.filter(user_to=request.user)

    # for notification in notifications:
    #     notification.delete()

    return render(request, html, {
        'notifications': notifications
    })
