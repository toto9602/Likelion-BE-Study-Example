from django.contrib import admin

from .models import *

# admin.register decorator 사용 
# 목록에 표시할 필드를 정의하는 list_display만 사용했습니다.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('account', 'is_staff')


@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content',)

