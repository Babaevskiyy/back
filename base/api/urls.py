from django.urls import path 
from . import views
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', views.getRoutes),
    path('notes/', views.getNotes),
    path('notes/add/', views.addNote),
    path('notes/update/<int:pk>/', views.updateNote),
    path('notes/delete/<int:pk>/', views.deleteNote),

    path('educational_organizations/', views.EducationalOrganization_ListView),
    path('educational_organizations/<int:pk>/', views.EducationalOrganization_DetailView),

    path('subdivisions/', views.Subdivisions_ListView),
    path('subdivisions/<int:pk>/', views.Subdivision_DetailView),

    path('activities/', views.Activity_ListView),
    path('activities/<int:pk>/', views.Activity_DeatailView),

    path('practices/', views.Practice_ListView),
    path('practices/<int:pk>/', views.Practice_DetailView),

    path('moderators/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('moderators/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]