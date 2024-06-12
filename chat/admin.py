from django.contrib import admin
from .models import MessageModel, UserModel, ChatModel


admin.site.register(MessageModel)
admin.site.register(ChatModel)
