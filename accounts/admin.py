from django.contrib import admin
# from accounts.models import Student, StudentEducation, StudentAbout, Teacher, TeacherEducation, TeacherAbout, Depertment, SessionYear, Subject, DepertmentInstance, Staff, Year, StudentPayment, TutionFee, OthersCharge, MonthlyPayment, TotalPaidMonths
from accounts.models import *
# Register your models here.

admin.site.register(Student)
admin.site.register(StudentEducation)
admin.site.register(StudentAbout)
admin.site.register(StudentReceipt)
admin.site.register(Teacher)
admin.site.register(TeacherEducation)
admin.site.register(Principal)
admin.site.register(PrincipalEducation)
admin.site.register(NormalStaff)
admin.site.register(Depertment)
admin.site.register(SessionYear)
admin.site.register(Subject)
admin.site.register(StudentPayment)
admin.site.register(TutionFee)
admin.site.register(OthersCharge)
admin.site.register(MonthlyPayment)
# admin.site.register(TotalPaidMonths)
# admin.site.register(YearWiseMonths)

# INCOME TABLE STARTS (students part)
# -------------------------------------------

admin.site.register(BoardExamFee)
admin.site.register(CollegeDevelopmentFee)
admin.site.register(MiladPujaFee)
admin.site.register(LibraryFee)
admin.site.register(CollegeSportsFee)
admin.site.register(BoardSportsFee)
admin.site.register(ScienceAndTechnologyFee)
admin.site.register(ComputerLab)
admin.site.register(AdmissionFee)
admin.site.register(RegistrationFee)
admin.site.register(CollegeRoversFee)
admin.site.register(BoardRoversFee)
admin.site.register(IdCardFee)
admin.site.register(CertificateFee)
admin.site.register(RetentionFee)
admin.site.register(TestimonialFee)
admin.site.register(PaperMagazineFee)
admin.site.register(PracticalFee)
admin.site.register(WaterFee)
admin.site.register(ManagementFee)
admin.site.register(FourthPaperFee)
admin.site.register(LateFee)
admin.site.register(CenterFee)

admin.site.register(PoorFundFee)
admin.site.register(BankInterestFee)
admin.site.register(donation)

# INCOME TABLE ends (students part)
# -------------------------------------------

# Expences college side Starts
# -----------------------------

admin.site.register(GovtSalaryExp)
admin.site.register(HouseRentAndBonusExp)
admin.site.register(BoardRegExp)
admin.site.register(CollegeExamExp)
admin.site.register(CollegeDevExp)
admin.site.register(MiladPujaExp)
admin.site.register(LibraryExp)
admin.site.register(SportsExp)
admin.site.register(PoorFundExp)
admin.site.register(WaterExp)
admin.site.register(ElectricExp)
admin.site.register(BankChargeExp)
admin.site.register(TelephoneBillExp)
admin.site.register(ScienceAndTechnologyExp)
admin.site.register(ComputerLabExp)
admin.site.register(EntertainmentExp)
admin.site.register(ConveyanceExp)
admin.site.register(PrintingAndStationaryExp)
admin.site.register(ManagementExp)
admin.site.register(PardonExp)
admin.site.register(OtherExp)

# Expences college side Ends
# -----------------------------


# TOTAL INCOME AND EXPENCES STARTS
# --------------------------------

admin.site.register(TotalEarning)
admin.site.register(TotalIncome)
admin.site.register(TotalExpances)

# TOTAL INCOME AND EXPENCES ENDS
# --------------------------------

# admin.site.register(Attendence)
admin.site.register(DepertmentInstance)
admin.site.register(Staff)
admin.site.register(Year)
# admin.site.register(TeacherWillTake)
