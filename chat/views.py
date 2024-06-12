from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatModel


@login_required(login_url='login/')
def index(request):
    chat_rooms = ChatModel.objects.filter(members=request.user)
    return render(request, "chat/index.html", {"chat_rooms": chat_rooms})


@login_required(login_url='login/')
def room(request, room_name):
    chat = ChatModel.objects.filter(room_name=room_name)
    if chat.exists():
        chat[0].members.add(request.user)
    else:
        new_chat = ChatModel.objects.create(room_name=room_name)
        new_chat.members.add(request.user)

    context = {
        "room_name": room_name,
    }
    return render(request, "chat/room.html", context)
