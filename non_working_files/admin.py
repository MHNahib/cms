from django.contrib import admin

from .models import Notice, Library, Gallery
# Register your models here.

admin.site.register(Notice)
admin.site.register(Library)
admin.site.register(Gallery)