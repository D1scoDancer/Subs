from django.urls import path

from . import views

urlpatterns = [
    path('uploaded/download', views.download, name='download'),
    path('uploaded/', views.uploaded, name='uploaded'),
    path('', views.index, name='index'),
]