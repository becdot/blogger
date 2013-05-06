from blog.models import Post
from django.contrib import admin
from django.contrib.auth.models import User

class DisplayUserPosts(admin.TabularInline):
    model = Post
    ordering = ['date']

# class UserAdmin(admin.ModelAdmin):
#     fields = ['username']
#     inlines = [DisplayUserPosts]
#     ordering = ['username']
#     search_fields = ['username']

class PostAdmin(admin.ModelAdmin):
    ordering = ['-date']
    list_filter = ['author', 'date']
    search_fields = ['title', 'content', 'date']

admin.site.register(Post, PostAdmin)