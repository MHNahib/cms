from django.db import models
from django.contrib.auth.models import User, auth

# Create your models here.

# DEPERTMENT
class Depertment(models.Model):
   
    dept_name= models.CharField(max_length=100, null=True, blank=False)

    def __str__(self):
        return self.dept_name


# STUDENT
class Student(models.Model):
    
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    roll= models.CharField(max_length=100, null=True)
    name= models.CharField(max_length=100, null=True, blank=False)
    group= models.CharField(max_length=100, null=True, blank=False)
    course= models.CharField(max_length=100, null=True, blank=False)
    session= models.CharField(max_length=100, null=True, blank=False)
    email= models.EmailField(max_length=100, null=True, blank=False)   
    img= models.ImageField(upload_to='profile/student/', blank=False) 
    # dept_name= models.OneToOneField(Depertment, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

# EDUCATIONAL QUALIFICATION OF STUDENT
class StudentEducation(models.Model):
    
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    ssc_roll= models.CharField(max_length=100, null=True, blank=False)  
    ssc_reg= models.CharField(max_length=100, null=True, blank=False)
    ssc_year= models.CharField(max_length=100, null=True, blank=False)
    ssc_grade= models.CharField(max_length=100, null=True, blank=False)    
    ssc_group= models.CharField(max_length=100, null=True, blank=False)    
    ssc_board= models.CharField(max_length=100, null=True, blank=False)    

    hsc_roll= models.CharField(max_length=100, null=True, blank=False)  
    hsc_reg= models.CharField(max_length=100, null=True, blank=False) 
    hsc_year= models.CharField(max_length=100, null=True, blank=False)   
    hsc_grade= models.CharField(max_length=100, null=True, blank=False)
    hsc_group= models.CharField(max_length=100, null=True, blank=False)
    hsc_board= models.CharField(max_length=100, null=True, blank=False)

    def __str__(self):
        return self.user.username
    
    

# ABOUT STUDENT
class StudentAbout(models.Model):

    user= models.OneToOneField(User, on_delete=models.CASCADE)
    fathers_name= models.CharField(max_length=100, null=True, blank=False)
    mothers_name= models.CharField(max_length=100, null=True, blank=False)
    blood_group= models.CharField(max_length=10, null=True, blank=False)
    gender= models.CharField(max_length=10, null=True, blank=False)
    nid= models.CharField(max_length=10, null=True, blank=False)
    date_of_birth= models.DateField()
    marital_status= models.CharField(max_length=50, null=True, blank=True)
    present_address= models.TextField(null=True, blank=False)
    permanent_address= models.TextField(null=True, blank=False)
    phone_number= models.CharField(max_length=50, null=True, blank=False)
    parents_number= models.CharField(max_length=50, null=True, blank=True)
    religion= models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username


# STUDENTS EXACT PAYMENT
class StudentPayment(models.Model):
    user= models.OneToOneField(Student, on_delete=models.CASCADE)
    total= models.FloatField(default=0)
    monthly= models.FloatField(default=0)

    def __str__(self):
        return self.user.name

# DONATION
class donation(models.Model):
    donar_name= models.CharField(max_length=100, null=True, blank=True)
    amount= models.FloatField(default=0)

    def __str__(self):
        return self.donar_name

# TUTION FEE
class TutionFee(models.Model):
    class_name= models.CharField(max_length=50, null=True, blank=True)
    # session= models.ForeignKey(SessionYear, on_delete=models.CASCADE)
    fee= models.FloatField(default=0)
    college_exam_fee= models.FloatField(default=0)
    board_exam_fee= models.FloatField(default=0)
    admision_fee= models.FloatField(default=0)
    registration_fee= models.FloatField(default=0)
    registration_fee= models.FloatField(default=0)
    college_transfer_fee= models.FloatField(default=0)
    id_fee= models.FloatField(default=0)
    certificate_fee= models.FloatField(default=0)
    retention_fee= models.FloatField(default=0)
    tc_fee= models.FloatField(default=0)
    management_fee= models.FloatField(default=0)
    fourth_paper_fee= models.FloatField(default=0)
    late_fee= models.FloatField(default=0)
    center_fee= models.FloatField(default=0)
    

    def __str__(self):
        return self.class_name
    

# OTHERS CHARGES
class OthersCharge(models.Model):
    # class_name= models.OneToOneField(TutionFee, on_delete=models.CASCADE)
    college_dev_fee= models.FloatField(default=0)
    milad_puja_fee= models.FloatField(default=0)
    library_fee= models.FloatField(default=0)
    college_sports_fee= models.FloatField(default=0)
    board_sports_fee= models.FloatField(default=0)
    poor_fund= models.FloatField(default=0)
    science_tech_fee= models.FloatField(default=0)
    computer_lab_fee= models.FloatField(default=0)
    computer_lab_fee= models.FloatField(default=0)
    computer_lab_fee= models.FloatField(default=0)
    college_rovers= models.FloatField(default=0)
    board_rovers= models.FloatField(default=0)
    paper_fee= models.FloatField(default=0)
    practical_fee= models.FloatField(default=0)
    bill= models.FloatField(default=0)

    def __str__(self):
        return str(self.college_dev_fee)



# TEACHER
class Teacher(models.Model):

    user= models.OneToOneField(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=100, null=True)
    email= models.EmailField(max_length=100, null=True)
    dept_name= models.ForeignKey(Depertment, on_delete=models.CASCADE)
    dept_head= models.BooleanField(default=False, blank=True)
    joining_date= models.DateField()
    phone_number= models.CharField(max_length=50, null=True)
    parents_number= models.CharField(max_length=50, null=True)
    teacher_img= models.ImageField(upload_to='profile/teacher/', blank=False)


    def __str__(self):
        return self.name

# EDUCATIONAL QUALIFICATION OF TEACHER
class TeacherEducation(models.Model):

    user= models.OneToOneField(User, on_delete=models.CASCADE)
    honours_year= models.CharField(max_length=100, null=True, blank=False)
    honours_grade= models.CharField(max_length=100, null=True, blank=False)
    masters_year= models.CharField(max_length=100, null=True, blank=False)   
    masters_grade= models.CharField(max_length=100, null=True, blank=False)

    def __str__(self):
        return self.user.username

# ABOUT TEACHER
class TeacherAbout(models.Model):

    user= models.OneToOneField(User, on_delete=models.CASCADE)
    blood_group= models.CharField(max_length=10, null=True, blank=False)
    date_of_birth= models.DateField(null= True)
    marital_status= models.CharField(max_length=50, null=True, blank=True)
    present_address= models.TextField(null=True, blank=False)
    permanent_address= models.TextField(null=True, blank=False)
    gender= models.CharField(max_length=10, null=True, blank=False)
    nid= models.CharField(max_length=10, null=True, blank=False)


    def __str__(self):
        return self.user.username




# DEPERTMENT INSTANCE
class DepertmentInstance(models.Model):
    teacher= models.OneToOneField(Teacher, on_delete=models.CASCADE)
    student= models.OneToOneField(Student, on_delete=models.CASCADE)
    dept_name= models.OneToOneField(Depertment, on_delete=models.CASCADE)

    def __str__(self):
        return self.dept_name



# SESSION YEAR
class SessionYear(models.Model):
    session_name= models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.session_name




# YEAR

class Year(models.Model):

    user= models.ForeignKey(Student, on_delete= models.CASCADE)
    # dept=  models.ForeignKey(Depertment, on_delete=models.CASCADE)
    # session= models.ForeignKey(SessionYear, on_delete= models.CASCADE)
    year_name= models.CharField( max_length=50, null=True)

    def __str__(self):
        return self.year_name


# SUBJECT
class Subject(models.Model):
    user= models.ForeignKey(User, on_delete= models.CASCADE)
    firstpaper_code= models.CharField(max_length=50, null=True, blank=True)
    secondpaper_code= models.CharField(max_length=50, null=True, blank=True)
    subject_name= models.CharField(max_length=50, null=True, blank=True)
    optional= models.BooleanField(default=False)


    def __str__(self):
        return self.user.first_name



# # ATTENDENCE
# class Attendence(models.Model):
#     present= models.BooleanField(default= False)
#     subject= models.ForeignKey(Subject, on_delete=models.CASCADE)
#     session_year= models.ForeignKey(SessionYear, on_delete=models.CASCADE)
#     Student= models.ForeignKey(Student, on_delete=models.CASCADE)
#     date= models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.Student.name


class Staff(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=100)
    email= models.EmailField(max_length=100, null=True)    
    joining_date= models.DateField()
    phone_number= models.CharField(max_length=50, null=True)
    parents_number= models.CharField(max_length=50, null=True)
    staff_img= models.ImageField(upload_to='profile/staff/', blank=False)

    def __str__(self):
        return self.name


# # TEACHERS CLASS
# class TeacherWillTake(models.Model):
#     teacher= models.OneToOneField(Teacher, on_delete=models.CASCADE)
#     subject= models.ManyToManyField(Subject)

#     def __str__(self):
#         return self.teacher.name



