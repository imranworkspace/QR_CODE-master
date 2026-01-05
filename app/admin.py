from django.contrib import admin
from .models import RegistrationModel,AdminModel
# Register your models here.

@admin.register(RegistrationModel)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['id','empid','fname','lname','email','mobile','website','password','confirm','image','profile_pic','pdf','date']

@admin.register(AdminModel)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','password','otp']