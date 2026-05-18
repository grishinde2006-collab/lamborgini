
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Comment


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Телефон'
    fields = ('phone',)

class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ('username', 'email', 'phone_display', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'profile__phone')
    
    def phone_display(self, obj):
        """Отображаем телефон из профиля"""
        try:
            # Пробуем получить профиль
            profile = UserProfile.objects.get(user=obj)
            return profile.phone if profile.phone else '-'
        except UserProfile.DoesNotExist:
            return '-'
        except Exception:
            return '?'
    phone_display.short_description = 'Телефон'
    phone_display.admin_order_field = 'profile__phone'

# Перерегистрируем User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')
    search_fields = ('user__username', 'phone')



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'text')