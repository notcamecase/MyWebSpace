from django.contrib import admin
from .models import Image,Post
# Register your models here.
class Filter(admin.ModelAdmin):
    list_display = ('title','document',)
    list_filter = ('post',)
    search_fields = ('title',)
    ordering = ('title',)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date',)
admin.site.register(Post,PostAdmin)
admin.site.register(Image,Filter)


