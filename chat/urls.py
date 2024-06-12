from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name="index"),
    path("chat/<str:room_name>/", views.room, name="room"),
    path('login/', LoginView.as_view(template_name='chat/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
