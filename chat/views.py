from django.contrib.messages.context_processors import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import ChatGroup, GroupMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from django.http import JsonResponse


# Create your views here.
@login_required
def home_view(request):
    """ вюшка главной страницы """
    user = User.objects.exclude(id=request.user.id)
    return render(request, 'home.html', {'users':user} )

def chat_view(request, user_id):
    """ вюшка чата """
    receiver = get_object_or_404(User, id=user_id)

    messages = Message.objects.filter(
        sender=request.user,
        receiver=receiver
    ) | Message.objects.filter(
        sender=receiver,
        receiver=request.user
    ).order_by('timestamp')


    return render(request, 'chat.html', {'receiver':receiver, 'messages':messages})

@login_required
def mark_as_read(request, username):
    user = request.user

    sender = User.objects.get(username=username)
    messages = Message.objects.filter(sender=sender, receiver=user, is_read=False)



    return JsonResponse({'status': 'ok'})


@login_required
def get_unread_counts(request):
    user = request.user

    message = Message.objects.filter(receiver=user, is_read=False)
    counts = {}

    for m in message:
        sender = m.sender.username
        counts[sender] = counts.get(sender, 0) + 1

    return JsonResponse(counts)





