from django.contrib import admin
from accounts.models import Student, StudentEducation, StudentAbout, Teacher, TeacherEducation, TeacherAbout, Depertment, SessionYear, Subject, DepertmentInstance, Staff, Year
# Register your models here.

admin.site.register(Student)
admin.site.register(StudentEducation)
admin.site.register(StudentAbout)
admin.site.register(Teacher)
admin.site.register(TeacherEducation)
admin.site.register(TeacherAbout)
admin.site.register(Depertment)
admin.site.register(SessionYear)
admin.site.register(Subject)
# admin.site.register(Attendence)
admin.site.register(DepertmentInstance)
admin.site.register(Staff)
admin.site.register(Year)
# admin.site.register(TeacherWillTake)
