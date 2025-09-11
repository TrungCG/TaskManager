from django.contrib import admin

from .models import User, Category, Task, TaskFile, Tag, TaskTag

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(TaskFile)
admin.site.register(Tag)
admin.site.register(TaskTag)