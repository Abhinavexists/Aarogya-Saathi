from django.urls import path
from .views import signup_view, login_view, login_view, home_view, chat_view
from django.views.generic import TemplateView


urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('chat/', chat_view, name='chat'),
    path('', home_view, name='home'),
]
