from django.shortcuts import render
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.views.generic import ListView
from .models import Notice, Library, Gallery
from non_working_files.models import Notice, Library, Gallery
from accounts.models import * 


# Create your views here.

# 404 handel

def handler404(request, *args, **argv):
    response = render_to_response('accounts/failed.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

# index page
def index(request):

    # USER WILL GET EMAIL WHEN ANYONE FILLSUP THE FORM
    
    successful=False

    head= Teacher.objects.filter(dept_head= True).order_by('dept_name')


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

    context= {'successful': successful, 'head': head}        


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

# TEACHER LIST OF ACCOUNTING DEPT
def accouting(request):
    head= Teacher.objects.filter(dept_head= True, dept_name= "Accounting")

    teachers= Teacher.objects.filter(subject= "Accounting").order_by('-joining_date')

    paginator = Paginator(teachers, 20)
    page = request.GET.get('page')
 
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1) 

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)   

      

    context = {'head': head, 'teachers': teachers, 'dept': "Accounting", 'page':page,'posts':posts}
    return render(request, 'non-working-files/list-teacher.html', context)

# TEACHER LIST OF BANGLA DEPT
def bangla(request):
    head= Teacher.objects.filter(dept_head= True, dept_name= "Bangla")

    teachers= Teacher.objects.filter(subject= "Bangla").order_by('-joining_date')

    paginator = Paginator(teachers, 20)
    page = request.GET.get('page')
 
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1) 

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)   

      

    context = {'head': head, 'teachers': teachers, 'dept': "Bangla", 'page':page,'posts':posts}
    return render(request, 'non-working-files/list-teacher.html', context)

# TEACHER LIST OF management DEPT
def management(request):
    head= Teacher.objects.filter(dept_head= True, dept_name= "Management")

    teachers= Teacher.objects.filter(subject= "Management").order_by('-joining_date')

    paginator = Paginator(teachers, 20)
    page = request.GET.get('page')
 
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1) 

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)   

      

    context = {'head': head, 'teachers': teachers, 'dept': "Management", 'page':page,'posts':posts}
    return render(request, 'non-working-files/list-teacher.html', context)

# TEACHER LIST OF geography DEPT
def geography(request):
    head= Teacher.objects.filter(dept_head= True, dept_name= "Geography")

    teachers= Teacher.objects.filter(subject= "Geography").order_by('-joining_date')

    paginator = Paginator(teachers, 20)
    page = request.GET.get('page')
 
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1) 

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)   

      

    context = {'head': head, 'teachers': teachers, 'dept': "Geography", 'page':page,'posts':posts}
    return render(request, 'non-working-files/list-teacher.html', context)

# TEACHER LIST OF general DEPT
def general(request):
    head= 'General'

    teachers= Teacher.objects.all().order_by('-joining_date')

    paginator = Paginator(teachers, 20)
    page = request.GET.get('page')
 
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1) 

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)   

      

    context = {'head': head, 'teachers': teachers, 'dept': "General", 'page':page,'posts':posts}
    return render(request, 'non-working-files/list-teacher.html', context)

# TEACHER LIST OF general DEPT
def staffs(request):
    

    staff= Staff.objects.all().order_by('-joining_date')

    paginator = Paginator(staff, 20)
    page = request.GET.get('page')
 
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1) 

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)   

      

    context = { 'staff': staff, 'page':page,'posts':posts}
    return render(request, 'non-working-files/list-staff.html', context)


def profile(request, id):
    
    
    # user_profile= Student.objects.get(id=id)
    # student_id= User.objects.get(id= user_profile.user_id)
    # about= StudentAbout.objects.get(user= student_id)
    # education= StudentEducation.objects.get(user= student_id)
    # recepits= StudentReceipt.objects.filter(user= user_profile)
    
    # group=""
    user= Teacher.objects.get(id= id)
    education= TeacherEducation.objects.get(user= user)


    # context= {'user':  user, 'user_profile': user_profile, 'group': group, 'about': about, 'education': education}
    context= { 'user_profile': user, 'education': education}
    return render(request, 'non-working-files/profile-teacher.html', context)   


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