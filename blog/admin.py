from django.contrib import admin

from .models import Category, Tag, Post, Like, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
