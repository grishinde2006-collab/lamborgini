from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Comment
from django.contrib.admin.views.decorators import staff_member_required
import json
import os

SERVICE_ROLE = os.environ.get('SERVICE_ROLE', 'full')

# URL сервисов из переменных окружения (с значениями по умолчанию)
FULL_URL = os.environ.get('FULL_SERVICE_URL', 'https://lamborgini-full.onrender.com')
AUTH_URL = os.environ.get('AUTH_SERVICE_URL', 'https://lamborgini-auth.onrender.com')
COMMENTS_URL = os.environ.get('COMMENTS_SERVICE_URL', 'https://lamborgini-comments.onrender.com')

def index(request):
    """Главная страница"""
    return render(request, 'main/index.html', {
        'FULL_URL': FULL_URL,
        'AUTH_URL': AUTH_URL,
        'COMMENTS_URL': COMMENTS_URL,
    })

def lastyear(request):
    """Страница 'Гранд-финал 2022'"""
    return render(request, 'main/lastyear.html', {
        'FULL_URL': FULL_URL,
        'AUTH_URL': AUTH_URL,
        'COMMENTS_URL': COMMENTS_URL,
    })

def register_user(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if not all([username, email, phone, password, password2]):
            messages.error(request, 'Пожалуйста, заполните все поля!')
            return redirect('register_user')
        
        if password != password2:
            messages.error(request, 'Пароли не совпадают!')
            return redirect('register_user')
        
        if len(password) < 6:
            messages.error(request, 'Пароль должен содержать не менее 6 символов!')
            return redirect('register_user')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким логином уже существует!')
            return redirect('register_user')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует!')
            return redirect('register_user')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={'phone': phone}
        )
        if not created:
            profile.phone = phone
            profile.save()
        
        messages.success(request, f'✅ Пользователь {username} успешно зарегистрирован!')
        
        # Редирект на главный сайт (полный URL)
        return redirect(f'{FULL_URL}/')
    
    return render(request, 'main/register_user.html', {
        'FULL_URL': FULL_URL,
        'AUTH_URL': AUTH_URL,
        'COMMENTS_URL': COMMENTS_URL,
    })

def login_user(request):
    """Вход пользователя"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'✅ Добро пожаловать, {user.username}!')
            # Редирект на главный сайт (полный URL)
            return redirect(f'{FULL_URL}/')
        else:
            messages.error(request, '❌ Неверный логин или пароль!')
            return redirect('login')
    
    return render(request, 'main/login.html', {
        'FULL_URL': FULL_URL,
        'AUTH_URL': AUTH_URL,
        'COMMENTS_URL': COMMENTS_URL,
    })

def logout_user(request):
    """Выход пользователя"""
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect(f'{FULL_URL}/')

def comments_page(request):
    """Страница с комментариями"""
    return render(request, 'main/comments.html', {
        'FULL_URL': FULL_URL,
        'AUTH_URL': AUTH_URL,
        'COMMENTS_URL': COMMENTS_URL,
    })

@login_required
def comment_list(request):
    """Получение списка комментариев в формате JSON"""
    comments = Comment.objects.all()[:50]
    data = {
        'comments': [
            {
                'id': c.id,
                'username': c.user.username,
                'text': c.text,
                'created_at': c.created_at.strftime('%d.%m.%Y %H:%M')
            }
            for c in comments
        ]
    }
    return JsonResponse(data)

@csrf_exempt
@require_http_methods(['POST'])
@login_required
def comment_add(request):
    """Добавление нового комментария"""
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        
        if not text:
            return JsonResponse({'error': 'Комментарий не может быть пустым'}, status=400)
        
        if len(text) > 500:
            return JsonResponse({'error': 'Комментарий слишком длинный (макс. 500 символов)'}, status=400)
        
        comment = Comment.objects.create(
            user=request.user,
            text=text
        )
        
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'username': comment.user.username,
                'text': comment.text,
                'created_at': comment.created_at.strftime('%d.%m.%Y %H:%M')
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Неверный формат данных'}, status=400)

@csrf_exempt
@require_http_methods(['DELETE'])
@staff_member_required
def comment_delete(request, comment_id):
    """Удаление комментария (только для администратора)"""
    try:
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return JsonResponse({'success': True})
    except Comment.DoesNotExist:
        return JsonResponse({'error': 'Комментарий не найден'}, status=404)
