from django.db import models
from django.contrib.auth.models import User, auth
from django.db.models.signals import pre_save, post_delete
from django.conf import settings
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from datetime import datetime
# Create your models here.

class Notice(models.Model):

    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notice_title= models.CharField(max_length=200, null=True, blank=False)
    notice_body= models.TextField(null=True, blank=False)
    notice_document= models.FileField(upload_to='notice/documents/', blank=True, null=True)
    notice_date= models.DateTimeField(auto_now_add=True)
    slug= models.SlugField(blank=True, unique=True, allow_unicode=True)

    def __str__(self):
        return self.notice_title


@receiver(post_delete, sender=Notice)
def notice_delete(sender, instance, **kwargs):
    instance.notice_document.delete(False)

def pre_save_notice(sender, instance, **kwargs):
    if not instance.slug:
        now = datetime.now()
        month = now.strftime("%m")
        day = now.strftime("%d")
        year = now.strftime("%Y")
        time = now.strftime("%H:%M:%S")
        instance.slug= slugify(time+"-"+day+"-"+month+"-"+year+"-"+instance.notice_title)

pre_save.connect(pre_save_notice, sender=Notice)


# LIBRARY MODEL
class Library(models.Model):

    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book_title= models.CharField(max_length=200, null=True, blank=False)   
    book_writter= models.CharField(max_length=200, null=True, blank=True)   
    book_subject= models.CharField(max_length=200, null=True, blank=True)   
    book_description= models.TextField(null=True, blank=False) 
    book_file= models.FileField(upload_to='library/books/', blank=True, null=True)
    book_img= models.ImageField(upload_to='library/img/', blank=True, null=True)
    book_adding_date= models.DateTimeField(auto_now_add=True)
    slug= models.SlugField(blank=True, unique=True, allow_unicode=True)

    def __str__(self):
        return self.book_title


@receiver(post_delete, sender=Library)
def library_delete(sender, instance, **kwargs):
    instance.book_file.delete(False)
    instance.book_img.delete(False)

def pre_save_library(sender, instance, **kwargs):
    if not instance.slug:
        now = datetime.now()
        month = now.strftime("%m")
        day = now.strftime("%d")
        year = now.strftime("%Y")
        time = now.strftime("%H:%M:%S")
        instance.slug= slugify(time+"-"+day+"-"+month+"-"+year+"-"+instance.book_title)

pre_save.connect(pre_save_library, sender=Library)

# GALERRY
class Gallery(models.Model):

    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo_title= models.CharField(max_length=200, null=True, blank=False)
    img= models.ImageField(upload_to='gallery/', blank=False)


    def __str__(self):
        return self.photo_title


@receiver(post_delete, sender=Gallery)
def gallery_delete(sender, instance, **kwargs):
    instance.gallery.delete(False)




