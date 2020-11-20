from django.contrib import admin
from .models import Post, Comments, Project, FSI_user
# Register your models here.

admin.site.register(FSI_user),
admin.site.register(Project),
admin.site.register(Post),
admin.site.register(Comments),

