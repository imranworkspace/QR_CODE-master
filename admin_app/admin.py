from django.contrib import admin
from .models import AdminLoginModel
# Register your models here.
@admin.register(AdminLoginModel)
class AdminLoginAdmin(admin.ModelAdmin):
    list_display = ['id','username','password']