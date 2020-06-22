from django.db import models
from django.contrib.auth.models import User, auth

# Create your models here.


# SESSION YEAR
class SessionYear(models.Model):
    session_name= models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.session_name

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
    student_year= models.CharField(max_length=100, null=True, blank=False)
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

# INCOME TABLE STARTS (students part)
# -------------------------------------------

# STUDENTS MONTHLY PAYMENT
class MonthlyPayment(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)
    student_year= models.CharField(null=True, max_length=55)
    month= models.TextField(null=True)
    date_time= models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.name

# STUDENTS MONTHLY PAID MONTHS
# class TotalPaidMonths(models.Model):
#     monthly_payment= models.OneToOneField(MonthlyPayment, on_delete=models.CASCADE)
#     month= models.TextField(null=True)

#     def __str__(self):
#         return self.monthly_payment.user.name

# STUDENT YEAR WISE MONTH ADDITON
# class YearWiseMonths(models.Model):
#     user= models.OneToOneField(Student, on_delete=models.CASCADE)    
#     student_year= models.CharField(null=True, max_length=55)
#     month= models.TextField(null=True)

#     def __str__(self):
#         return self.user.name

# College Exam Fee
class CollegeExamFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name




# Board Exam Fee
class BoardExamFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name





# College Development Fee
class CollegeDevelopmentFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name


# Milad Puja Fee
class MiladPujaFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name


# Library Fee
class LibraryFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name


#  College Sports Fee
class CollegeSportsFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

#  Board Sports Fee
class BoardSportsFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

#  Science and technology Fee
class ScienceAndTechnologyFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

#  Computer Lab Fee
class ComputerLab(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

#  Admission Fee
class AdmissionFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

#  Registration Fee
class RegistrationFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

#  Collge Rovers Fee
class CollegeRoversFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

#  Board Rovers Fee
class BoardRoversFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

#  College Transefer Rovers Fee
class CollegeTranseferFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

#  ID Card Fee
class IdCardFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

#  Certificate Fee
class CertificateFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

#  Retention Fee
class RetentionFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

#  Testimonial Fee
class TestimonialFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

#  Paper Magazine Fee
class PaperMagazineFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

#  Practical Fee
class PracticalFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

#  Water Fee
class WaterFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

#  Management Fee
class ManagementFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

#  Fourth paper Fee
class FourthPaperFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

#  Late Fee
class LateFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name


#  center Fee
class CenterFee(models.Model):
    user= models.ForeignKey(Student, on_delete=models.CASCADE)
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name


# INCOME TABLE ENDS (student part)
# ---------------------------------


# Income college side starts
# -----------------------------

#  PoorFund Fee
class PoorFundFee(models.Model):    
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name

#  Bank Interest Fee
class BankInterestFee(models.Model):    
    amount= models.FloatField(default=0)    
    date_time= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name


# DONATION
class donation(models.Model):
    donar_name= models.CharField(max_length=100, null=True, blank=True)
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.donar_name

# Income college side ends
# -----------------------------


# Expences college side Starts
# -----------------------------

# Govt. salary Expenses
class GovtSalaryExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date


# House rent and bonus Expenses
class HouseRentAndBonusExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date


# Board Registration Expenses
class BoardRegExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date


# College Exam Expenses
class CollegeExamExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date


# College Development Expenses
class CollegeDevExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date


# Milad Puja Expenses
class MiladPujaExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date


# Library Expenses
class LibraryExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date


# Sports Expenses
class SportsExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date


# Poor fund Expenses
class PoorFundExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date


# Water Expenses
class WaterExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date


# Electric Expenses
class ElectricExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date


# Bank Charge Expenses
class BankChargeExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date


# Telephone Bill Expenses
class TelephoneBillExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date


# Science and technology Expenses
class ScienceAndTechnologyExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date


# Computer lab Expenses
class ComputerLabExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date


# Entertainment Expenses
class EntertainmentExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date


# Conveyance Expenses
class ConveyanceExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date


# Printing and stationary Expenses
class PrintingAndStationaryExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date


# Management Expenses
class ManagementExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date


# Tution fee and other charges pardon
class PardonExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date


# Other Expenses
class OtherExp(models.Model):    
    amount= models.FloatField(default=0)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.date



# Expences college side ends
# -----------------------------


# TOTAL INCOME AND EXPENCES STARTS
# --------------------------------

# TOTAL
class TotalEarning(models.Model):
    amount= models.FloatField(default=0)
    session= models.OneToOneField( SessionYear, on_delete=models.CASCADE)
    update_date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.session.session_name


# TOTAL INCOME IN SESSION
class TotalIncome(models.Model):
    total_amount= models.FloatField(default=0)
    session= models.OneToOneField(SessionYear, on_delete=models.CASCADE)
    update_date= models.DateTimeField(auto_now_add=True)

    govt_reuneration= models.FloatField(default=0)
    hsc_tutionfee= models.FloatField(default=0)
    honours_tutionfee= models.FloatField(default=0)
    degree_tutionfee= models.FloatField(default=0)
    board_examfee= models.FloatField(default=0)
    college_devfee= models.FloatField(default=0)
    milad_puja= models.FloatField(default=0)
    library_fee= models.FloatField(default=0)
    college_sports_fee= models.FloatField(default=0)
    board_sports_fee= models.FloatField(default=0)
    poor_fund= models.FloatField(default=0)
    donation= models.FloatField(default=0)
    bank_interest= models.FloatField(default=0)
    science_and_tech= models.FloatField(default=0)
    computer_lab_fee= models.FloatField(default=0)
    admission_fee= models.FloatField(default=0)
    reg_fee= models.FloatField(default=0)
    college_rovers= models.FloatField(default=0)
    board_rovers= models.FloatField(default=0)
    college_transfer= models.FloatField(default=0)
    id_fee= models.FloatField(default=0)
    certificate_fee= models.FloatField(default=0)
    retention_fee= models.FloatField(default=0)
    testimonial_fee= models.FloatField(default=0)
    paper_magazine= models.FloatField(default=0)
    preactical_fee= models.FloatField(default=0)
    bill= models.FloatField(default=0)
    management_fee= models.FloatField(default=0)
    fourth_paper= models.FloatField(default=0)
    late_fine= models.FloatField(default=0)
    center= models.FloatField(default=0)

    def __str__(self):
        return self.session.session_name



# TOTAL EXPENCES IN SESSION
class TotalExpances(models.Model):
    total_amount= models.FloatField(default=0)
    session= models.OneToOneField(SessionYear, on_delete=models.CASCADE)
    update_date= models.DateTimeField(auto_now_add=True)

    govt_salary= models.FloatField(default=0)
    house_rent= models.FloatField(default=0)
    board_reg= models.FloatField(default=0)
    college_exam= models.FloatField(default=0)
    college_dev= models.FloatField(default=0)
    milad_puja= models.FloatField(default=0)
    library_exp= models.FloatField(default=0)
    sports_exp= models.FloatField(default=0)
    poor_fund_exp= models.FloatField(default=0)
    water_exp= models.FloatField(default=0)
    electric_exp= models.FloatField(default=0)
    telephone_exp= models.FloatField(default=0)
    bank_charges= models.FloatField(default=0)
    scinece_and_tech= models.FloatField(default=0)
    computer_lab_exp= models.FloatField(default=0)
    entertainment_exp= models.FloatField(default=0)
    conveyance= models.FloatField(default=0)
    printing_and_stationary= models.FloatField(default=0)
    management_exp= models.FloatField(default=0)
    pardon= models.FloatField(default=0)
    other= models.FloatField(default=0)

    def __str__(self):
        return self.session.session_name
     


# TOTAL INCOME AND EXPENCES ENDS
# --------------------------------



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
    # computer_lab_fee= models.FloatField(default=0)
    # computer_lab_fee= models.FloatField(default=0)
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



