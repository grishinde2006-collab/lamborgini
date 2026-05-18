from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import redirect
import os

SERVICE_ROLE = os.environ.get('SERVICE_ROLE', 'full')

# ========== ГЛАВНЫЕ СТРАНИЦЫ ==========

def full_home(request):
    from main import views
    return views.index(request)

def auth_home(request):
    from main import views
    return views.login_user(request)

def comments_home(request):
    from main import views
    return views.comments_page(request)

# Выбор главной страницы по роли
if SERVICE_ROLE == 'auth':
    home_view = auth_home
elif SERVICE_ROLE == 'comments':
    home_view = comments_home
else:
    home_view = full_home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='index'),
]

# ========== URL ДЛЯ КАЖДОГО СЕРВИСА ==========

if SERVICE_ROLE == 'full':      # Порт 8000
    from main import views
    urlpatterns += [
        path('lastyear/', views.lastyear, name='lastyear'),
        path('login/', views.login_user, name='login'),
        path('logout/', views.logout_user, name='logout'),
        path('register-user/', views.register_user, name='register_user'),
        path('comments/', views.comments_page, name='comments'),
        path('api/comments/', views.comment_list, name='comment_list'),
        path('api/comments/add/', views.comment_add, name='comment_add'),
        path('api/comments/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    ]

elif SERVICE_ROLE == 'auth':    # Порт 8001
    from main import views
    urlpatterns += [
        path('login/', views.login_user, name='login'),
        path('logout/', views.logout_user, name='logout'),
        path('register-user/', views.register_user, name='register_user'),
    ]

elif SERVICE_ROLE == 'comments': # Порт 8002
    from main import views
    urlpatterns += [
        path('comments/', views.comments_page, name='comments'),
        path('api/comments/', views.comment_list, name='comment_list'),
        path('api/comments/add/', views.comment_add, name='comment_add'),
        path('api/comments/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    ]