from django.db import models
from django.contrib.auth.models import User as UserModel


class ChatModel(models.Model):
    room_name = models.CharField(max_length=100)
    members = models.ManyToManyField(UserModel, null=True, blank=True)

    def __str__(self):
        return self.room_name


class MessageModel(models.Model):
    auther = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.TextField()
    chat = models.ForeignKey(ChatModel, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    @property
    def auther_username(self):
        return self.auther.username

    def __str__(self):
        return f'{self.auther}: {self.content[:20]} at {self.date}'
