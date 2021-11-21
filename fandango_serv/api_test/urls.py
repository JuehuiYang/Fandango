from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('file_upload/', views.file_upload, name='upload')
]
