from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('user/', views.UserList.as_view()),
    path('all_posts/', views.PostList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('login/', views.AuthClass.as_view()),
    path('logout/', views.Logout.as_view()),
    path('post/',views.PostCreateView.as_view()),
    path('follow/<int:pk>/', views.FollowView.as_view({'post': 'follow'})),
    path('unfollow/<int:pk>/', views.FollowView.as_view({'post': 'unfollow'})),
    path('post/<int:pk>/', views.PostDetail.as_view()),
    path('like/<int:pk>/', views.LikeViewSet.as_view({'post': 'like'})),
    path('unlike/<int:pk>/', views.LikeViewSet.as_view({'delete': 'unlike'})),
    path('comment/<int:pk>/', views.CommentCreateView.as_view()),


]

urlpatterns = format_suffix_patterns(urlpatterns)