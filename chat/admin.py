from django.contrib import admin
from .models import Posts,Profile
# Register your models here.


class PostsAdmin(admin.ModelAdmin):
    filter_horizontal =('user',)

admin.site.register(Posts,PostsAdmin)
admin.site.register(Profile)
 