from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lastyear/', views.lastyear, name='lastyear'),
    path('register-user/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('comments/', views.comments_page, name='comments'),
    path('api/comments/', views.comment_list, name='comment_list'),
    path('api/comments/add/', views.comment_add, name='comment_add'),
    path('api/comments/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
]


