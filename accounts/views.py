from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import Subject, Student, StudentEducation, StudentAbout, Teacher, TeacherEducation, TeacherAbout, Depertment, SessionYear, Staff, Year
# from .serializerElements import SessionSerializer
from django.http import JsonResponse
from non_working_files.models import Notice, Gallery
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
from django.core import serializers
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.datastructures import MultiValueDictKeyError
from .token import generate_token
from django.core.mail import EmailMessage

# Create your views here.

# message3
# def test(request):

#     if request.method == "POST":
#         get_value= request.body
#         # Do your logic here coz you got data in `get_value`
#         data = {}
#         data['result'] = 'you made a request'
#         return HttpResponse(json.dumps(data), content_type="application/json")

#     subject= Subject.objects.all()
#     data=''
#     context= {'subject': subject, 'data': data}
#     return render(request, 'accounts/test.html', context)


# LOGIN
def user_login(request):

    if request.method== 'POST':
        
        username= request.POST.get('email')
        password= request.POST.get('password')

        user= authenticate(username=username, password=password)

        person= User.objects.get(username=username)

        if person.is_active==False:
            print('got it')
            messages.info(request, 'User is not active. Wait for your activation (untill the roll is assingned) or contuct accounts office.') 
            return HttpResponseRedirect(reverse('login'))

        else:
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('dashboard'))              
            

            else:
                
                messages.info(request, 'Sorry! user not found or password or email address is not matched.') 
                return HttpResponseRedirect(reverse('login'))

    else:
        return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# SIGNUP HSC

def signup_hsc(request):

    registered = False

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['pws']
        fathers_name = request.POST['fname']
        mothers_name = request.POST['mname']
        date_of_birth = request.POST['date']
        marital_status = request.POST['marital']
        present_address = request.POST['paddress'] 
        permanent_address = request.POST['peraddress']
        phone_number = request.POST['phone1']
        parents_number = request.POST['phone2']
        blood_group= request.POST['blood_group']
        gender= request.POST['gender']
        nid= request.POST['nid']

        print(name)
        print(email)
        

        ssc_roll= request.POST['ssc_roll']  
        ssc_reg= request.POST['ssc_reg'] 
        ssc_year= request.POST['ssc_year'] 
        ssc_grade= request.POST['ssc_grade']  
        ssc_group= request.POST['ssc_group'] 
        ssc_board= request.POST['ssc_board']         
        group_user= request.POST['group'] 
        # agree= request.POST['agree'] 

          
        if User.objects.filter(email=email).exists():

            if parents_number== phone_number:
                messages.info(request, 'Same phone number cant be used in two fields.')    
            else:
                messages.info(request, 'Email exists') 
                print('error')       
                return redirect('signup')



        else:
            user= User.objects.create_user(username=email, first_name=name, last_name= name, email=email, password=password)
            user.is_active= False
                
            user.save()            

            student= Student(user= user, name= name, group= group_user, email= email, roll='')
            student.save()

            about= StudentAbout(user= user, fathers_name= fathers_name, mothers_name= mothers_name, blood_group= blood_group, gender=gender, date_of_birth= date_of_birth, marital_status= marital_status, present_address= present_address, permanent_address= permanent_address, phone_number= phone_number, parents_number= parents_number, nid=nid)
            about.save()

            education= StudentEducation(user= user, ssc_board=ssc_board, ssc_grade= ssc_grade, ssc_group= ssc_group, ssc_reg= ssc_reg, ssc_roll=ssc_roll, ssc_year=ssc_year)
            education.save()

            group = Group.objects.get(name='student')

            user.groups.add(group)

                

            registered= True

    context= {'registered': registered}

    return render(request, 'accounts/signup.html', context)


# SIGNUP HONOURS
def signup_honours(request):

    registered = False

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['pws']
        fathers_name = request.POST['fname']
        mothers_name = request.POST['mname']
        date_of_birth = request.POST['date']
        marital_status = request.POST['marital']
        present_address = request.POST['paddress'] 
        permanent_address = request.POST['peraddress']
        phone_number = request.POST['phone1']
        parents_number = request.POST['phone2']
        blood_group= request.POST['blood_group']
        gender= request.POST['gender']
        nid= request.POST['nid']


        ssc_roll= request.POST['ssc_roll']  
        ssc_reg= request.POST['ssc_reg'] 
        ssc_year= request.POST['ssc_year'] 
        ssc_grade= request.POST['ssc_grade']  
        ssc_group= request.POST['ssc_group'] 
        ssc_board= request.POST['ssc_board'] 

        hsc_roll= request.POST['hsc_roll']  
        hsc_reg= request.POST['hsc_reg'] 
        hsc_year= request.POST['hsc_year'] 
        hsc_grade= request.POST['hsc_grade']  
        hsc_group= request.POST['hsc_group'] 
        hsc_board= request.POST['hsc_board']         
        group_user= request.POST['group'] 
        # agree= request.POST['agree'] 

          
        if User.objects.filter(email=email).exists():

            if parents_number== phone_number:
                messages.info(request, 'Same phone number cant be used in two fields.')    
            else:
                messages.info(request, 'Email exists') 
                print('error')       
                return redirect('signup')



        else:
            user= User.objects.create_user(username=email, first_name=name, last_name= name, email=email, password=password)
            user.is_active= False
                
            user.save()            

            student= Student(user= user, name= name, group= group_user, email= email, roll='')
            student.save()

            about= StudentAbout(user= user, fathers_name= fathers_name, mothers_name= mothers_name, blood_group= blood_group, gender=gender, date_of_birth= date_of_birth, marital_status= marital_status, present_address= present_address, permanent_address= permanent_address, phone_number= phone_number, parents_number= parents_number, nid=nid)
            about.save()

            education= StudentEducation(user= user, ssc_board=ssc_board, ssc_grade= ssc_grade, ssc_group= ssc_group, ssc_reg= ssc_reg, ssc_roll=ssc_roll, ssc_year=ssc_year, hsc_board=hsc_board, hsc_grade= hsc_grade, hsc_group= hsc_group, hsc_reg= hsc_reg, hsc_roll=hsc_roll, hsc_year=hsc_year)
            education.save()

            group = Group.objects.get(name='student')

            user.groups.add(group)

                

            registered= True

    context= {'registered': registered}

    return render(request, 'accounts/signup-h.html', context)

# ADMIN DASHBOARD
def admin_dashboard(request):
    user_count= User.objects.all().count()
    today_login= User.objects.filter(last_login__startswith=timezone.now().date()).count()

    today_login= round((today_login/user_count)*100)

    context= {'user_count': user_count, 'today_login': today_login}
    return render(request, 'dashboard/index.html', context)

# # ADD NOTICE
def notice(request):

    registered = False
        
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        uploaded_file= request.FILES['filename'] 
        notice = Notice(notice_title=title, notice_body=body, notice_document=uploaded_file, user=User.objects.get(username=request.user))
        notice.save()
             
        return redirect('notice')
    
    context={'registered': registered}
    return render(request, 'dashboard/add-noitce.html', context)

# # ADD PHOTO
def photo(request):

    registered = False
    
    if request.method == 'POST':
        title = request.POST['title']
        uploaded_file= request.FILES['filename'] 
        
        photo= Gallery(user= User.objects.get(username=request.user), photo_title= title, img= uploaded_file)
        photo.save()

        
        return redirect('photo')
    
    context={'registered': registered}
    return render(request, 'dashboard/add-photo.html', context)




# ADD TEACHER
def add_teacher(request):

    depertment= Depertment.objects.all()

    registered = False
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        dept_name = request.POST['dept']
        dept_head = request.POST.get('dept_head')
        joining_date= request.POST['date']
        uploaded_file= request.FILES['filename']
    

        if dept_head == 'on':
            dept_head= True

        else:
            dept_head= False

        
        if User.objects.filter(email=email).exists():

            messages.info(request, 'Email exists') 
                  
            return redirect('add-teacher')

        else:        

            user= User.objects.create_user(username=email, first_name=name, last_name= name, email=email, password='IamOK')
            user.is_active= False
                    
            user.save()      

            dept= Depertment.objects.get(dept_name= dept_name)      

            teacher= Teacher(user= user, name= name, dept_name=dept, email= email, dept_head= dept_head, joining_date=joining_date, teacher_img=uploaded_file)
            teacher.save()
            about= TeacherAbout(user= user)
            about.save()
            education= TeacherEducation(user= user)
            education.save()

            
            group = Group.objects.get(name='teacher')

            user.groups.add(group)  

            registered = True   

            # SEND EMAIL

            site = get_current_site(request)
            mail_subject = "Confirmation message from CMS"
            msg= render_to_string('accounts/activate_email.html', 
            {
                'user': user,
                'domain': site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })

            email_msg = EmailMessage(
            mail_subject,
            msg,
            settings.EMAIL_HOST_USER,
            [email]
            
            )

            email_msg.send()


           
    

    context= {'depertment':depertment, 'registered':registered }
    return render(request, 'dashboard/add-teacher.html', context)

# ADD STAFF
def add_staff(request):

    registered = False
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone1 = request.POST['p1']
        phone2 = request.POST['p2']        
        joining_date= request.POST['date']
        uploaded_file= request.FILES['filename']

        
        if User.objects.filter(email=email).exists():

            messages.info(request, 'Email exists') 
                  
            return redirect('add-staff')

        else:        

            user= User.objects.create_user(username=email, first_name=name, last_name= name, email=email, password='IamOK')
            user.is_active= False
                    
            user.save()      

            staff= Staff(user= user, name= name, email= email, joining_date=joining_date, phone_number= phone1, parents_number= phone2, staff_img=uploaded_file)
            staff.save()

            
            group = Group.objects.get(name='staff')

            user.groups.add(group)  

            registered = True     


             # SEND EMAIL

            site = get_current_site(request)
            mail_subject = "Confirmation message from CMS"
            msg= render_to_string('accounts/activate_email.html', 
            {
                'user': user,
                'domain': site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })

            email_msg = EmailMessage(
            mail_subject,
            msg,
            settings.EMAIL_HOST_USER,
            [email]
            
            )

            email_msg.send()
    
        
    

    context= {'registered':registered }
    return render(request, 'dashboard/add-staff.html', context)


# PROFILE
def profile(request, id):
    
    user= User.objects.get(id= id)

    group= Group.objects.get(user= user)

    if group.name == 'teacher':
        user_profile= Teacher.objects.get(user=user)
        about= TeacherAbout.objects.get(user=user)
        education= TeacherEducation.objects.get(user=user)

    elif group.name == 'student':
        user_profile= Student.objects.get(user=user)
        about= StudentAbout.objects.get(user=user)
        education= StudentEducation.objects.get(user=user)

    else:
        user_profile= Staff.objects.get(user= user)
        about= ''
        education=''


    context= {'user':  user, 'user_profile': user_profile, 'group': group, 'about': about, 'education': education}
    return render(request, 'dashboard/profile.html', context)   


# ADD DEPERTMENT
def depertment(request):

    registered = False
    
    if request.method == 'POST':
        dept_name = request.POST['dept']

        dept= Depertment(dept_name= dept_name)
        dept.save()

        registered= True
        
    context= {'registered': registered}
    return render(request, 'dashboard/depertment.html', context)    

# ADD YEAR
def year(request):

    registered = False

    depertment= Depertment.objects.all()
    session= SessionYear.objects.all()
    
    if request.method == 'POST':
        dept_name = request.POST['dept']
        session_name = request.POST['session']
        year_name= request.POST['year']

        dept= Depertment.objects.get(dept_name= dept_name)
        session_year= SessionYear.objects.get(session_name= session_name)

        store_year=  Year(dept= dept, session= session_year, year_name=year_name)
        store_year.save()

        registered= True
        
    context= {'registered': registered, 'depertment': depertment, 'session':session}
    return render(request, 'dashboard/year.html', context)    

# ADD SUBJECT
def subject(request):

    depertment= Depertment.objects.all()
    year= Year.objects.all()
    registered = False
    
    if request.method == 'POST':
        dept_name = request.POST['dept']
        sub_name= request.POST['name']
        sub_code= request.POST['code']
        sub_type= request.POST['type']
        year_name= request.POST['year']

        dept= Depertment.objects.get(dept_name= dept_name)
        year_name= Year.objects.get(year_name= year_name)

        sub= Subject(dept= dept, subject_code=sub_code, subject_name=sub_name, subject_type= sub_type, year= year_name)
        sub.save()

        registered= True
        
    context= {'registered': registered, 'depertment': depertment, 'year': year}
    return render(request, 'dashboard/subject.html', context)    

# ADD SESSSION
def session(request):
        
    context= {}
    return render(request, 'dashboard/session.html', context)   

# ADD SESSSION SAVE
def session_save(request):
    # if request.method == 'GET':
    getSession= request.GET.get('name')
    print(getSession)
    saveSession= SessionYear(session_name= getSession)
    try:
        saveSession.save()
        return HttpResponse('true')
    except:
        return HttpResponse('false')
        
# ADD SESSSION SHOW
def session_show(request):
    

    # session_list = list()
    all_session= SessionYear.objects.all().order_by('-id')
    
    elements = list(all_session.values())
    
    return HttpResponse(json.dumps(elements))


# USER LIST FOR CHECK EMAIL 
def user_list(request): 

    # User object is made json this way because date and time can't be serialize using json.dumps
    # elements =serializers.serialize('json', User.objects.all(), fields=('email'))
    email= request.GET.get('email', None)
    print(email)
    data = User.objects.filter(email__iexact=email).exists()
    print(data)
    
    return HttpResponse(data)

        


# SHOW TEACHER'S LIST
def teachersList(request, dept_name):

    dept= Depertment.objects.get(dept_name= dept_name)

    count=0

    if count==0:     
        teacher= Teacher.objects.filter(dept_name= dept, dept_head=True)
        count+=1
    else:
        teacher= Teacher.objects.filter(dept_name= dept)

    # teacher= Teacher.objects.filter(dept_name= dept)

    # subject= TeacherWillTake.objects.get(teacher= teacher.id)

    paginator = Paginator(teacher, 10)
    page = request.GET.get('page')
 
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1) 

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)       
   
            
    context= {'teacher': teacher, 'page':page,'posts':posts}
    count=0
    return render(request, 'dashboard/user-list.html', context)    


# # TEACHER WILL TAKE
# def wil_take(request, id):

#     user= User.objects.get(id=id)

#     # teacher= Teacher.objects.raw('select dept_name_id from accounts_teacher where user_id= %s ',id)
#     teacher= Teacher.objects.get(user=user)

#     dept= teacher.dept_name 

#     subject= Subject.objects.filter(dept= dept)

#     if request.method == 'POST':
#         subject = request.POST.getlist('subject')
#         print(subject)

#         work= TeacherWillTake(teacher= teacher)         
#         work.save()
#         work.subject.set(subject)  
#         work.save()  

        
        
#     context= {'teacher': teacher, 'subject': subject}    
#     return render(request, 'dashboard/will-take.html', context)    
    


# def activate(self, request, uidb64, token):
#     try:
#         uid= force_text(urlsafe_base64_decode(uidb64))
#         user= User.objects.get(pk=uid)
    
#     except Exception as identifier:       
#         user= None
        
#     if user is not None and generate_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         messages.info(request, 'Account is activated') 
#         return redirect('login')

#     return render(request, 'accounts/failed.html', status= 401)


# ACCOUNT ACTIVATION
def activate(request, uidb64, token):  
        try:  
            uid = force_text(urlsafe_base64_decode(uidb64))  
            user = User.objects.get(id=uid)  
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
            user = None  
        if user is not None and generate_token.check_token(user, token):  
            user.is_active = True  
            user.save()  
            messages.info(request, 'Account is activated.') 
            return redirect('login')  
        else:  
            return render(request, 'accounts/failed.html', status= 401)
    
