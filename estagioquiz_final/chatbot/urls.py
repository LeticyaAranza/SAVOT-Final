from django.urls import path
from .views import conversar

urlpatterns = [path("conversar/", conversar, name="chatbot_conversar")]
