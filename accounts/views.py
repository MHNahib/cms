from django.shortcuts import render, redirect, Http404, get_object_or_404
import random, string
from datetime import datetime, timedelta
from django.db.models import Sum
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
# from .models import Subject, Student, StudentEducation, StudentAbout, Teacher, TeacherEducation, TeacherAbout, Depertment, SessionYear, Staff, Year, StudentPayment, TutionFee, OthersCharge, MonthlyPayment, TotalPaidMonths
from .models import *
from non_working_files.models import *
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

def handler404(request, exception, template_name="accounts/failed.html"):

    response = render_to_response("accounts/failed.html")
    response.status_code = 404
    return response

# FLOAT CHECKER

def isFloat(number):
    try:
        return float(number)
        
    except:
        return False


# GENERATE PASSWORD

def passwordGenerator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


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
        # password = request.POST['pws']
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
        religion= request.POST['religion']
        nationality= request.POST['nationality']       
        uploaded_file= request.FILES['filename'] 

        ssc_roll= request.POST['ssc_roll']  
        ssc_reg= request.POST['ssc_reg'] 
        ssc_year= request.POST['ssc_year'] 
        ssc_grade= request.POST['ssc_grade']  
        ssc_group= request.POST['ssc_group'] 
        ssc_board= request.POST['ssc_board']    

        group_user= request.POST['group'] 
        optional_sub_science= request.POST['subjectSci'] 
        optional_sub_arts_a= request.POST['subjectA'] 
        optional_sub_arts_b= request.POST['subjectB'] 
        optional_sub_com= request.POST['subjectCom'] 
        # agree= request.POST['agree'] 

        # print(group_user)
        # print(optional_sub_science)
        # print(optional_sub_arts_a)
        # print(optional_sub_arts_b)
        # print(optional_sub_com)
        session=  SessionYear.objects.all().last()
        try:
            user= User.objects.create_user(username=email, first_name=name, last_name= name, email=email, password=passwordGenerator())
            user.is_active= False

            user.save()
            print("crossed user")
        except:
            return render(request, 'accounts/failed.html', status= 401)

        if group_user == 'Science':
            print("On science")
            student= Student(user= user, name= name, group= group_user, course='HSC', email= email, roll=None, img=uploaded_file, session=session)
            student.save()

            year= Year(user= student, year_name="1st year")
            year.save()

            payment= StudentPayment(user= student, total=6000, monthly=250)
            payment.save()

            about= StudentAbout(user= user, fathers_name= fathers_name, mothers_name= mothers_name, blood_group= blood_group, gender=gender, date_of_birth= date_of_birth, marital_status= marital_status, present_address= present_address, permanent_address= permanent_address, phone_number= phone_number, parents_number= parents_number, nid=nid, religion=religion)
            about.save()

            education= StudentEducation(user= user, ssc_board=ssc_board, ssc_grade= ssc_grade, ssc_group= ssc_group, ssc_reg= ssc_reg, ssc_roll=ssc_roll, ssc_year=ssc_year)
            education.save()

            # compulsory subjects
            subject1= Subject(user= user, subject_name= 'Bangla',firstpaper_code= '101', secondpaper_code= '102',optional= False)
            subject1.save()
            subject2= Subject(user= user, subject_name= 'English',firstpaper_code= '107', secondpaper_code= '108',optional= False)
            subject2.save()
            subject3= Subject(user= user, subject_name= 'Information and communications technology',firstpaper_code= '207', secondpaper_code= None,optional= False)
            subject3.save()

            # group subject
            subject4= Subject(user= user, subject_name= 'Physics',firstpaper_code= '174', secondpaper_code= '175',optional= False)
            subject4.save()
            subject5= Subject(user= user, subject_name= 'Chemistry',firstpaper_code= '176', secondpaper_code= '177',optional= False)
            subject5.save()

            if optional_sub_science == 'Biology':
                subject6= Subject(user= user, subject_name= 'Higher math',firstpaper_code= '265', secondpaper_code= '266',optional= False)
                subject6.save()
                subject7= Subject(user= user, subject_name= 'Biology',firstpaper_code= '178', secondpaper_code= '179',optional= True)
                subject7.save()

            else:
                subject7= Subject(user= user, subject_name= 'Higher math',firstpaper_code= '265', secondpaper_code= '266',optional= False)
                subject7.save()
                subject6= Subject(user= user, subject_name= 'Biology',firstpaper_code= '178', secondpaper_code= '179',optional= True)
                subject6.save()

            print("crossed ok")            

        elif group_user == 'Business Studies':
            
            student= Student(user= user, name= name, group= group_user, course='HSC', email= email, roll=None, img=uploaded_file, session=session )
            student.save()

            year= Year(user= student, year_name="1st year")
            year.save()

            payment= StudentPayment(user= student, total=6000, monthly=250)
            payment.save()

            about= StudentAbout(user= user, fathers_name= fathers_name, mothers_name= mothers_name, blood_group= blood_group, gender=gender, date_of_birth= date_of_birth, marital_status= marital_status, present_address= present_address, permanent_address= permanent_address, phone_number= phone_number, parents_number= parents_number, nid=nid, religion=religion)
            about.save()

            education= StudentEducation(user= user, ssc_board=ssc_board, ssc_grade= ssc_grade, ssc_group= ssc_group, ssc_reg= ssc_reg, ssc_roll=ssc_roll, ssc_year=ssc_year)
            education.save()

            # compulsory subjects
            subject1= Subject(user= user, subject_name= 'Bangla',firstpaper_code= '101', secondpaper_code= '102',optional= False)
            subject1.save()
            subject2= Subject(user= user, subject_name= 'English',firstpaper_code= '107', secondpaper_code= '108',optional= False)
            subject2.save()
            subject3= Subject(user= user, subject_name= 'Information and communications technology',firstpaper_code= '207', secondpaper_code= None,optional= False)
            subject3.save()

            # group subject
            subject4= Subject(user= user, subject_name= 'Business Organization and Management',firstpaper_code= '277', secondpaper_code= '278',optional= False)
            subject4.save()
            subject5= Subject(user= user, subject_name= 'Accounting',firstpaper_code= '253', secondpaper_code= '254',optional= False)
            subject5.save()

            if optional_sub_science == 'Finance, Banking, and Insurance':
                subject6= Subject(user= user, subject_name= 'Production Management and Marketing',firstpaper_code= '286', secondpaper_code= '287',optional= False)
                subject6.save()
                subject7= Subject(user= user, subject_name= 'Finance, Banking, and Insurance',firstpaper_code= '292', secondpaper_code= '293',optional= True)
                subject7.save()

            else:
                subject7= Subject(user= user, subject_name= 'Finance, Banking, and Insurance',firstpaper_code= '292', secondpaper_code= '293',optional= False)
                subject7.save()
                subject6= Subject(user= user, subject_name= 'Production Management and Marketing',firstpaper_code= '286', secondpaper_code= '287',optional= True)
                subject6.save()

            

        elif group_user == 'Humanities (A)':
            
            student= Student(user= user, name= name, group= group_user, course='HSC', email= email, roll=None, img=uploaded_file, session=session )
            student.save()

            year= Year(user= student, year_name="1st year")
            year.save()

            payment= StudentPayment(user= student, total=6000, monthly=250)
            payment.save()

            about= StudentAbout(user= user, fathers_name= fathers_name, mothers_name= mothers_name, blood_group= blood_group, gender=gender, date_of_birth= date_of_birth, marital_status= marital_status, present_address= present_address, permanent_address= permanent_address, phone_number= phone_number, parents_number= parents_number, nid=nid, religion=religion)
            about.save()

            education= StudentEducation(user= user, ssc_board=ssc_board, ssc_grade= ssc_grade, ssc_group= ssc_group, ssc_reg= ssc_reg, ssc_roll=ssc_roll, ssc_year=ssc_year)
            education.save()

            # compulsory subjects
            subject1= Subject(user= user, subject_name= 'Bangla',firstpaper_code= '101', secondpaper_code= '102',optional= False)
            subject1.save()
            subject2= Subject(user= user, subject_name= 'English',firstpaper_code= '107', secondpaper_code= '108',optional= False)
            subject2.save()
            subject3= Subject(user= user, subject_name= 'Information and communications technology',firstpaper_code= '207', secondpaper_code= None,optional= False)
            subject3.save()

            # group subject
            subject4= Subject(user= user, subject_name= 'Economy',firstpaper_code= '109', secondpaper_code= '110',optional= False)
            subject4.save()
            subject5= Subject(user= user, subject_name= 'Islamic History and Culture',firstpaper_code= '267', secondpaper_code= '268',optional= False)
            subject5.save()
            subject6= Subject(user= user, subject_name= 'Logic',firstpaper_code= '121', secondpaper_code= '122',optional= False)
            subject6.save()

            if optional_sub_science == 'Psychology':                
                subject7= Subject(user= user, subject_name= 'Psychology',firstpaper_code= '123', secondpaper_code= '124',optional= True)
                subject7.save()

            else:
                subject7= Subject(user= user, subject_name= 'Islamic Study',firstpaper_code= '249', secondpaper_code= '250',optional= True)
                subject7.save()

            


        elif group_user == 'Humanities (B)':
            
            student= Student(user= user, name= name, group= group_user, course='HSC', email= email, roll=None, img=uploaded_file , session=session)
            student.save()

            year= Year(user= student, year_name="1st year")
            year.save()

            payment= StudentPayment(user= student, total=6000, monthly=250)
            payment.save()

            about= StudentAbout(user= user, fathers_name= fathers_name, mothers_name= mothers_name, blood_group= blood_group, gender=gender, date_of_birth= date_of_birth, marital_status= marital_status, present_address= present_address, permanent_address= permanent_address, phone_number= phone_number, parents_number= parents_number, nid=nid, religion=religion)
            about.save()

            education= StudentEducation(user= user, ssc_board=ssc_board, ssc_grade= ssc_grade, ssc_group= ssc_group, ssc_reg= ssc_reg, ssc_roll=ssc_roll, ssc_year=ssc_year)
            education.save()

            # compulsory subjects
            subject1= Subject(user= user, subject_name= 'Bangla',firstpaper_code= '101', secondpaper_code= '102',optional= False)
            subject1.save()
            subject2= Subject(user= user, subject_name= 'English',firstpaper_code= '107', secondpaper_code= '108',optional= False)
            subject2.save()
            subject3= Subject(user= user, subject_name= 'Information and communications technology',firstpaper_code= '207', secondpaper_code= None,optional= False)
            subject3.save()

            # group subject
            subject4= Subject(user= user, subject_name= 'Civics and good governance',firstpaper_code= '269', secondpaper_code= '270',optional= False)
            subject4.save()
            subject5= Subject(user= user, subject_name= 'Social Work',firstpaper_code= '271', secondpaper_code= '272',optional= False)
            subject5.save()
            subject6= Subject(user= user, subject_name= 'Geography',firstpaper_code= '125', secondpaper_code= '126',optional= False)
            subject6.save()

            if optional_sub_science == 'Psychology':                
                subject7= Subject(user= user, subject_name= 'Psychology',firstpaper_code= '123', secondpaper_code= '124',optional= True)
                subject7.save()

            else:
                subject7= Subject(user= user, subject_name= 'Islamic Study',firstpaper_code= '249', secondpaper_code= '250',optional= True)
                subject7.save()

            

        
        user= User.objects.get(username=user)
        # education= StudentEducation.objects.get(user=user)
        # profile= Student.objects.get(user=user)
        # about= StudentAbout.objects.get(user=user)
        # subject= Subject.objects.filter(user=user)
        context={'user': user}
        # context={'user': user, 'education':education, 'profile':profile, 'subject':subject, 'about':about}

        # return render(request, 'accounts/form-hsc.html', context)
        return render(request, 'accounts/download.html', context)

        # print(name+','+fathers_name+','+mothers_name+','+email+','+marital_status+','+date_of_birth+','+present_address+','+permanent_address+',')
        # print(phone_number+','+parents_number+','+blood_group+','+gender+','+nid+','+ssc_board+','+ssc_grade+','+ssc_group+','+ssc_reg+','+ssc_roll+','+ssc_year)
        # print(group_user+','+optional_sub+','+passwordGenerator())

          
        # if User.objects.filter(email=email).exists():

        #     if parents_number== phone_number:
        #         messages.info(request, 'Same phone number cant be used in two fields.')    
        #     else:
        #         messages.info(request, 'Email exists') 
        #         print('error')       
        #         return redirect('signup')



        # else:
        #     user= User.objects.create_user(username=email, first_name=name, last_name= name, email=email, password=password)
        #     user.is_active= False
                
        #     user.save()            

        #     student= Student(user= user, name= name, group= group_user, email= email, roll='')
        #     student.save()

        #     about= StudentAbout(user= user, fathers_name= fathers_name, mothers_name= mothers_name, blood_group= blood_group, gender=gender, date_of_birth= date_of_birth, marital_status= marital_status, present_address= present_address, permanent_address= permanent_address, phone_number= phone_number, parents_number= parents_number, nid=nid)
        #     about.save()

        #     education= StudentEducation(user= user, ssc_board=ssc_board, ssc_grade= ssc_grade, ssc_group= ssc_group, ssc_reg= ssc_reg, ssc_roll=ssc_roll, ssc_year=ssc_year)
        #     education.save()

        #     group = Group.objects.get(name='student')

        #     user.groups.add(group)

                

        #     registered= True

    context= {'registered': registered}

    return render(request, 'accounts/signup.html', context)


# DOWNLOAD FORM
def download_form(request, username):
    user= User.objects.get(username=username)
    education= StudentEducation.objects.get(user=user)
    profile= Student.objects.get(user=user)
    about= StudentAbout.objects.get(user=user)
    subject= Subject.objects.filter(user=user)
    # context={'user': user, 'education':education, 'profile':profile, 'subject':subject, 'about':about}

    # all_student=Students.objects.all()
    # data={'students':all_student}
    # template=get_template("accounts/form-hsc.html")
    # data_p=template.render(context)
    # response=BytesIO()

    # pdfPage=pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")),response)
    # if not pdfPage.err:
    #     return HttpResponse(response.getvalue(),content_type="application/pdf")
    # else:
    #     return render(request, 'accounts/failed.html', status= 401)

        
    context={'user': user, 'education':education, 'profile':profile, 'subject':subject, 'about':about}

    return render(request, 'accounts/form-hsc.html', context)


# SIGNUP HONOURS
def signup_honours(request):

    registered = False   

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        # password = request.POST['pws']
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
        religion= request.POST['religion']
        nationality= request.POST['nationality']       
        uploaded_file= request.FILES['filename'] 

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
        session=  SessionYear.objects.all().last()
        group_user= request.POST['group'] 
        
        try:
            user= User.objects.create_user(username=email, first_name=name, last_name= name, email=email, password=passwordGenerator())
            user.is_active= False

            user.save()
            print("crossed user")
        except:
            return render(request, 'accounts/failed.html', status= 401)

        
            
        student= Student(user= user, name= name, group= group_user, course='Honours', email= email, roll=None, img=uploaded_file, session=session )
        student.save()

        year= Year(user= student, year_name="1st year")
        year.save()

        payment= StudentPayment(user= student, total=24000, monthly=500)
        payment.save()

        about= StudentAbout(user= user, fathers_name= fathers_name, mothers_name= mothers_name, blood_group= blood_group, gender=gender, date_of_birth= date_of_birth, marital_status= marital_status, present_address= present_address, permanent_address= permanent_address, phone_number= phone_number, parents_number= parents_number, nid=nid, religion=religion)
        about.save()

        education= StudentEducation(user= user, ssc_board=ssc_board, ssc_grade= ssc_grade, ssc_group= ssc_group, ssc_reg= ssc_reg, ssc_roll=ssc_roll, ssc_year=ssc_year, hsc_board=hsc_board, hsc_grade= hsc_grade, hsc_group= hsc_group, hsc_reg= hsc_reg, hsc_roll=hsc_roll, hsc_year=hsc_year)
        education.save()

        user= User.objects.get(username=user)
        # education= StudentEducation.objects.get(user=user)
        # profile= Student.objects.get(user=user)
        # about= StudentAbout.objects.get(user=user)
        # subject= Subject.objects.filter(user=user)
        context={'user': user}
        # context={'user': user, 'education':education, 'profile':profile, 'subject':subject, 'about':about}

        # return render(request, 'accounts/form-hsc.html', context)
        return render(request, 'accounts/download.html', context)

        
    # registered = False

    # if request.method == 'POST':
    #     name = request.POST['name']
    #     email = request.POST['email']
    #     password = request.POST['pws']
    #     fathers_name = request.POST['fname']
    #     mothers_name = request.POST['mname']
    #     date_of_birth = request.POST['date']
    #     marital_status = request.POST['marital']
    #     present_address = request.POST['paddress'] 
    #     permanent_address = request.POST['peraddress']
    #     phone_number = request.POST['phone1']
    #     parents_number = request.POST['phone2']
    #     blood_group= request.POST['blood_group']
    #     gender= request.POST['gender']
    #     nid= request.POST['nid']


    #     ssc_roll= request.POST['ssc_roll']  
    #     ssc_reg= request.POST['ssc_reg'] 
    #     ssc_year= request.POST['ssc_year'] 
    #     ssc_grade= request.POST['ssc_grade']  
    #     ssc_group= request.POST['ssc_group'] 
    #     ssc_board= request.POST['ssc_board'] 

    #     hsc_roll= request.POST['hsc_roll']  
    #     hsc_reg= request.POST['hsc_reg'] 
    #     hsc_year= request.POST['hsc_year'] 
    #     hsc_grade= request.POST['hsc_grade']  
    #     hsc_group= request.POST['hsc_group'] 
    #     hsc_board= request.POST['hsc_board']         
    #     group_user= request.POST['group'] 
    #     # agree= request.POST['agree'] 

          
    #     if User.objects.filter(email=email).exists():

    #         if parents_number== phone_number:
    #             messages.info(request, 'Same phone number cant be used in two fields.')    
    #         else:
    #             messages.info(request, 'Email exists') 
    #             print('error')       
    #             return redirect('signup')



    #     else:
    #         user= User.objects.create_user(username=email, first_name=name, last_name= name, email=email, password=password)
    #         user.is_active= False
                
    #         user.save()            

    #         student= Student(user= user, name= name, group= group_user, email= email, roll='')
    #         student.save()

    #         about= StudentAbout(user= user, fathers_name= fathers_name, mothers_name= mothers_name, blood_group= blood_group, gender=gender, date_of_birth= date_of_birth, marital_status= marital_status, present_address= present_address, permanent_address= permanent_address, phone_number= phone_number, parents_number= parents_number, nid=nid)
    #         about.save()

    #         education= StudentEducation(user= user, ssc_board=ssc_board, ssc_grade= ssc_grade, ssc_group= ssc_group, ssc_reg= ssc_reg, ssc_roll=ssc_roll, ssc_year=ssc_year, hsc_board=hsc_board, hsc_grade= hsc_grade, hsc_group= hsc_group, hsc_reg= hsc_reg, hsc_roll=hsc_roll, hsc_year=hsc_year)
    #         education.save()

    #         group = Group.objects.get(name='student')

    #         user.groups.add(group)

                

    #         registered= True

    context= {'registered': registered}

    return render(request, 'accounts/signup-h.html', context)

# SIGNUP IBM
def signup_ibm(request):

    registered = False   

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        # password = request.POST['pws']
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
        religion= request.POST['religion']
        nationality= request.POST['nationality']       
        uploaded_file= request.FILES['filename'] 

        ssc_roll= request.POST['ssc_roll']  
        ssc_reg= request.POST['ssc_reg'] 
        ssc_year= request.POST['ssc_year'] 
        ssc_grade= request.POST['ssc_grade']  
        ssc_group= request.POST['ssc_group'] 
        ssc_board= request.POST['ssc_board']    
        session=  SessionYear.objects.all().last()
        
        # agree= request.POST['agree']

        # group_user= request.POST['group'] 
        
        try:
            user= User.objects.create_user(username=email, first_name=name, last_name= name, email=email, password=passwordGenerator())
            user.is_active= False

            user.save()
            print("crossed user")
        except:
            return render(request, 'accounts/failed.html', status= 401)

        
            
        student= Student(user= user, name= name, group= 'IBM', course='IBM', email= email, roll=None, img=uploaded_file, session=session )
        student.save()

        year= Year(user= student, year_name="1st year")
        year.save()

        payment= StudentPayment(user= student, total=6000, monthly=250)
        payment.save()

        about= StudentAbout(user= user, fathers_name= fathers_name, mothers_name= mothers_name, blood_group= blood_group, gender=gender, date_of_birth= date_of_birth, marital_status= marital_status, present_address= present_address, permanent_address= permanent_address, phone_number= phone_number, parents_number= parents_number, nid=nid, religion=religion)
        about.save()

        education= StudentEducation(user= user, ssc_board=ssc_board, ssc_grade= ssc_grade, ssc_group= ssc_group, ssc_reg= ssc_reg, ssc_roll=ssc_roll, ssc_year=ssc_year)
        education.save()

        user= User.objects.get(username=user)
        # education= StudentEducation.objects.get(user=user)
        # profile= Student.objects.get(user=user)
        # about= StudentAbout.objects.get(user=user)
        # subject= Subject.objects.filter(user=user)
        context={'user': user}
        # context={'user': user, 'education':education, 'profile':profile, 'subject':subject, 'about':about}

        # return render(request, 'accounts/form-hsc.html', context)
        return render(request, 'accounts/download.html', context)

        

    context= {'registered': registered}

    return render(request, 'accounts/signup-ibm.html', context)

# SIGNUP DEGREE
def signup_degree(request):

    registered = False   

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        # password = request.POST['pws']
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
        religion= request.POST['religion']
        nationality= request.POST['nationality']       
        uploaded_file= request.FILES['filename'] 

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

        session=  SessionYear.objects.all().last()
        
        
         
        
        
        
        try:
            user= User.objects.create_user(username=email, first_name=name, last_name= name, email=email, password=passwordGenerator())
            user.is_active= False

            user.save()
            print("crossed user")
        except:
            return render(request, 'accounts/failed.html', status= 401)

        
            
        student= Student(user= user, name= name, group= group_user, course='Degree (Pass)', email= email, roll=None, img=uploaded_file , session=session)
        student.save()

        year= Year(user= student, year_name="1st year")
        year.save()

        payment= StudentPayment(user= student, total=6000, monthly=250)
        payment.save()

        about= StudentAbout(user= user, fathers_name= fathers_name, mothers_name= mothers_name, blood_group= blood_group, gender=gender, date_of_birth= date_of_birth, marital_status= marital_status, present_address= present_address, permanent_address= permanent_address, phone_number= phone_number, parents_number= parents_number, nid=nid, religion=religion)
        about.save()

        education= StudentEducation(user= user, ssc_board=ssc_board, ssc_grade= ssc_grade, ssc_group= ssc_group, ssc_reg= ssc_reg, ssc_roll=ssc_roll, ssc_year=ssc_year, hsc_board=hsc_board, hsc_grade= hsc_grade, hsc_group= hsc_group, hsc_reg= hsc_reg, hsc_roll=hsc_roll, hsc_year=hsc_year)
        education.save()

        if group_user == 'BA (PASS)':
            first_subject= request.POST['subject1'] 
            second_subject= request.POST['subject2'] 
            third_subject= request.POST['subject3'] 
            subject1= Subject(user= user, subject_name= 'History of the rise of independent Bangladesh',firstpaper_code= None, secondpaper_code= None,optional= False)
            subject1.save()
            subject2= Subject(user= user, subject_name= first_subject,firstpaper_code= None, secondpaper_code= None,optional= False)
            subject2.save()
            subject3= Subject(user= user, subject_name= second_subject,firstpaper_code= None, secondpaper_code= None,optional= False)
            subject3.save()
            subject4= Subject(user= user, subject_name= third_subject,firstpaper_code= None, secondpaper_code= None,optional= False)
            subject4.save()

        elif group_user == 'BSS (PASS)':
            fifth_subject= request.POST['subjectBSS']
            subject1= Subject(user= user, subject_name= 'History of the rise of independent Bangladesh',firstpaper_code= None, secondpaper_code= None,optional= False)
            subject1.save()
            subject2= Subject(user= user, subject_name= 'Social work',firstpaper_code= None, secondpaper_code= None,optional= False)
            subject2.save()
            subject3= Subject(user= user, subject_name= fifth_subject,firstpaper_code= None, secondpaper_code= None,optional= False)
            subject3.save()

        elif group_user == 'BBA (PASS)':
            fourth_subject= request.POST['subjectBBA'] 
            subject1= Subject(user= user, subject_name= 'History of the rise of independent Bangladesh',firstpaper_code= None, secondpaper_code= None,optional= False)
            subject1.save()
            subject2= Subject(user= user, subject_name= 'Accounting and Management',firstpaper_code= None, secondpaper_code= None,optional= False)
            subject2.save()
            subject3= Subject(user= user, subject_name= fourth_subject,firstpaper_code= None, secondpaper_code= None,optional= False)
            subject3.save()

                    


        user= User.objects.get(username=user)
        # education= StudentEducation.objects.get(user=user)
        # profile= Student.objects.get(user=user)
        # about= StudentAbout.objects.get(user=user)
        # subject= Subject.objects.filter(user=user)
        context={'user': user}
        # context={'user': user, 'education':education, 'profile':profile, 'subject':subject, 'about':about}

        # return render(request, 'accounts/form-hsc.html', context)
        return render(request, 'accounts/download.html', context)        

    context= {'registered': registered}

    return render(request, 'accounts/signup-degree.html', context)

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
        try:
            uploaded_file= request.FILES['filename'] 
            notice = Notice(notice_title=title, notice_body=body, notice_document=uploaded_file, user=User.objects.get(username=request.user))
            notice.save()
        except:
            notice = Notice(notice_title=title, notice_body=body, user=User.objects.get(username=request.user))
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

# # ADD BOOKS
def books(request):

    registered = False
    
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        written = request.POST['written']
        subject = request.POST['subject']
        img= request.FILES['filename'] 
        try:
            book= request.FILES['book'] 
            add_book= Library(

                    user=User.objects.get(username=request.user),
                    book_title= title,  
                    book_writter= written,
                    book_subject= subject,
                    book_description= body,
                    book_file= book,
                    book_img= img,
                )
            add_book.save()

        except:
            add_book= Library(
                    user=User.objects.get(username=request.user),
                    book_title= title,  
                    book_writter= written,
                    book_subject= subject,
                    book_description= body,                    
                    book_img= img,
                )
            add_book.save()

        
        return redirect('library')
    
    context={'registered': registered}
    return render(request, 'dashboard/add-books.html', context)




# ADD TEACHER
def add_teacher(request):

    # depertment= Depertment.objects.all()

    registered = False
    
    if request.method == 'POST':

        name = request.POST['name']
        email = request.POST['email']
        gender = request.POST['gender']

        # dept_name = request.POST['dept']
        # dept_head = request.POST.get('dept_head')
        joining_date= request.POST['date']
        phone1= request.POST['phone1']
        phone2= request.POST['phone2']

        ssc_ins= request.POST['ssc-i']
        ssc_grade= request.POST['ssc-g']
        hsc_ins= request.POST['hsc-i']
        hsc_grade= request.POST['hsc-g']

        hons= request.POST['hons']
        hons_i= request.POST['hons-i']
        hons_g= request.POST['hons-g']

        try:
            mast= request.POST['mast']
            mast_i= request.POST['mast-i']
            mast_g= request.POST['mast-g']
        except:
            mast= None
            mast_i= None
            mast_g= None

        try:
            phd_i= request.POST['phd-i']
            phd_g= request.POST['phd-i']
        except:
            phd_i= None
            phd_g= None

        

        dsg= request.POST['dsg']

        teacher_of= request.POST['teacher']
        try:
            head= request.POST['head']
        except:
            head= None
        
        dept_head= None
        if head:
            dept_head= True
        else:
            dept_head= False
        
        uploaded_file= request.FILES['filename']

        user= User.objects.create_user(username=email, first_name=name, last_name= name, email=email, password=passwordGenerator())
        user.is_active= True
                
        user.save() 

        teacher= Teacher(
            user= user, 
            name= name,             
            email= email,            
            joining_date=joining_date, 
            teacher_img=uploaded_file, 
            gender= gender,
            subject= teacher_of,
            designation= dsg,
            dept_head= dept_head,
            dept_name= head,
            phone_number= phone1,
            phone_number_2= phone2,
        )

        teacher.save()
        
        education= TeacherEducation(

            user= teacher,

            ssc= ssc_ins,
            ssc_grade= ssc_grade,
            hsc= hsc_ins,
            hsc_grade= hsc_grade,

            honours= hons,
            honours_from= hons_i,
            honours_grade= hons_g,

            masters= mast,
            masters_from= mast_i,  
            masters_grade= mast_g,

            phd= phd_i,
            subject= phd_g,
        )
        education.save()

        registered = True
    


    context= {'depertment':depertment, 'registered':registered }
    return render(request, 'dashboard/add-teacher.html', context)


#  EDIT TEACHER
def edit_teacher(request, id):

    # depertment= Depertment.objects.all()

    employee= Teacher.objects.get(id= id)
    education= TeacherEducation.objects.get(user= employee)

    registered = False
    
    if request.method == 'POST':

        name = request.POST['name']
       
        gender = request.POST['gender']

        # dept_name = request.POST['dept']
        # dept_head = request.POST.get('dept_head')
        joining_date= request.POST['date']
        phone1= request.POST['phone1']
        phone2= request.POST['phone2']

        ssc_ins= request.POST['ssc-i']
        ssc_grade= request.POST['ssc-g']
        hsc_ins= request.POST['hsc-i']
        hsc_grade= request.POST['hsc-g']

        hons= request.POST['hons']
        hons_i= request.POST['hons-i']
        hons_g= request.POST['hons-g']

        try:
            mast= request.POST['mast']
            mast_i= request.POST['mast-i']
            mast_g= request.POST['mast-g']
        except:
            mast= None
            mast_i= None
            mast_g= None

        try:
            phd_i= request.POST['phd-i']
            phd_g= request.POST['phd-i']
        except:
            phd_i= None
            phd_g= None

        

        dsg= request.POST['dsg']

        teacher_of= request.POST['teacher']
        try:
            head= request.POST['head']
        except:
            head= None
        
        dept_head= None
        if head:
            dept_head= True
        else:
            dept_head= False
        
        uploaded_file= None
        try:
            uploaded_file= request.FILES['filename']
        except:
            pass
        

         

        Teacher.objects.filter(id=id).update(
            
            name= name, 
            joining_date=joining_date, 
            
            gender= gender,
            subject= teacher_of,
            designation= dsg,
            dept_head= dept_head,
            dept_name= head,
            phone_number= phone1,
            phone_number_2= phone2,
        )

        if uploaded_file:
            img= Teacher.objects.get(id=id)
            img.teacher_img=uploaded_file
            img.save()
        

        
        TeacherEducation.objects.filter(user= employee).update(

            ssc= ssc_ins,
            ssc_grade= ssc_grade,
            hsc= hsc_ins,
            hsc_grade= hsc_grade,

            honours= hons,
            honours_from= hons_i,
            honours_grade= hons_g,

            masters= mast,
            masters_from= mast_i,  
            masters_grade= mast_g,

            phd= phd_i,
            subject= phd_g,
        )
        education.save()

        registered = True
    


    context= {'depertment':depertment, 'registered':registered, 'teacher': employee, 'education': education }
    return render(request, 'dashboard/edit-teacher.html', context)


# ADD principal
def add_principal(request):

    # depertment= Depertment.objects.all()

    registered = False
    
    if request.method == 'POST':

        name = request.POST['name']
        email = request.POST['email']
        gender = request.POST['gender']

        # dept_name = request.POST['dept']
        # dept_head = request.POST.get('dept_head')
        joining_date= request.POST['date']
        phone1= request.POST['phone1']
        phone2= request.POST['phone2']

        ssc_ins= request.POST['ssc-i']
        ssc_grade= request.POST['ssc-g']
        hsc_ins= request.POST['hsc-i']
        hsc_grade= request.POST['hsc-g']

        hons= request.POST['hons']
        hons_i= request.POST['hons-i']
        hons_g= request.POST['hons-g']

        try:
            mast= request.POST['mast']
            mast_i= request.POST['mast-i']
            mast_g= request.POST['mast-g']
        except:
            mast= None
            mast_i= None
            mast_g= None

        try:
            phd_i= request.POST['phd-i']
            phd_g= request.POST['phd-i']
        except:
            phd_i= None
            phd_g= None       

        
        uploaded_file= request.FILES['filename']

        user= User.objects.create_user(username=email, first_name=name, last_name= name, email=email, password='IamOK')
        user.is_active= True
                
        user.save() 

        teacher= Principal(
            user= user, 
            name= name,             
            email= email,            
            joining_date=joining_date, 
            teacher_img=uploaded_file, 
            gender= gender,            
            phone_number= phone1,
            phone_number_2= phone2,
        )

        teacher.save()
        
        education= PrincipalEducation(

            user= teacher,

            ssc= ssc_ins,
            ssc_grade= ssc_grade,
            hsc= hsc_ins,
            hsc_grade= hsc_grade,

            honours= hons,
            honours_from= hons_i,
            honours_grade= hons_g,

            masters= mast,
            masters_from= mast_i,  
            masters_grade= mast_g,

            phd= phd_i,
            subject= phd_g,
        )
        education.save()

        registered = True


    context= {'depertment':depertment, 'registered':registered }
    return render(request, 'dashboard/add-principal.html', context)


# STUDENT SEARCH FOR PAYMENT
def payment_search(request):

    registered = False
    
    if request.method == 'POST':
        
        roll = request.POST['roll']
        session_name = request.POST['session']
        class_name = request.POST['class']
        year = request.POST['year']

        try:
            element= Student.objects.filter(roll= roll, session= session_name, course= class_name, student_year= year)
            for i in element:
                store_id= i.id
                return HttpResponseRedirect(reverse('payment', args=(store_id,))) 
        except:
            registered = True 
        
        

    session= SessionYear.objects.all().order_by('-session_name')

        
    context= {'registered':registered, 'session': session, 'registered':registered, "name": "payment" }
    return render(request, 'dashboard/serach.html', context)


# STUDENT SEARCH FOR EDIT
def edit_search(request):

    registered = False
    
    if request.method == 'POST':
        
        roll = request.POST['roll']
        session_name = request.POST['session']
        class_name = request.POST['class']
        year = request.POST['year']

        try:
            element= Student.objects.filter(roll= roll, session= session_name, course= class_name, student_year= year)
            for i in element:
                store_id= i.id
                return HttpResponseRedirect(reverse('edit-profile', args=(store_id,))) 
        except:
            registered = True 
        
        

    session= SessionYear.objects.all().order_by('-session_name')

        
    context= {'registered':registered, 'session': session, 'registered':registered , "name": "edit"}
    return render(request, 'dashboard/serach.html', context)

# UPDATE YEAR
def update_year_search(request):

    registered = False
    
    if request.method == 'POST':
        
        # roll = request.POST['roll']
        session_name = request.POST['session']
        class_name = request.POST['class']
        year = request.POST['year']

        
        try:
            element= Student.objects.filter(session= session_name, course= class_name, student_year= year).order_by('roll')
            # print(element)
            context= {'course': class_name, 'session': session_name, 'year': year, 'students': element}
            return render(request, 'dashboard/show-list-of-students.html', context)
            
        except:
            registered = True 
        
        

    session= SessionYear.objects.all().order_by('-session_name')

        
    context= {'registered':registered, 'session': session, 'registered':registered , "name": "update year"}
    return render(request, 'dashboard/update-year.html', context)


# DISPLAY INCOME
def display_income(request):

    registered = False
    total = 0.0
    exp= 0.0
    if request.method == 'POST':

        start_date= request.POST['start-date']
        end_date= request.POST['end-date']

        start_date= datetime.strptime(start_date, '%Y-%m-%d')
        end_date_show= datetime.strptime(end_date, '%Y-%m-%d')
        end_date = (datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # INCOME SIDE STARTS 

        hsc= MonthlyPayment.objects.filter(user__in= Student.objects.filter(course="HSC"),date_time__range= [start_date, end_date])
        hsc_sum= MonthlyPayment.objects.filter(user__in= Student.objects.filter(course="HSC"),date_time__range= [start_date, end_date]).aggregate(Sum('amount'))
        
        if hsc_sum.get('amount__sum'):
            total= total+  hsc_sum.get('amount__sum')

        honours= MonthlyPayment.objects.filter(user__in= Student.objects.filter(course="Honours"),date_time__range= [start_date, end_date])
        honours_sum= MonthlyPayment.objects.filter(user__in= Student.objects.filter(course="Honours"),date_time__range= [start_date, end_date]).aggregate(Sum('amount'))
        
        if honours_sum.get('amount__sum'):
            total= total+  honours_sum.get('amount__sum')

        degree= MonthlyPayment.objects.filter(user__in= Student.objects.filter(course="Degree (Pass)"),date_time__range= [start_date, end_date])
        degree_sum= MonthlyPayment.objects.filter(user__in= Student.objects.filter(course="Degree (Pass)"),date_time__range= [start_date, end_date]).aggregate(Sum('amount'))
   
        if degree_sum.get('amount__sum'):
            total= total+  degree_sum.get('amount__sum')

        govt_remu = GovtRemuneration.objects.filter(date_time__range= [start_date, end_date])
        govt_remu_sum = GovtRemuneration.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if govt_remu_sum.get('amount__sum'):
            total= total+  govt_remu_sum.get('amount__sum')

        college_exam = CollegeExamFee.objects.filter(date_time__range= [start_date, end_date])
        college_exam_sum = CollegeExamFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if college_exam_sum.get('amount__sum'):
            total= total+  college_exam_sum.get('amount__sum')

        board_exam = BoardExamFee.objects.filter(date_time__range= [start_date, end_date])
        board_exam_sum = BoardExamFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if board_exam_sum.get('amount__sum'):
            total= total+  board_exam_sum.get('amount__sum')

        college_dev = CollegeDevelopmentFee.objects.filter(date_time__range= [start_date, end_date])
        college_dev_sum = CollegeDevelopmentFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if college_dev_sum.get('amount__sum'):
            total= total+  college_dev_sum.get('amount__sum')

        milad_puja = MiladPujaFee.objects.filter(date_time__range= [start_date, end_date])
        milad_puja_sum = MiladPujaFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if milad_puja_sum.get('amount__sum'):
            total= total+  milad_puja_sum.get('amount__sum')

        library = LibraryFee.objects.filter(date_time__range= [start_date, end_date])
        library_sum = LibraryFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if library_sum.get('amount__sum'):
            total= total+  library_sum.get('amount__sum')

        college_sports = CollegeSportsFee.objects.filter(date_time__range= [start_date, end_date])
        college_sports_sum = CollegeSportsFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if college_sports_sum.get('amount__sum'):
            total= total+  college_sports_sum.get('amount__sum')

        board_sports = BoardSportsFee.objects.filter(date_time__range= [start_date, end_date])
        board_sports_sum = BoardSportsFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if board_sports_sum.get('amount__sum'):
            total= total+  board_sports_sum.get('amount__sum')

        science_tech = ScienceAndTechnologyFee.objects.filter(date_time__range= [start_date, end_date])
        science_tech_sum = ScienceAndTechnologyFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if science_tech_sum.get('amount__sum'):
            total= total+  science_tech_sum.get('amount__sum')

        computer_lab = ComputerLab.objects.filter(date_time__range= [start_date, end_date])
        computer_lab_sum = ComputerLab.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if computer_lab_sum.get('amount__sum'):
            total= total+  computer_lab_sum.get('amount__sum')

        admission = AdmissionFee.objects.filter(date_time__range= [start_date, end_date])
        admission_sum = AdmissionFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if admission_sum.get('amount__sum'):
            total= total+  admission_sum.get('amount__sum')

        reg = RegistrationFee.objects.filter(date_time__range= [start_date, end_date])
        reg_sum = RegistrationFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if reg_sum.get('amount__sum'):
            total= total+  reg_sum.get('amount__sum')

        college_rov = CollegeRoversFee.objects.filter(date_time__range= [start_date, end_date])
        college_rov_sum = CollegeRoversFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if college_rov_sum.get('amount__sum'):
            total= total+  college_rov_sum.get('amount__sum')

        board_rov = BoardRoversFee.objects.filter(date_time__range= [start_date, end_date])
        board_rov_sum = BoardRoversFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if board_rov_sum.get('amount__sum'):
            total= total+  board_rov_sum.get('amount__sum')

        transfer = CollegeTranseferFee.objects.filter(date_time__range= [start_date, end_date])
        transfer_sum = CollegeTranseferFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if transfer_sum.get('amount__sum'):
            total= total+  transfer_sum.get('amount__sum')

        id_card = IdCardFee.objects.filter(date_time__range= [start_date, end_date])
        id_card_sum = IdCardFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if id_card_sum.get('amount__sum'):
            total= total+  id_card_sum.get('amount__sum')

        certificate = CertificateFee.objects.filter(date_time__range= [start_date, end_date])
        certificate_sum = CertificateFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if certificate_sum.get('amount__sum'):
            total= total+  certificate_sum.get('amount__sum')

        retention = RetentionFee.objects.filter(date_time__range= [start_date, end_date])
        retention_sum = RetentionFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if retention_sum.get('amount__sum'):
            total= total+  retention_sum.get('amount__sum')

        tc = TestimonialFee.objects.filter(date_time__range= [start_date, end_date])
        tc_sum = TestimonialFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if tc_sum.get('amount__sum'):
            total= total+  tc_sum.get('amount__sum')

        paper = PaperMagazineFee.objects.filter(date_time__range= [start_date, end_date])
        paper_sum = PaperMagazineFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if paper_sum.get('amount__sum'):
            total= total+  paper_sum.get('amount__sum')

        practical = PracticalFee.objects.filter(date_time__range= [start_date, end_date])
        practical_sum = PracticalFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if practical_sum.get('amount__sum'):
            total= total+  practical_sum.get('amount__sum')

        bill = WaterFee.objects.filter(date_time__range= [start_date, end_date])
        bill_sum = WaterFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if bill_sum.get('amount__sum'):
            total= total+  bill_sum.get('amount__sum')

        management = ManagementFee.objects.filter(date_time__range= [start_date, end_date])
        management_sum = ManagementFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if management_sum.get('amount__sum'):
            total= total+  management_sum.get('amount__sum')

        fourth = FourthPaperFee.objects.filter(date_time__range= [start_date, end_date])
        fourth_sum = FourthPaperFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if fourth_sum.get('amount__sum'):
            total= total+  fourth_sum.get('amount__sum')

        late_fee = LateFee.objects.filter(date_time__range= [start_date, end_date])
        late_fee_sum = LateFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if late_fee_sum.get('amount__sum'):
            total= total+  late_fee_sum.get('amount__sum')

        center_fee = CenterFee.objects.filter(date_time__range= [start_date, end_date])
        center_fee_sum = CenterFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if center_fee_sum.get('amount__sum'):
            total= total+  center_fee_sum.get('amount__sum')

        poor = PoorFundFee.objects.filter(date_time__range= [start_date, end_date])
        poor_sum = PoorFundFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if poor_sum.get('amount__sum'):
            total= total+  poor_sum.get('amount__sum')

        bank = BankInterestFee.objects.filter(date_time__range= [start_date, end_date])
        bank_sum = BankInterestFee.objects.filter(date_time__range= [start_date, end_date]).aggregate(Sum('amount'))

        if bank_sum.get('amount__sum'):
            total= total+  bank_sum.get('amount__sum')

        d = donation.objects.filter(date__range=[start_date, end_date])
        d_sum = donation.objects.filter(date__range=[start_date, end_date]).aggregate(Sum('amount'))
        
        if d_sum.get('amount__sum'):
            total= total+  d_sum.get('amount__sum')

        # INCOME SIDE ENDS

        # EXPENCE STATS
            
        print(exp)

        salery = GovtSalaryExp.objects.filter(date__range= [start_date, end_date])
        salery_sum = GovtSalaryExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if salery_sum.get('amount__sum'):
            print(exp)
            exp= exp+  salery_sum.get('amount__sum')
            

        house = HouseRentAndBonusExp.objects.filter(date__range= [start_date, end_date])
        house_sum = HouseRentAndBonusExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if house_sum.get('amount__sum'):
            exp= exp+  house_sum.get('amount__sum')
          

        board_exp = BoardRegExp.objects.filter(date__range= [start_date, end_date])
        board_exp_sum = BoardRegExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if board_exp_sum.get('amount__sum'):
            exp= exp+  board_exp_sum.get('amount__sum')
    
        
        college_exam_exp = CollegeExamExp.objects.filter(date__range= [start_date, end_date])
        college_exam_sum = CollegeExamExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if college_exam_sum.get('amount__sum'):
            exp= exp+  college_exam_sum.get('amount__sum')
    
      
        college_dev_exp = CollegeDevExp.objects.filter(date__range= [start_date, end_date])
        college_dev_sum = CollegeDevExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if college_dev_sum.get('amount__sum'):
            exp= exp+  college_dev_sum.get('amount__sum')
    
       
        milad_puja_exp = MiladPujaExp.objects.filter(date__range= [start_date, end_date])
        milad_puja_exp_sum = MiladPujaExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if milad_puja_exp_sum.get('amount__sum'):
            exp= exp+  milad_puja_exp_sum.get('amount__sum')
    
        
        library_exp = LibraryExp.objects.filter(date__range= [start_date, end_date])
        library_exp_sum = LibraryExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if library_exp_sum.get('amount__sum'):
            exp= exp+  library_exp_sum.get('amount__sum')
    
        
        sports_exp = SportsExp.objects.filter(date__range= [start_date, end_date])
        sports_exp_sum = SportsExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if sports_exp_sum.get('amount__sum'):
            exp= exp+  sports_exp_sum.get('amount__sum')
    
        
        poor_exp = PoorFundExp.objects.filter(date__range= [start_date, end_date])
        poor_exp_sum = PoorFundExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if poor_exp_sum.get('amount__sum'):
            exp= exp+  poor_exp_sum.get('amount__sum')
    
        
        water_exp = WaterExp.objects.filter(date__range= [start_date, end_date])
        water_exp_sum = WaterExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if water_exp_sum.get('amount__sum'):
            exp= exp+  water_exp_sum.get('amount__sum')
    
        
        electric_exp = ElectricExp.objects.filter(date__range= [start_date, end_date])
        electric_exp_sum = ElectricExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if electric_exp_sum.get('amount__sum'):
            exp= exp+  electric_exp_sum.get('amount__sum')
    
        
        bank_exp = BankChargeExp.objects.filter(date__range= [start_date, end_date])
        bank_exp_sum = BankChargeExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if bank_exp_sum.get('amount__sum'):
            exp= exp+  bank_exp_sum.get('amount__sum')
    
        tel_exp = TelephoneBillExp.objects.filter(date__range= [start_date, end_date])
        tel_exp_sum = TelephoneBillExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if tel_exp_sum.get('amount__sum'):
            exp= exp+  tel_exp_sum.get('amount__sum')
    
       
        sct_exp = ScienceAndTechnologyExp.objects.filter(date__range= [start_date, end_date])
        sct_exp_sum = ScienceAndTechnologyExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if sct_exp_sum.get('amount__sum'):
            exp= exp+  sct_exp_sum.get('amount__sum')
    
        
        cl_exp = ComputerLabExp.objects.filter(date__range= [start_date, end_date])
        cl_exp_sum = ComputerLabExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if cl_exp_sum.get('amount__sum'):
            exp= exp+  cl_exp_sum.get('amount__sum')
    
        entertainment_exp = EntertainmentExp.objects.filter(date__range= [start_date, end_date])
        entertainment_exp_sum = EntertainmentExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if entertainment_exp_sum.get('amount__sum'):
            exp= exp+  entertainment_exp_sum.get('amount__sum')
    
        
        conveyance_exp = ConveyanceExp.objects.filter(date__range= [start_date, end_date])
        conveyance_exp_sum = ConveyanceExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if conveyance_exp_sum.get('amount__sum'):
            exp= exp+  conveyance_exp_sum.get('amount__sum')
    
      
        printing_exp = PrintingAndStationaryExp.objects.filter(date__range= [start_date, end_date])
        printing_exp_sum = PrintingAndStationaryExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if printing_exp_sum.get('amount__sum'):
            exp= exp+  printing_exp_sum.get('amount__sum')
    
    
        management_exp = ManagementExp.objects.filter(date__range= [start_date, end_date])
        management_exp_sum = ManagementExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if management_exp_sum.get('amount__sum'):
            exp= exp+  management_exp_sum.get('amount__sum')
    
        
        pardon_exp = PardonExp.objects.filter(date__range= [start_date, end_date])
        pardon_exp_sum = PardonExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if pardon_exp_sum.get('amount__sum'):
            exp= exp+  pardon_exp_sum.get('amount__sum')
    
        
        others_exp = OtherExp.objects.filter(date__range= [start_date, end_date])
        others_exp_sum = OtherExp.objects.filter(date__range= [start_date, end_date]).aggregate(Sum('amount'))

        if others_exp_sum.get('amount__sum'):
            exp= exp+  others_exp_sum.get('amount__sum')
    
        
        # EXPENCE ENDS

        context= {
            'start_date': start_date, 
            'end_date': end_date_show, 
            'name': 'Income and expences',
            
            # INCOME 
            'govt_remu': govt_remu,
            'govt_remu_sum': govt_remu_sum,

            'hsc': hsc,
            'hsc_sum': hsc_sum,

            'honours': honours,
            'honours_sum': honours_sum,

            'degree': degree,
            'degree_sum': degree_sum,

            'college_exam': college_exam,
            'college_exam_sum': college_exam_sum,

            'board_exam': board_exam,
            'board_exam_sum': board_exam_sum,

            'college_dev':college_dev,
            'college_dev_sum': college_dev_sum,

            'milad_puja':milad_puja,
            'milad_puja_sum':milad_puja_sum,

            'library': library,
            'library_sum': library_sum,

            'college_sports': college_sports,
            'college_sports_sum': college_sports_sum,

            'board_sports': board_sports,
            'board_sports_sum': board_sports_sum,

            'science_tech': science_tech,
            'science_tech_sum': science_tech_sum,

            'computer_lab': computer_lab,
            'computer_lab_sum': computer_lab_sum,

            'admission': admission,
            'admission_sum': admission_sum,

            'reg': reg,
            'reg_sum': reg_sum,

            'college_rov': college_rov,
            'college_rov_sum': college_rov_sum,

            'board_rov': board_rov,
            'board_rov_sum': board_rov_sum,

            'transfer': transfer,
            'transfer_sum': transfer_sum,

            'id_card': id_card,
            'id_card_sum': id_card_sum,

            'certificate': certificate,
            'certificate_sum': certificate_sum,

            'retention': retention,
            'retention_sum': retention_sum,

            'tc': tc,
            'tc_sum': tc_sum,

            'paper': paper,
            'paper_sum': paper_sum,

            'practical': practical,
            'practical_sum': practical_sum,

            'bill': bill,
            'bill_sum': bill_sum,

            'management': management,
            'management_sum': management_sum,

            'fourth': fourth,
            'fourth_sum': fourth_sum,

            'late_fee': late_fee,
            'late_fee_sum': late_fee_sum,

            'center_fee': center_fee,
            'center_fee_sum': center_fee_sum,

            'poor': poor,
            "poor_sum": poor_sum,

            'bank': bank,
            'bank_sum': bank_sum,

            'd': d,
            'd_sum': d_sum,

            # EXPENCES
            'salery': salery,
            'salery_sum': salery_sum,

            'house': house,
            'house_sum': house_sum,

            'board_exp': board_exp,
            'board_exp_sum': board_exp_sum,

            'college_exam_exp': college_exam_exp,
            'college_exam_sum': college_exam_sum,

            'college_dev_exp': college_dev_exp,
            'college_dev_sum': college_dev_sum,

            'milad_puja_exp': milad_puja_exp,
            'milad_puja_exp_sum': milad_puja_exp_sum,

            'library_exp': library_exp,
            'library_exp_sum': library_exp_sum,

            'sports_exp': sports_exp,
            'sports_exp_sum': sports_exp_sum,

            'poor_exp': poor_exp,
            'poor_exp_sum': poor_exp_sum,

            'water_exp': water_exp,
            'water_exp_sum': water_exp_sum,

            'electric_exp': electric_exp,
            'electric_exp_sum': electric_exp_sum,

            'bank_exp': bank_exp,
            'bank_exp_sum': bank_exp_sum,

            'tel_exp': tel_exp,
            'tel_exp_sum': tel_exp_sum,

            'sct_exp': sct_exp,
            'sct_exp_sum': sct_exp_sum,

            'cl_exp': cl_exp,
            'cl_exp_sum': cl_exp_sum,

            'entertainment_exp': entertainment_exp,
            'entertainment_exp_sum': entertainment_exp_sum,

            'conveyance_exp': conveyance_exp,
            'conveyance_exp_sum': conveyance_exp_sum,

            'printing_exp': printing_exp,
            'printing_exp_sum': printing_exp_sum,

            'management_exp': management_exp,
            'management_exp_sum': management_exp_sum,

            'pardon_exp': pardon_exp,
            'pardon_exp_sum': pardon_exp_sum,

            'others_exp': others_exp,
            'others_exp_sum': others_exp_sum,

            'income': total,
            'exp': exp

            }
        return render(request, 'dashboard/income_summary.html', context)
        # for i in data:
        #     print(data.user.roll)

        
        # print(start_date)
        # print(end_date)
        
    #     roll = request.POST['roll']
    #     session_name = request.POST['session']
    #     class_name = request.POST['class']
    #     year = request.POST['year']

    #     try:
    #         element= Student.objects.filter(roll= roll, session= session_name, course= class_name, student_year= year)
    #         for i in element:
    #             store_id= i.id
    #             return HttpResponseRedirect(reverse('edit-profile', args=(store_id,))) 
    #     except:
    #         registered = True 
        
        

    # session= SessionYear.objects.all().order_by('-session_name')

        
    context= {'registered':registered, 'session': session, 'registered':registered , "name": "edit"}
    return render(request, 'dashboard/monthly_income_expences.html', context)

# ADD STAFF
def add_staff(request):

    registered = False
    
    if request.method == 'POST':
        try:
            name = request.POST['name']
        except:
            name= None
        try:
            email = request.POST['email']
        except:
            email= None
        try:
            phone1 = request.POST['p1']
        except:
            phone1 = None
        try:
            phone2 = request.POST['p2'] 
        except:
            phone2= None
        try:
            designation = request.POST['class'] 
        except:
            designation = None     
        try:
            post = request.POST['post']  
        except:
            post= None       
        try:
            gender = request.POST['gender'] 
        except:
            gender= None       
        try:
            joining_date= request.POST['date']
        except:
            joining_date= None
            
        uploaded_file= request.FILES['filename']

        if designation == '3rd':
            if email:
                user= User.objects.create_user(username=email, first_name=name, last_name= name, email=email, password=passwordGenerator())
                user.is_active= True
                user.save()  
                staff= Staff(
                    user= user, 
                    name= name, 
                    email= email, 
                    joining_date=joining_date, 
                    phone_number= phone1, 
                    phone_number_2= phone2, 
                    gender= gender,
                    designation= designation,
                    post= post,
                    staff_img=uploaded_file
                    )

                staff.save()
            else:
                return render(request, 'accounts/failed.html', status= 404)

        else:
            user= User.objects.create_user(username=name, first_name=name, last_name= name)
            staff= Staff(
                user= user, 
                name= name, 
                email= email, 
                joining_date=joining_date, 
                phone_number= phone1, 
                phone_number_2= phone2, 
                gender= gender,
                designation= designation,
                post= post,
                staff_img=uploaded_file
                )

            staff.save()
        
        registered = True 

        
    context= {'registered':registered }
    return render(request, 'dashboard/add-staff.html', context)
    
# EDIT STAFF
def edit_staff(request, id):

    registered = False
    user_details= User.objects.get(id=id)
    employee = Staff.objects.get(user= user_details)
    
    if request.method == 'POST':
       
        name = request.POST['name']
        phone1 = request.POST['p1']
        phone2 = request.POST['p2'] 
        designation = request.POST['class'] 
        post_name = request.POST['post']  
        gender = request.POST['gender'] 
        joining_date= request.POST['date']

        # print(post)
        
        uploaded_file= None
        try:
            uploaded_file= request.FILES['filename']
        except:
            pass

        
        Staff.objects.filter(user= user_details).update(
            
            name= name,             
            joining_date=joining_date, 
            phone_number= phone1, 
            phone_number_2= phone2, 
            gender= gender,
            designation= designation,
            post= post_name
        )

        if uploaded_file:
            staff= Staff.objects.get(user= user_details)

            staff.staff_img=uploaded_file
            staff.save()
            
            

        
        registered = True 

        employee = Staff.objects.get(user= user_details)

        
    context= {'registered':registered, "staff": employee }
    return render(request, 'dashboard/edit-staff.html', context)


# PROFILE
def profile(request, id):
    
    
    user_profile= Student.objects.get(id=id)
    student_id= User.objects.get(id= user_profile.user_id)
    about= StudentAbout.objects.get(user= student_id)
    education= StudentEducation.objects.get(user= student_id)
    recepits= StudentReceipt.objects.filter(user= user_profile)
    
    group=""


    # context= {'user':  user, 'user_profile': user_profile, 'group': group, 'about': about, 'education': education}
    context= { 'user_profile': user_profile, 'group': group, 'about': about, 'education': education, 'recepits':recepits}
    return render(request, 'dashboard/profile-student.html', context)   


# PROFILE EDIT 
def profile_edit(request, id):
    
    
    user_profile= Student.objects.get(id=id)
    student_id= User.objects.get(id= user_profile.user_id)
    about= StudentAbout.objects.get(user= student_id)
    education= StudentEducation.objects.get(user= student_id)
    # recepits= StudentReceipt.objects.filter(user= user_profile)

    registered = False
    
    if request.method == 'POST':        

        name = request.POST['name']
        uploaded_file= None
        hsc_roll= None
        hsc_reg= None
        hsc_year= None
        hsc_grade= None 
        hsc_group= None
        hsc_board=  None

        # password = request.POST['pws']
        roll = request.POST['roll']
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
        religion= request.POST['religion']
        print(fathers_name)
        try:    
            uploaded_file= request.FILES['filename']
        except:
            pass 

        ssc_roll= request.POST['ssc_roll']  
        ssc_reg= request.POST['ssc_reg'] 
        ssc_year= request.POST['ssc_year'] 
        ssc_grade= request.POST['ssc_grade']  
        ssc_group= request.POST['ssc_group'] 
        ssc_board= request.POST['ssc_board']    
        try:
            hsc_roll= request.POST['hsc_roll']  
            hsc_reg= request.POST['hsc_reg'] 
            hsc_year= request.POST['hsc_year'] 
            hsc_grade= request.POST['hsc_grade']  
            hsc_group= request.POST['hsc_group'] 
            hsc_board= request.POST['hsc_board'] 
        except:
            hsc_roll= None
            hsc_reg= None
            hsc_year= None
            hsc_grade= None 
            hsc_group= None
            hsc_board=  None

        
        Student.objects.filter(id=id).update(
            roll= roll,
            name= name        
        )

        if uploaded_file:
            Student.objects.filter(id=id).update(
            img= uploaded_file       
            )

        StudentAbout.objects.filter(user= student_id).update(
            
            fathers_name= fathers_name,
            mothers_name= mothers_name,
            blood_group= blood_group,
            gender= gender,
            nid= nid,
            date_of_birth= date_of_birth,
            marital_status= marital_status,
            present_address= present_address,
            permanent_address= permanent_address,
            phone_number= phone_number,
            parents_number= parents_number,
            religion= religion
        )

        StudentEducation.objects.filter(user= student_id).update(
            ssc_roll= ssc_roll,
            ssc_reg= ssc_reg,
            ssc_year= ssc_year,
            ssc_grade= ssc_grade,
            ssc_group= ssc_group, 
            ssc_board= ssc_board,   

            hsc_roll= hsc_roll,
            hsc_reg= hsc_reg,
            hsc_year= hsc_year,
            hsc_grade= hsc_grade,
            hsc_group= hsc_group,
            hsc_board= hsc_board
        )

        registered = True
        user_profile= Student.objects.get(id=id)
        student_id= User.objects.get(id= user_profile.user_id)
        about= StudentAbout.objects.get(user= student_id)
        education= StudentEducation.objects.get(user= student_id)
        context= { 'user_profile': user_profile, 'about': about, 'education': education, "registered": registered}


    # context= {'user':  user, 'user_profile': user_profile, 'group': group, 'about': about, 'education': education}
    context= { 'user_profile': user_profile, 'about': about, 'education': education, "registered": registered}
    return render(request, 'dashboard/edit-student.html', context)   


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

# # ADD DEPERTMENT
# def list_students(request):

#     registered = False
    
#     if request.method == 'POST':
#         dept_name = request.POST['dept']

#         dept= Depertment(dept_name= dept_name)
#         dept.save()

#         registered= True
        
#     context= {'registered': registered}
#     return render(request, 'dashboard/depertment.html', context)    

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

# ADD ROLL OF SCIENCE (HSC) STUDENTS
def roll_hsc_science(request):
    user= Student.objects.filter(course= "HSC", group='Science', roll= None)
    context={'user': user, 'course': "HSC", 'group':'Science'}
    return render(request, 'dashboard/add-roll.html', context)


# ADD ROLL OF COMARTS (HSC) STUDENTS
def roll_hsc_commarts(request):
    user= Student.objects.filter(course= "HSC", group='Business Studies', roll= None)
    context={'user': user, 'course': "HSC", 'group':'Business Studies'}
    return render(request, 'dashboard/add-roll.html', context)


# ADD ROLL OF ARTS A (HSC) STUDENTS
def roll_hsc_arts_a(request):
    user= Student.objects.filter(course= "HSC", group='Humanities (A)', roll= None)
    context={'user': user, 'course': "HSC", 'group':'Humanities (A)'}
    return render(request, 'dashboard/add-roll.html', context)


# ADD ROLL OF ARTS B (HSC) STUDENTS
def roll_hsc_arts_b(request):
    user= Student.objects.filter(course= "HSC", group='Humanities (B)', roll= None)
    context={'user': user, 'course': "HSC", 'group':'Humanities (B)'}
    return render(request, 'dashboard/add-roll.html', context)


# ADD ROLL OF HONOURS (Department of Accounting) STUDENTS
def roll_honours_accounting(request):
    user= Student.objects.filter(course= 'Honours', group='Department of Accounting', roll= None)
    context={'user': user, 'course': 'Honours', 'group':'Department of Accounting'}
    return render(request, 'dashboard/add-roll.html', context)


# ADD ROLL OF HONOURS (Department of Bengali) STUDENTS
def roll_honours_bangla(request):
    user= Student.objects.filter(course= 'Honours', group='Department of Bengali', roll= None)
    context={'user': user, 'course': 'Honours', 'group':'Department of Bengali'}
    return render(request, 'dashboard/add-roll.html', context)


# ADD ROLL OF HONOURS (Department of Geography) STUDENTS
def roll_honours_geography(request):
    user= Student.objects.filter(course= 'Honours', group='Department of Geography', roll= None)
    context={'user': user, 'course': 'Honours', 'group':'Department of Geography'}
    return render(request, 'dashboard/add-roll.html', context)


# ADD ROLL OF HONOURS (Department of Management) STUDENTS
def roll_honours_management(request):
    user= Student.objects.filter(course= 'Honours', group='Department of Management', roll= None)
    context={'user': user, 'course': 'Honours', 'group':'Department of Management'}
    return render(request, 'dashboard/add-roll.html', context)


# ADD ROLL OF DEGREE (BBA) STUDENTS
def roll_degree_bba(request):
    user= Student.objects.filter(course= 'Degree (Pass)', group='BBA (PASS)', roll= None)
    context={'user': user, 'course': 'Degree (Pass)', 'group':'BBA (PASS)'}
    return render(request, 'dashboard/add-roll.html', context)

# ADD ROLL OF DEGREE (BA) STUDENTS
def roll_degree_ba(request):
    user= Student.objects.filter(course= 'Degree (Pass)', group='BA (PASS)', roll= None)
    context={'user': user, 'course': 'Degree (Pass)', 'group':'BA (PASS)'}
    return render(request, 'dashboard/add-roll.html', context)

# ADD ROLL OF DEGREE (BSS) STUDENTS
def roll_degree_bss(request):
    user= Student.objects.filter(course= 'Degree (Pass)', group='BSS (PASS)', roll= None)
    context={'user': user, 'course': 'Degree (Pass)', 'group':'BSS (PASS)'}
    return render(request, 'dashboard/add-roll.html', context)

# ADD ROLL OF IBM STUDENTS
def roll_ibm(request):
    user= Student.objects.filter(course= 'IBM', roll= None)
    context={'user': user, 'course': 'IBM', 'group':''}
    return render(request, 'dashboard/add-roll.html', context)


    
# ADD ROLL
def add_roll(request):
    if request.method == 'POST':
        roll = request.POST['roll']
        user_id = request.POST['id']
        # print(roll)
        # print(user_id)
        user= User.objects.get(id=user_id)
        if roll == 'None':
            return HttpResponse('false')
        # print(user)
        try:
            saveRoll= Student.objects.filter(user= user).update(roll= roll)
            print(saveRoll)
            return HttpResponse('true')
        except:
            return HttpResponse('false')

        
    
# ADD ROLL
def update_year(request):
    if request.method == 'POST':
        # roll = request.POST['roll']
        list_of_students = request.POST.getlist('students[]')
        year= request.POST['year']
        # print(year)
                   

        try:
            for i in list_of_students:
                Student.objects.filter(id=i).update(student_year= year) 
            
            return HttpResponse('true')
        except:
            return HttpResponse('false')

        
        # user= User.objects.get(id=user_id)
        # if roll == 'None':
        #     return HttpResponse('false')
        # # print(user)
        # try:
        #     saveRoll= Student.objects.filter(user= user).update(roll= roll)
        #     print(saveRoll)
        #     return HttpResponse('true')
        # except:
        #     return HttpResponse('false')

        


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
def teachersList(request):

    # dept= Depertment.objects.get(dept_name= dept_name)

    # count=0

    # if count==0:     
    #     teacher= Teacher.objects.filter(dept_name= dept, dept_head=True)
    #     count+=1
    # else:
    #     teacher= Teacher.objects.filter(dept_name= dept)

    teacher= Teacher.objects.all().order_by('joining_date')
    # teacher= Teacher.objects.filter(dept_name= dept)

    # subject= TeacherWillTake.objects.get(teacher= teacher.id)

    paginator = Paginator(teacher, 20)
    page = request.GET.get('page')
 
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1) 

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)       
   
            
    context= {'teacher': teacher, 'page':page,'posts':posts}
    
    return render(request, 'dashboard/teachers-list.html', context)    


# SHOW TEACHER'S LIST
def staffsList(request):

    # dept= Depertment.objects.get(dept_name= dept_name)

    # count=0

    # if count==0:     
    #     teacher= Teacher.objects.filter(dept_name= dept, dept_head=True)
    #     count+=1
    # else:
    #     teacher= Teacher.objects.filter(dept_name= dept)

    staffs= Staff.objects.all().order_by('joining_date')
    # teacher= Teacher.objects.filter(dept_name= dept)

    # subject= TeacherWillTake.objects.get(teacher= teacher.id)

    paginator = Paginator(staffs, 20)
    page = request.GET.get('page')
 
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1) 

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)       
   
            
    context= {'staffs': staffs, 'page':page,'posts':posts}
    
    return render(request, 'dashboard/staffs-list.html', context)    


# PAYMENT
def payment(request, id):

    student= Student.objects.get(id= id)
    user= User.objects.get(id= student.user.id)
    pay= StudentPayment.objects.get(user= student)
    tution= TutionFee.objects.get(class_name= student.course)
    others= OthersCharge.objects.all().first()

    monthly_fee=0
    admission_fee= 0
    mp= 0
    cd= 0
    library_fee=0
    poor_fund=0
    st_fee=0
    cl_fee=0
    id_fee=0
    reg=0
    rov_college=0
    rov_board=0
    exam_fee=0
    board_exam_fee=0
    clg_sports_fee= 0
    board_sports_fee= 0   
    transfer_fee= 0   
    certificate_fee= 0   
    ret_fee= 0   
    test_fee= 0   
    paper_fee= 0   
    practical_fee= 0   
    water= 0   
    management_fee= 0   
    fourth_fee=0   
    late_fee= 0   
    center_fee= 0      
    
    if request.method == 'POST':
        

        fee= request.POST.get('payfee', "")
        admission= request.POST.get('payadmission', "")
        exam= request.POST.get('payexam', "")
        others= request.POST.get('payothers', "")

        total= float(request.POST['total-fee'])
        print('total: ' ,total)

        # FIND SESSION
        session= TotalIncome.objects.last()

        # FEE HERE 
        if fee == "True" :
            # print("ok on fee")
            # FLOAT CHECK
            # sum_of_income=0.0

            monthly_fee = isFloat(request.POST.get('monthly-tuition-fee'))
            if type(monthly_fee )!= bool:
                # DB CONNECTION
                monthly_list = request.POST.get('monthly-list')
                monthly_list= monthly_list.split(",")
                monthly_payment_fee= MonthlyPayment(user=Student.objects.get(id=id) , amount= monthly_fee , student_year= Student.objects.get(id=id).student_year, month= json.dumps(monthly_list))
                monthly_payment_fee.save()

                # sum_of_income= sum_of_income+ monthly_fee

                # ADD IT TO TOTAL INCOME
                if student.course== 'HSC':
                    income= TotalIncome.objects.get(id= session.id)
                    pay= income.hsc_tutionfee + monthly_fee
                    
                    income= TotalIncome.objects.filter(id= session.id).update(hsc_tutionfee= pay)
                
                elif student.course== 'Honours':
                    income= TotalIncome.objects.get(id= session.id)
                    pay= income.honours_tutionfee + monthly_fee
                    # total_amount= TotalEarning.objects.get(session= session.session)
                    # total_amount= TotalEarning.objects.filter(session= session.session).update(amount=total_amount.amount+ pay)
                    income= TotalIncome.objects.filter(id= session.id).update(honours_tutionfee= pay)

                elif student.course== 'IBM':
                    income= TotalIncome.objects.get(id= session.id)
                    pay= income.hsc_tutionfee + monthly_fee
                    # total_amount= TotalEarning.objects.get(session= session.session)
                    # total_amount= TotalEarning.objects.filter(session= session.session).update(amount=total_amount.amount+ pay)
                    income= TotalIncome.objects.filter(id= session.id).update(hsc_tutionfee= pay)

                elif student.course== 'Degree (Pass)':
                    income= TotalIncome.objects.get(id= session.id)
                    pay= income.degree_tutionfee + monthly_fee
                    # total_amount= TotalEarning.objects.get(session= session.session)
                    # total_amount= TotalEarning.objects.filter(session= session.session).update(amount=total_amount.amount+ pay)
                    income= TotalIncome.objects.filter(id= session.id).update(degree_tutionfee= pay)

                

                
                
                
            else:
                # return render(request, 'accounts/failed.html', status= 401)
                monthly_fee=0

           
            # print(monthly_list)
            # for i in monthly_list:
            #     print(i)
            
            # for month_name in monthly_list:
            #     payment_months= TotalPaidMonths(monthly_payment= MonthlyPayment.objects.filter(user= Student.objects.get(id=id)), month= month_name)
            #     payment_months.save()
            # try:
            #     payment_months= TotalPaidMonths(monthly_payment= monthly_payment_fee, month= json.dumps(monthly_list))
            #     payment_months.save()
            # except :
            #     return render(request, 'accounts/failed.html', status= 401)
            

            

            # for i in monthly_list:
            #     print(i)
            #     print()

        # ADMISSION PAYMENT HERE 
        if admission == "True" :

            mp =  isFloat(request.POST.get('mp-fee'))

            if type(mp )!= bool:
                payment= MiladPujaFee(user=Student.objects.get(id=id) , amount= mp)
                payment.save()
                
                # income= TotalIncome.objects.get(id= session.id)
                # income= income.milad_puja + mp
                # total_amount= TotalEarning.objects.filter(session= session.session).update(amount= income)
                # income= TotalIncome.objects.filter(id= session.id).update(milad_puja= income)
            else:
                mp=0

            cd =  isFloat(request.POST.get('cd-fee'))

            if type(cd )!= bool:
                payment= CollegeDevelopmentFee(user=Student.objects.get(id=id) , amount= cd)
                payment.save()
                
                # income= TotalIncome.objects.get(id= session.id)
                # income= income.milad_puja + mp
                # total_amount= TotalEarning.objects.filter(session= session.session).update(amount= income)
                # income= TotalIncome.objects.filter(id= session.id).update(milad_puja= income)
            else:
                cd=0

            admission_fee =  isFloat(request.POST.get('admissin-fee'))
            
            # try:
            #     print("admission", admission_fee)
            # except expression as identifier:
            #     print("admission"+ admission_fee)

            if type(admission_fee )!= bool:
                print(admission_fee)
                payment= AdmissionFee(user=Student.objects.get(id=id) , amount= admission_fee )
                payment.save()

                # income= TotalIncome.objects.get(id= session.id)
                # income= income.admission_fee + admission_fee
                # total_amount= TotalEarning.objects.filter(session= session.session).update(amount= income)
                # income= TotalIncome.objects.filter(id= session.id).update(admission_fee= income)
            else:
                admission_fee=0

            library_fee =  isFloat(request.POST.get('library-fee'))

            if type(library_fee )!= bool:
                payment= LibraryFee(user=Student.objects.get(id=id) , amount= library_fee )
                payment.save()

                # income= TotalIncome.objects.get(id= session.id)
                # income= income.library_fee + library_fee
                # total_amount= TotalEarning.objects.filter(session= session.session).update(amount= income)
                # income= TotalIncome.objects.filter(id= session.id).update(library_fee= income)
            else:
                library_fee=0

            poor_fund =  isFloat(request.POST.get('poor-fund'))

            if type(poor_fund )!= bool:
                payment= PoorFundFee(user=Student.objects.get(id=id) , amount= poor_fund )
                payment.save()

                # income= TotalIncome.objects.get(id= session.id)
                # income= income.poor_fund + poor_fund
                # total_amount= TotalEarning.objects.filter(session= session.session).update(amount= income)
                # income= TotalIncome.objects.filter(id= session.id).update(poor_fund= income)
            else:
                poor_fund=0

            st_fee =  isFloat(request.POST.get('st-fee'))

            if type(st_fee )!= bool:
                payment= ScienceAndTechnologyFee(user=Student.objects.get(id=id) , amount= st_fee )
                payment.save()

                # income= TotalIncome.objects.get(id= session.id)
                # income= income.science_and_tech + st_fee
                # total_amount= TotalEarning.objects.filter(session= session.session).update(amount= income)
                # income= TotalIncome.objects.filter(id= session.id).update(science_and_tech= income)
            else:
                st_fee=0

            cl_fee =  isFloat(request.POST.get('cl-fee'))
            
            if type(cl_fee )!= bool:
                payment= ComputerLab(user=Student.objects.get(id=id) , amount= cl_fee)
                payment.save()

                # income= TotalIncome.objects.get(id= session.id)
                # income= income.computer_lab_fee + cl_fee
                # total_amount= TotalEarning.objects.filter(session= session.session).update(amount= income)
                # income= TotalIncome.objects.filter(id= session.id).update(computer_lab_fee= income)
            else:
                cl_fee=0

            id_fee =  isFloat(request.POST.get('id-fee'))
            
            if type(id_fee )!= bool:
                payment= IdCardFee(user=Student.objects.get(id=id) , amount= id_fee)
                payment.save()

                # income= TotalIncome.objects.get(id= session.id)
                # income= income.id_fee + id_fee
                # total_amount= TotalEarning.objects.filter(session= session.session).update(amount= income)
                # income= TotalIncome.objects.filter(id= session.id).update(id_fee= income)
            else:
                id_fee=0
           
            reg =  isFloat(request.POST.get('reg-fee'))
                        
            if type(reg )!= bool:
                payment= RegistrationFee(user=Student.objects.get(id=id) , amount= reg )
                payment.save()

                # income= TotalIncome.objects.get(id= session.id)
                # income= income.reg_fee + reg
                # total_amount= TotalEarning.objects.filter(session= session.session).update(amount= income)
                # income= TotalIncome.objects.filter(id= session.id).update(reg_fee= income)
            else:
                reg=0
           
            rov_college =  isFloat(request.POST.get('rov-clg-fee'))
                                    
            if type(rov_college )!= bool:
                payment= CollegeRoversFee(user=Student.objects.get(id=id) , amount= rov_college )
                payment.save()

                # income= TotalIncome.objects.get(id= session.id)
                # income= income.college_rovers + rov_college
                # total_amount= TotalEarning.objects.filter(session= session.session).update(amount= income)
                # income= TotalIncome.objects.filter(id= session.id).update(college_rovers= income)
            else:
                rov_college=0
           
            rov_board = isFloat( request.POST.get('rov-board-fee'))
                                                
            if type(rov_board )!= bool:
                payment= BoardRoversFee(user=Student.objects.get(id=id) , amount= rov_board)
                payment.save()

                # income= TotalIncome.objects.get(id= session.id)
                # income= income.board_rovers + rov_board
                # total_amount= TotalEarning.objects.filter(session= session.session).update(amount= income)
                # income= TotalIncome.objects.filter(id= session.id).update(board_rovers= income)
            else:
                rov_board=0
            # print('admission: ', mp)
            # print('admission: ', admission_fee)
            # print('library: ',library_fee)
            # print('Poor: ',poor_fund)
            # print('clg: ',cl_fee)
            # print('st: ',st_fee)
            # print('id ',id_fee)

            

            income= TotalIncome.objects.get(id= session.id)
            income= TotalIncome.objects.filter(id= session.id).update(
                
                # total_amount= income.total_amount+ sum_of_income,
                admission_fee= income.admission_fee + admission_fee,
                milad_puja= income.milad_puja+ mp,
                college_devfee= income.college_devfee+ cd,
                library_fee=income.library_fee+ library_fee,
                poor_fund=income.poor_fund+ poor_fund,
                science_and_tech=income.science_and_tech+ st_fee,
                computer_lab_fee=income.computer_lab_fee+ cl_fee,
                id_fee=income.id_fee+ id_fee,
                reg_fee=income.reg_fee+ reg,
                college_rovers=income.college_rovers+ rov_college,
                board_rovers=income.college_rovers+ rov_board

            )

            # sum_of_income= sum_of_income+ mp+ admission_fee+ library_fee+ poor_fund+ st_fee+ cl_fee+id_fee+ reg+ rov_college+ rov_board
            


        # EXAM PAYMENT HERE 
        if exam == "True" :
            exam_fee = isFloat(request.POST.get('exam-fee'))

            if type(exam_fee )!= bool:
                payment= CollegeExamFee(user=Student.objects.get(id=id) , amount= exam_fee )
                payment.save()

            board_exam_fee = isFloat(request.POST.get('board-fee'))

            if type(board_exam_fee )!= bool:
                payment= BoardExamFee(user=Student.objects.get(id=id) , amount= board_exam_fee )
                payment.save()

            income= TotalIncome.objects.get(id= session.id)
            income= TotalIncome.objects.filter(id= session.id).update(
                
                college_examfee=income.college_examfee  + exam_fee,
                board_examfee=income.board_examfee  + board_exam_fee
            )



        # OTHERS PAYMENT HERE 
        if others == "True" :
            clg_sports_fee = isFloat(request.POST.get('clg-sports-fee'))

            if type(clg_sports_fee )!= bool:
                payment= CollegeSportsFee(user=Student.objects.get(id=id) , amount= clg_sports_fee )
                payment.save()

            board_sports_fee = isFloat(request.POST.get('board-sports-fee'))

            if type(board_sports_fee )!= bool:
                payment= BoardSportsFee(user=Student.objects.get(id=id) , amount= board_sports_fee )
                payment.save()

            transfer_fee = isFloat(request.POST.get('transfer-fee'))

            if type(transfer_fee )!= bool:
                payment= CollegeTranseferFee(user=Student.objects.get(id=id) , amount= transfer_fee )
                payment.save()

            certificate_fee = isFloat(request.POST.get('certificate-fee'))

            if type(certificate_fee )!= bool:
                payment= CertificateFee(user=Student.objects.get(id=id) , amount= certificate_fee )
                payment.save()

            ret_fee = isFloat(request.POST.get('ret-fee'))

            if type(ret_fee )!= bool:
                payment= RetentionFee(user=Student.objects.get(id=id) , amount= ret_fee )
                payment.save()

            test_fee = isFloat(request.POST.get('test-fee'))

            if type(test_fee )!= bool:
                payment= TestimonialFee(user=Student.objects.get(id=id) , amount= test_fee )
                payment.save()

            paper_fee = isFloat(request.POST.get('paper-fee'))

            if type(paper_fee )!= bool:
                payment= PaperMagazineFee(user=Student.objects.get(id=id) , amount= paper_fee )
                payment.save()

            practical_fee =isFloat( request.POST.get('practical-fee'))

            if type(practical_fee )!= bool:
                payment= PracticalFee(user=Student.objects.get(id=id) , amount= practical_fee )
                payment.save()

            water = isFloat(request.POST.get('bill'))

            if type(water )!= bool:
                payment= WaterFee(user=Student.objects.get(id=id) , amount= water )
                payment.save()

            management_fee = isFloat(request.POST.get('management-fee'))

            if type(management_fee )!= bool:
                payment= ManagementFee(user=Student.objects.get(id=id) , amount= management_fee )
                payment.save()

            fourth_fee = isFloat(request.POST.get('fourth-fee'))

            if type(fourth_fee )!= bool:
                payment= FourthPaperFee(user=Student.objects.get(id=id) , amount= fourth_fee )
                payment.save()

            late_fee = isFloat(request.POST.get('late-fee'))

            if type(late_fee )!= bool:
                payment= LateFee(user=Student.objects.get(id=id) , amount= late_fee )
                payment.save()

            center_fee = isFloat(request.POST.get('center-fee'))

            if type(center_fee )!= bool:
                payment= CenterFee(user=Student.objects.get(id=id) , amount= center_fee )
                payment.save()


            income= TotalIncome.objects.get(id= session.id)
            income= TotalIncome.objects.filter(id= session.id).update(
                
                college_sports_fee= income.college_sports_fee  + clg_sports_fee,
                board_sports_fee= income.board_sports_fee  + board_sports_fee,
                college_transfer= income.college_transfer  + transfer_fee,
                certificate_fee= income.certificate_fee  + certificate_fee,
                retention_fee= income.retention_fee  + ret_fee,
                testimonial_fee= income.testimonial_fee  + test_fee,
                paper_magazine= income.paper_magazine  + paper_fee,
                preactical_fee= income.preactical_fee  + practical_fee,
                bill= income.bill  + water,
                management_fee= income.management_fee  + management_fee,
                fourth_paper=income.fourth_paper  + fourth_fee,
                late_fine= income.late_fine  + late_fee,
                center= income.center  + center_fee,

            )
        # print("fee "+fee)
        # print("fee "+admission)
        # print("fee "+exam)
        # print("fee "+others)

    # user= User.objects.get(id=id)
        
        income= TotalIncome.objects.get(id= session.id)
        income= TotalIncome.objects.filter(id= session.id).update(
                
            total_amount= income.total_amount+ total,
            
        )

        total_amount= TotalEarning.objects.get(session= session.session)

        total_amount= TotalEarning.objects.filter(session= session.session).update(amount=total_amount.amount+ total)

        pay_slip=  StudentReceipt(                   
                    user= student,
                    total_amount= total,
                    year= student.student_year,  

                    
                    tutionfee= monthly_fee,
                    board_examfee= board_exam_fee,
                    college_examfee= exam_fee,
                    college_devfee= cd,
                    milad_puja= mp,
                    library_fee= library_fee,
                    college_sports_fee= clg_sports_fee,
                    board_sports_fee= board_sports_fee,
                    poor_fund= poor_fund,
                    donation= 0,
                    
                    science_and_tech= st_fee,
                    computer_lab_fee= cl_fee,
                    admission_fee= admission_fee,
                    reg_fee= reg,
                    college_rovers= rov_college,
                    board_rovers= rov_board,
                    college_transfer= transfer_fee,
                    id_fee= id_fee,
                    certificate_fee= certificate_fee,
                    retention_fee= ret_fee,
                    testimonial_fee= test_fee,
                    paper_magazine= paper_fee,
                    preactical_fee= practical_fee,
                    bill= water,
                    management_fee= management_fee,
                    fourth_paper= fourth_fee,
                    late_fine= late_fee,
                    center= center_fee,
                    
        )
        pay_slip.save()
        context= {'pay_slip': pay_slip, 'total': total}

        return render(request, 'dashboard/receipts.html', context) 
        
  
     
    months= MonthlyPayment.objects.filter(user= student, student_year=student.student_year)
    jsonDec = json.decoder.JSONDecoder()
    # m_list=[]
    # for m in months:
    #     if m_list:
    #         row=[]
    #         row=  jsonDec.decode(m.month)
    #         for item in row:
    #             m_list.append(item)
    #     else:
    #         m_list=  jsonDec.decode(m.month)
    m_list=[]
    for m in months:
        if m_list:
            row= []
            row= jsonDec.decode(m.month) 
            for item in row:   
                m_list.append(item)
        else:
            m_list=  jsonDec.decode(m.month)
            
       
    
    
    
    context= {'user': user, 'student': student, 'pay': pay, 'tution': tution, 'others': others, 'months': m_list}
    # print(student.name)
    # print(student.id)
    # print(student.email)
    # print(user.email)
    # print(pay.user.id)
    # print(pay.monthly)
    print(m_list)
    return render(request, 'dashboard/payment.html', context)   

    
# PARDON
def pardon(request, id):

    if request.method == 'POST':
        monthly_fee = float(request.POST.get('monthly-tuition-fee'))
        monthly_list = request.POST.get('monthly-list')
        monthly_list= monthly_list.split(",")  
        print(monthly_fee)
        for i in monthly_list:
            print(i)   

        

    # user= User.objects.get(id=id)
    student= Student.objects.get(id= id)
    user= User.objects.get(id= student.user.id)
    # pay= StudentPayment.objects.get(user= student)
    # tution= TutionFee.objects.get(class_name= student.course)
    # others= OthersCharge.objects.all().first()
    
    # context= {'user': user, 'student': student, 'pay': pay, 'tution': tution, 'others': others}
    context= {'user': user, 'student': student}
    # print(student.name)
    # print(student.id)
    # print(student.email)
    # print(user.email)
    # print(pay.user.id)
    # print(pay.monthly)
    return render(request, 'dashboard/pardon.html', context)   


# EXPENSES
def expense(request):

    govt_salary= 0
    house_rent_bonus= 0
    board_reg_fee= 0
    clg_exam_fee = 0
    clg_dev_fee= 0
    milad_puja= 0
    library_exp= 0
    sports_exp= 0
    poor_fund= 0
    water_bill= 0
    electric_bill= 0
    bank_charges= 0
    telephone_bill= 0
    st_exp= 0
    comp_lab= 0
    entertainment_exp= 0
    conveyance= 0
    printing_stationary= 0
    management_exp= 0
    others_exp= 0

    if request.method == 'POST':
        # monthly_fee = request.POST.get('monthly-tuition-fee')
        govt_salary =  isFloat(request.POST.get('govt-salary-fee'))
        if type(govt_salary )!= bool:
            payment= GovtSalaryExp(
                amount= govt_salary,
                details= request.POST.get('govt-salary-fee-d'),
                vauture= request.POST.get('govt-salary-fee-v'),
            )
            payment.save()
        else:
            govt_salary=0

        house_rent_bonus =  isFloat(request.POST.get('house-rent-bonus-fee'))
        if type(house_rent_bonus )!= bool:
            payment= HouseRentAndBonusExp(
                amount= house_rent_bonus,
                details= request.POST.get('house-rent-bonus-fee-d'),
                vauture= request.POST.get('house-rent-bonus-fee-v'),
            )
            payment.save()
        else:
            house_rent_bonus=0

        board_reg_fee =  isFloat(request.POST.get('board-reg-fee'))
        if type(board_reg_fee )!= bool:
            payment= BoardRegExp (
                amount= board_reg_fee,
                details= request.POST.get('board-reg-fee-d'),
                vauture= request.POST.get('board-reg-fee-v'),
            )
            payment.save()
        else:
            board_reg_fee=0

        # university_reg_fee =  request.POST.get('monthly-tuition-fee'))
        clg_exam_fee =  isFloat(request.POST.get('clg-exam-fee'))
        if type(clg_exam_fee )!= bool:
            
            payment= CollegeExamExp (
                amount= clg_exam_fee,
                details= request.POST.get('clg-exam-fee-d'),
                vauture= request.POST.get('clg-exam-fee-v'),
            )
            payment.save()
        else:
            clg_exam_fee=0

        clg_dev_fee =  isFloat(request.POST.get('clg-dev-fee'))
        if type(clg_dev_fee )!= bool:
            
            payment= CollegeDevExp (
                amount= clg_dev_fee,
                details= request.POST.get('clg-dev-fee-d'),
                vauture= request.POST.get('clg-dev-fee-v'),
            )
            payment.save()
        else:
            clg_dev_fee=0

        milad_puja =  isFloat(request.POST.get('mp-fee'))
        if type(milad_puja )!= bool:
            
            payment= MiladPujaExp (
                amount= milad_puja,
                details= request.POST.get('mp-fee-d'),
                vauture= request.POST.get('mp-fee-v'),
            )
            payment.save()
        else:
            milad_puja=0

        library_exp =  isFloat(request.POST.get('library-fee'))
        if type(library_exp )!= bool:
            
            payment= LibraryExp (
                amount= library_exp,
                details= request.POST.get('library-fee-d'),
                vauture= request.POST.get('library-fee-v'),
            )
            payment.save()
        else:
            library_exp=0

        sports_exp =  isFloat(request.POST.get('clg-sports-fee'))
        if type(sports_exp )!= bool:
            
            payment= SportsExp (
                amount= sports_exp,
                details= request.POST.get('clg-sports-fee-d'),
                vauture= request.POST.get('clg-sports-fee-v'),
            )
            payment.save()
        else:
            sports_exp=0

        poor_fund =  isFloat(request.POST.get('poor-fund'))
        if type(poor_fund )!= bool:
            
            payment= PoorFundExp (
                amount= poor_fund,
                details= request.POST.get('poor-fund-d'),
                vauture= request.POST.get('poor-fund-v'),
            )
            payment.save()
        else:
            poor_fund=0

        water_bill =  isFloat(request.POST.get('water-bill-fee'))
        if type(water_bill )!= bool:
             
            payment= WaterExp (
                amount= water_bill,
                details= request.POST.get('water-bill-fee-d'),
                vauture= request.POST.get('water-bill-fee-v'),
            )
            payment.save()
        else:
            water_bill=0

        electric_bill =  isFloat(request.POST.get('electric-bill-fee'))
        if type(electric_bill )!= bool:

            payment= ElectricExp (
                amount= electric_bill,
                details= request.POST.get('electric-bill-fee-d'),
                vauture= request.POST.get('electric-bill-fee-v'),
            )
            payment.save()
        else:
            electric_bill=0

        bank_charges =  isFloat(request.POST.get('bank-charges-fee'))
        if type(bank_charges )!= bool:
                
            payment= BankChargeExp (
                amount= bank_charges,
                details= request.POST.get('bank-charges-fee-d'),
                vauture= request.POST.get('bank-charges-fee-v'),
            )
            payment.save()
        else:
            bank_charges=0

        telephone_bill =  isFloat(request.POST.get('telephone-bill-fee'))
        if type(telephone_bill )!= bool:
                
            payment= TelephoneBillExp (
                amount= telephone_bill,
                details= request.POST.get('telephone-bill-fee-d'),
                vauture= request.POST.get('telephone-bill-fee-v'),
            )
            payment.save()
        else:
            telephone_bill=0


        st_exp =  isFloat(request.POST.get('st-fee'))
        if type(st_exp )!= bool:
                
            payment= ScienceAndTechnologyExp (
                amount= st_exp,
                details= request.POST.get('st-fee-d'),
                vauture= request.POST.get('st-fee-v'),
            )
            payment.save()
        else:
            st_exp=0

        comp_lab =  isFloat(request.POST.get('cl-fee'))
        if type(comp_lab )!= bool:
                 
            payment= ComputerLabExp (
                amount= comp_lab,
                details= request.POST.get('cl-fee-d'),
                vauture= request.POST.get('cl-fee-v'),
            )
            payment.save()
        else:
            comp_lab=0

        entertainment_exp =  isFloat(request.POST.get('entertainment-exp-fee'))
        if type(entertainment_exp )!= bool:
                 
            payment= EntertainmentExp (
                amount= entertainment_exp,
                details= request.POST.get('entertainment-exp-fee-d'),
                vauture= request.POST.get('entertainment-exp-fee-v'),
            )
            payment.save()
        else:
            entertainment_exp=0

        conveyance =  isFloat(request.POST.get('conveyance-fee'))
        if type(conveyance )!= bool:
                 
            payment= ConveyanceExp (
                amount= conveyance,
                details= request.POST.get('conveyance-fee-d'),
                vauture= request.POST.get('conveyance-fee-v'),
            )
            payment.save()
        else:
            conveyance=0

        printing_stationary =  isFloat(request.POST.get('printing-stationary-fee'))
        if type(printing_stationary )!= bool:
                  
            payment= PrintingAndStationaryExp (
                amount= printing_stationary,
                details= request.POST.get('printing-stationary-fee-d'),
                vauture= request.POST.get('printing-stationary-fee-v'),
            )
            payment.save()
        else:
            printing_stationary=0

        management_exp = isFloat( request.POST.get('management-exp-fee'))
        if type(management_exp )!= bool:
                  
            payment= ManagementExp (
                amount= management_exp,
                details= request.POST.get('management-exp-fee-d'),
                vauture= request.POST.get('management-exp-fee-v'),
            )
            payment.save()
        else:
            management_exp=0    

        # tutionfee_and_others_perdon =  request.POST.get('monthly-tuition-fee')
        others_exp =  isFloat(request.POST.get('others-exp-fee'))
        if type(others_exp )!= bool:
                  
            payment= OtherExp (
                amount= others_exp,
                details= request.POST.get('others-exp-fee-d'),
                vauture= request.POST.get('others-exp-fee-v'),
            )
            payment.save()
        else:
            others_exp=0

        session= TotalIncome.objects.last()

        total= (
            govt_salary+
            house_rent_bonus+
            board_reg_fee+
            clg_exam_fee +
            clg_dev_fee+
            milad_puja+
            library_exp+
            sports_exp+
            poor_fund+
            water_bill+
            electric_bill+
            bank_charges+
            telephone_bill+
            st_exp+
            comp_lab+
            entertainment_exp+
            conveyance+
            printing_stationary+
            management_exp+
            others_exp
        )
        all_exp= TotalExpances.objects.get(id= session.id)
        all_exp= TotalExpances.objects.filter(id= session.id).update(
            total_amount=all_exp.total_amount+ total,  
            govt_salary=all_exp.govt_salary+ govt_salary,
            house_rent=all_exp.house_rent+ house_rent_bonus,
            board_reg= all_exp.board_reg+ board_reg_fee,
            college_exam= all_exp.college_exam+  clg_exam_fee,
            college_dev= all_exp.college_dev+  clg_dev_fee,
            milad_puja= all_exp.milad_puja+  milad_puja,
            library_exp= all_exp.library_exp +library_exp,
            sports_exp= all_exp.sports_exp+ sports_exp,
            poor_fund_exp= all_exp.poor_fund_exp+  poor_fund,
            water_exp= all_exp.water_exp +water_bill,
            electric_exp= all_exp.electric_exp +electric_bill,
            telephone_exp= all_exp.telephone_exp +telephone_bill,
            bank_charges= all_exp.bank_charges +bank_charges,
            scinece_and_tech= all_exp.scinece_and_tech +st_exp,
            computer_lab_exp= all_exp.computer_lab_exp +comp_lab,
            entertainment_exp= all_exp.entertainment_exp +entertainment_exp,
            conveyance= all_exp.conveyance + conveyance,
            printing_and_stationary= all_exp.printing_and_stationary + printing_stationary,
            management_exp= all_exp.management_exp + management_exp,
            other= all_exp.other + management_exp,
        )

        total_amount= TotalEarning.objects.get(session= session.session)

        total_amount= TotalEarning.objects.filter(session= session.session).update(amount=total_amount.amount- total)


        messages.info(request, 'Successfully added') 
        return HttpResponseRedirect(reverse('expense'))
                    
        # print(govt_salary)
        # print(house_rent_bonus)
        # print(board_reg_fee)
        # # university_reg_fee
        # print(clg_exam_fee +10)
        # print(clg_dev_fee)
        # print(milad_puja)
        # print(library_exp)
        # print(sports_exp)
        # print(poor_fund)
        # print(water_bill)
        # print(electric_bill)
        # print(bank_charges)
        # print(telephone_bill)
        # print(st_exp)
        # print(comp_lab)
        # print(entertainment_exp)
        # print(conveyance)
        # print(printing_stationary)
        # print(management_exp)
        # # tutionfee_and_others_perdon
        # print(others_exp)

    
    context= {}
    
    return render(request, 'dashboard/expense.html', context)   

    
# MONTHLY PAYMENT
def monthly_payment(request):
    
    context= {}
    return render(request, 'dashboard/monthly-payment.html', context)   


# MONTHLY DONATION
def get_donation(request):
   
    context= {}
    return render(request, 'dashboard/donation-payment.html', context)   


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
    
