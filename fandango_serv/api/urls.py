from django.urls import path

from . import views

urlpatterns = {
    path('', views.index, name='index'),
    path('keyword/', views.upload_keyword, name='keyword'),
    path('file/', views.upload_file, name='upload_file'),
    path('result/', views.download, name='upload_file'),
    path('<int:id>/sourcefile/', views.get_source_file, name='source_file'),
    path('<int:id>/markedfile/', views.get_marked_file, name='marked_file'),
    path('<int:id>/content/', views.get_text, name='content'),
    path('<int:id>/rating/', views.get_rating, name='rate'),
}
