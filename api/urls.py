from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('login', views.login),
    path('logout', views.Logout.as_view()),
    path('follow/<int:pk>/', views.FollowView.as_view({'post': 'follow'})),
    path('unfollow/<int:pk>/', views.FollowView.as_view({'post': 'unfollow'})),
]

urlpatterns = format_suffix_patterns(urlpatterns)