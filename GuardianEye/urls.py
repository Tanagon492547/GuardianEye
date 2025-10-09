# GuardianEye/urls.py
from django.urls import path
from . import views # import views จากโฟลเดอร์เดียวกัน

urlpatterns = [
    path('', views.index, name='index'),
    path('video_feed/', views.video_feed, name='video_feed'),
]
