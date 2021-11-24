from django.urls import path

from . import views

urlpatterns = (
    path('', views.index, name='index'),
    path('keyword/', views.upload_keyword, name='keyword'),
    path('frequency/', views.get_frequency, name='frequency'),
    path('file/', views.upload_file, name='upload_file'),
    path('result/', views.download, name='upload_file'),
)
