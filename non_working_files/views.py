from django.shortcuts import render
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.views.generic import ListView
from .models import Notice, Library, Gallery
from non_working_files.models import Notice, Library, Gallery
# Create your views here.

# index page
def index(request):

    # USER WILL GET EMAIL WHEN ANYONE FILLSUP THE FORM
    
    successful=False

    if request.method == 'POST':
        sub =  request.POST['sub']
        subject = "From Webapp Team <noreply@gmail.com> "
        msg =  request.POST['msg']
        email =  request.POST['user_email']
        name =  request.POST['user_name']
        send_msg =  msg+ "\n\nSent form: " + name +"\nEmail: "+ email + "\nSubject: "+ sub +"\nThank You" 
        
        # SEND TO ADMIN
        send_mail(
        subject,
        send_msg,
        settings.EMAIL_HOST_USER,
        ['mhnahib@gmail.com'],
        fail_silently=False,
        )

        # SEND TO USER
        send_mail(
        subject,
        'Thank you for your feedback.\nWe will contact you soon.',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
        )
        successful=True

    context= {'successful': successful}        


    return render(request, 'non-working-files/index.html', context)

# message1
def message1(request):
    return render(request, 'non-working-files/user1.html')

# message2
def message2(request):
    return render(request, 'non-working-files/user2.html')

# message3
def message3(request):
    return render(request, 'non-working-files/user3.html')

# HISTORY
def history(request):
    all_notice= all_notice= Notice.objects.all().order_by('-notice_date')[0:5]
    context= {'all_notice': all_notice}
    return render(request, 'non-working-files/history.html', context)

#  NOTICE BOARD
def notice(request):
       
    all_notice= Notice.objects.all().order_by('-notice_date')

    paginator = Paginator(all_notice, 10)
    page = request.GET.get('page')
 
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1) 

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)   

    context={'page':page,'posts':posts}   

    return render(request, 'non-working-files/notice.html', context)


#  LIBRARY
def library_book(request):
       
    books= Library.objects.all().order_by('-book_adding_date')

    paginator = Paginator(books, 12)
    page = request.GET.get('page')
 
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1) 

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)   

    context={'page':page,'posts':posts}    

    return render(request, 'non-working-files/library.html', context)

#  GALLERY
def gallery(request):
       
    photos= Gallery.objects.all()

    paginator = Paginator(photos, 12)
    page = request.GET.get('page')
 
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1) 

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)   

    context={'page':page,'posts':posts}   
    

    return render(request, 'non-working-files/photo_gallery.html', context)

# SHOW BOOKS
def show_book(request, slug):

    book= Library.objects.get(slug=slug)
    all_notice= Notice.objects.all().order_by('-notice_date')[0:5]

    context= {'book': book, 'all_notice': all_notice}

    return render(request, 'non-working-files/show_book.html', context)

# SHOW NOTICE
def show_notice(request, slug):

    notice= Notice.objects.get(slug=slug)
    books= Library.objects.all().order_by('-book_adding_date')[0:2]

    context= { 'notice': notice, 'books': books}

    return render(request, 'non-working-files/show_notice.html', context)