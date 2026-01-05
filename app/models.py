from django.db import models

# Create your models here.
class RegistrationModel(models.Model):
    empid=models.CharField(max_length=11)
    fname=models.CharField(max_length=75)
    lname=models.CharField(max_length=75)
    email=models.EmailField()
    mobile=models.CharField(max_length=11)
    website=models.CharField(max_length=75)
    password=models.CharField(max_length=255)
    confirm=models.CharField(max_length=255)
    image=models.ImageField(upload_to='media')
    profile_pic=models.ImageField(upload_to='profile_pic')
    date=models.DateField(auto_now=True)
    pdf=models.CharField(max_length=75)
    # profile_pic=models.ImageField(upload_to='profile_pic')

class AdminModel(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField()
    password=models.CharField(max_length=50)
    otp=models.CharField(max_length=8)

# class OtpModel(models.Model):
#     user = models.OneToOneField(RegistrationModel,on_delete=models.CASCADE)
#     mobile = models.CharField(max_length=20)
#     otp = models.CharField(max_length=6)

#     def __str__(self):
#         return self.fname