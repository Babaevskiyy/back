from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('', views.StudentApplicationView),
    path('list/', views.StudentApplication_ListView),
    path('manage/<int:pk>/', views.ManageApplicationView),

    path('notification/', views.NotificationApplicationView),
    path('notification/list', views.NotificationApplication_ListView),
]