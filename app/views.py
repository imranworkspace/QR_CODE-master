
from django.shortcuts import redirect, render,HttpResponseRedirect,HttpResponse
from django.urls import NoReverseMatch
# from resizeimage import resizeimage
import qrcode
from PIL import Image,ImageDraw,ImageFont
from .forms import RegistrationForm,AdminForm,IndexForm,ForgotPasswordForm,ForgotSuccessForm
from .models import RegistrationModel,AdminModel
from django.http import HttpResponseRedirect
# for modelform
from django.db import IntegrityError
from datetime import date
import os
from django.views.decorators.csrf import csrf_exempt
# for pagination
from django.core.paginator import Paginator
# for search
from django.db.models import Q
# to get queryset to json to string
import json
from django.core.serializers.json import DjangoJSONEncoder
# messages
from django.contrib import messages
import re
from django.core.exceptions import ObjectDoesNotExist

import random
import http.client
from django.conf import settings
# handle empty object 
import smtplib
from email.mime.text import MIMEText

from django.conf import settings
from django.core.mail import send_mail
import datetime
import random
import string
# convert png to pdf
import img2pdf
# for sending mail with attchement
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
# camera library
import cv2
from time import sleep
import os

session_msg = 'oops!!! session expired please login again'

def camera_fun(request):
    key = cv2.waitKey(1)
    webcam = cv2.VideoCapture(0)
    sleep(2)
    while True:
        try:
            check, frame = webcam.read()
            print(check)  # prints true as long as the webcam is running
            print(frame)  # prints matrix values of each frame
            saved_id = random.randint(10000000, 90000000)
            request.session['saved_id']=saved_id
            imgpath_new = "image/profile_pic/"+str(saved_id) + '.jpg'
            cv2.imshow("GatePass-User  Press-S for Save Photo, Q for Quit", frame)
            myname = 'imran'
            key = cv2.waitKey(1)
            if key == ord('s'):
                cv2.imwrite(os.path.join(imgpath_new), frame)
                webcam.release()
                print("Processing image...")
                imgpath = imgpath_new
                img_ = cv2.imread(imgpath_new,cv2.IMREAD_ANYCOLOR)
                print("Converting RGB image to grayscale...")
                # gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
                print("Converted RGB image to grayscale...")
                print("Resizing image to 28x28 scale...")
                # img_ = cv2.resize(gray, (350, 350)) # for gray
                img_ = cv2.resize(img_, (350, 350))  # for colorimage
                print("Resized...")
                # imgpath = 'image/profile_pic/saved_img.jpg'
                img_resized = cv2.imwrite(os.path.join(imgpath), img_)
                print("Image saved!")
                request.session['pic']=imgpath
                webcam.release()
                cv2.destroyAllWindows()
                return redirect('/')
                break
                
            elif key == ord('q'):
                # print('pressed q ',key)
                webcam.release()
                cv2.destroyAllWindows()
                return redirect('/')
                break
        
        except KeyboardInterrupt:
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break
            
# employee list records on userlist
total_records=4

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data['Email']
                # set session on email id 
                request.session['email']=email
                print('session set successfully for 60 secs')                
                # get user id and set session on id using email
                id = AdminModel.objects.get(email=email).pk
                # request.session['id'] = id
                match_email = AdminModel.objects.filter(email=email).exists()
                print('type match email ',type(match_email))
                if match_email == True:
                    password_characters = string.ascii_letters + string.digits + string.punctuation
                    password = ''.join(random.choice(password_characters)
                                    for i in range(8))
                    print("Random password is:", password)
                    # Output $z#m;-fb
                    subject = 'welcome to QR-CODE'
                    message = f'Hi forgot password key by QR CODE '+password
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [email,]
                    send_mail( subject, message, email_from, recipient_list)
                    
                    otp = AdminModel.objects.filter(email=email).update(otp=password)
                    match_otp = AdminModel.objects.filter(otp=otp).exists() # check otp exist or not
                    # print('type match otp ',match_otp)
                    if match_otp == True:
                        print('### otp match 2')
                        redirect('forgotsuccess')
                    #otp not match
                    else:
                        print('### otp not match')
                        form = ForgotSuccessForm()
                        context = {
                            'form':form,
                            'Email':email,
                            'message':'otp sent on '+email+" successfully",
                            'class':'success' 
                        }  
                        # forgot_success(request,email)
                        return render(request,'forgot_success.html',context)     
                # email not match
                elif match_email == False:
                    print('match failed')
                    context = {
                        'form':form,
                        'Email':email,
                        'message':'email does not exist ',
                        'class':'danger' 
                    }  
                    return render(request,'forgot.html',context)
            except AdminModel.DoesNotExist as d:
                print('inside exception')
                context ={
                        'form':form,
                        'message':'email does not exist',
                        'class':'danger'
                    }
                return render(request,'forgot.html',context)    
    else:
        form = ForgotPasswordForm()
    return render(request,'forgot.html',{'form':form})

def forgot_success(request):
    if request.method == 'POST':
        # get email id by session
        email = request.session.get('email')
        print('### email ',email)
        form = ForgotSuccessForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            print(otp)
            print(new_password)
            print(confirm_password)
            match_otp = AdminModel.objects.filter(otp=otp).exists() # check otp exist or not
            print('type match otp ',match_otp)
            if match_otp == True:
                if new_password == confirm_password:
                    # form.save() 
                    update = AdminModel.objects.filter(email=email).update(password=confirm_password) # update password column based on email id
                    print('update ',update)
                    # session cleared successfully
                    request.session.flush()
                    request.session.clear_expired()
                    form = IndexForm()
                    context = {
                        'form':form,
                        'message':'password changed successfully',
                        'class':'success' 
                    }  
                    return render(request,'login_page.html',context)
                elif new_password != confirm_password:
                    context = {
                        'form':form,
                        'message':'new password and confirm password does not matched',
                        'class':'danger' 
                    }  
                    return render(request,'forgot_success.html',context)
            # otp not matched
            else:
                context = {
                        'form':form,
                        'message':'otp does not matched please enter correct otp',
                        'class':'danger'}  
                return render(request,'forgot_success.html',context)
    else:
        print('get method ')
        form = ForgotSuccessForm()
    return render(request,'forgot_success.html',{'form':form,'message':'otp send on','class':'success'})

def homepage(request):
    # # generating a QR code using the make() function  
    qr_img = qrcode.make("http://127.0.0.1:8000/login_page") 
    # saving the image file  
    qr_img.save("homepage.jpg")
    try:
        if request.method == 'POST':
            print('post data')
            form = AdminForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                password = form.cleaned_data['password']
                reg_save = AdminModel(name=name,password=password)
                reg_save.save()
                print('data saved into db ')
        else:
            form = AdminForm()
        return render(request,'homepage.html',{'form':form})
    except NoReverseMatch as norevermatch:
        print('for change password no id found so we are handle here exception',norevermatch)
        context ={
                    'form':form,
                    'message':'for change password no id found so we are handle here exception',
                    'class':'danger'
                    }
        return render(request,'homepage.html',context)

# Create your views here.
def registration(request):
    username = request.session.get('username')
    if username == None:
        return redirect('login_page')
    print('registration session ',username)
    print('registration session ',type(username))
    if request.method == 'POST':
        try:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                fname = form.cleaned_data['fname']
                lname = form.cleaned_data['lname']
                email = form.cleaned_data['email']
                mobile = form.cleaned_data['mobile']
                website = form.cleaned_data['website']
                password = form.cleaned_data['password']
                confirm = form.cleaned_data['confirm']
                print('in try generate block executed')
                firstname=fname
                fullname=fname+'_'+lname
                image = Image.new('RGB', (1000, 900), (255, 255, 255))
                draw = ImageDraw.Draw(image)
                font = ImageFont.truetype('arial.ttf', size=45)
                # os.system("Title: ID CARD Generator by Imran Shaikh")
                d_date = datetime.datetime.now()
                reg_format_date = d_date.strftime("  %d-%m-%Y\t\t\t\t\t ID CARD Generator\t\t\t\t\t  %I:%M:%S %p")
                print(
                    '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print(reg_format_date)
                print(
                    '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                today = date.today()
                current_date= today.strftime("%b-%d-%Y")
                # starting position of the message
                (x, y) = (50, 50)
                company = "GatePass"
                color = 'rgb(0, 0, 0)' # black color
                font = ImageFont.truetype('arial.ttf', size=60)
                draw.text((x, y), company, fill=color, font=font)
                # adding an unique id number. You can manually take it from user

                (x, y) = (50, 135) 
                message = str('crtd by -> ' + username)
                color = 'rgb(0, 0, 0)'  # black color
                font = ImageFont.truetype('arial.ttf', size=39)
                draw.text((x, y), message, fill=color, font=font)


                (x, y) = (600, 60)
                idno = request.session.get('saved_id')
                empid=idno
                message = str('EmpID:' + str(idno))
                color = 'rgb(0, 0, 0)'  # black color
                font = ImageFont.truetype('arial.ttf', size=45)
                draw.text((x, y), message, fill=color, font=font)
                
                # For the Name
                (x, y) = (50, 580)
                # name = firstname 
                fname = str('F: ' + str(fname))
                color = 'rgb(0, 0, 0)'  # black color
                font = ImageFont.truetype('arial.ttf', size=45)
                draw.text((x, y), fname.capitalize(), fill=color, font=font)
                # # For the gender
                (x, y) = (50, 650)
                fgender = str('L: ' + str(lname))
                color = 'rgb(0, 0, 0)'  # black color
                draw.text((x, y), fgender.capitalize(), fill=color, font=font)
                # For the Mob No
                (x, y) = (50, 720)
                fNo = str('M: ' + str(mobile))
                color = 'rgb(0, 0, 0)'  # black color
                draw.text((x, y), fNo, fill=color, font=font)
                # For the Address
                (x, y) = (50, 782)
                femail = str('E: ' + str(email))
                color = 'rgb(0, 0, 0)'  # black color
                draw.text((x, y), femail.capitalize(), fill=color, font=font)
                (x, y) = (50, 845)
                faddress = str('C: ' + str(website))
                color = 'rgb(0, 0, 0)'  # black color
                draw.text((x, y), faddress.capitalize(), fill=color, font=font)
                # save the edited image
                image.save("image/media/"+str(idno) + '.png')
                QR=qrcode.make(f"Emp-id:{empid}\nFirstName:{firstname}\nLastname:{lname}\nEmail:{email}\nMobile:{mobile}\nCompany:{website}")
                QR.save("image/media/"+str(idno)+'.bmp')
                # print('### image saved')
                # print('QR Code Generated Successfully')
                profile_pic = request.session.get('pic')
                # print('##### profile pic ',profile_pic)
                if profile_pic==None:
                    context ={
                            'form':form,
                            'message':'please upload image',
                            'class':'danger'
                            }
                    return render(request,"gate_pass_registration.html",context)
                ID = Image.open("image/media/"+str(idno) + '.png')
                QR = Image.open("image/media/"+str(idno) + '.bmp')  # 25x25
                pic = Image.open(str(profile_pic))  # 25x25
                ID.paste(QR, (450, 175))
                ID.paste(pic, (35, 220))
                ID.save("image/media/"+str(idno) + '.png')
                img="image/media/"+str(idno) + '.png'
                print(('\n\n\nYour ID Card Successfully created in a PNG file ' + str(idno) + '.png'))
                # print('## ',password)
                # print(confirm)
                # print(img)
                # print('data saved into db ')
                image=Image.open(img)
                if image.mode == "RGBA":
                    image=image.convert("RGB")
                output = "image/mypdf/"+str(idno) + '.pdf'
                if not os.path.exists(output):
                    image.save(output,"PDF",resolution=100.0)
                    # print('pdf file created')
                reg_save = RegistrationModel(empid=empid,fname=firstname,lname=lname,email=email,mobile=mobile,website=website,password=password,confirm=confirm,image=img,profile_pic=profile_pic,date=current_date,pdf=output)
                reg_save.save()
                # print('pdf file created successfully')
                # check_user = OtpModel.objects.filter(email=email).first()
                # check_profile = OtpModel.objects.filter(mobile=mobile).first()
                # if check_user or check_profile:
                #     context = {'message':'user already exist ','class':'danger'}
                #     return render(request,'gate_pass_registration.html',context)
                # otp = str(random.randint(1000,9999))
                # profile = OtpModel(user=reg_save,mobile=mobile,otp=otp)
                # profile.save()
                # send_otp(mobile,otp)
                request.session['mobile']=mobile
                id = RegistrationModel.objects.all().last()
                user = firstname.capitalize() + " "+ lname.capitalize()
                username = request.session.get('username')
                # send email notification with pdf 
                subject = 'Welcome To GatePass QR-Code Generator'
                message = 'Thank you!!! for registration with us PFA '
                from django.core.mail import EmailMessage
                mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
                mail.attach_file(output)
                mail.send()
                context ={
                    'username':username,
                    'form':form,
                    'id':id,
                    'user':user,
                    'message':'Gate pass created for '+user+ ' successfully and qrcode sent on '+email,
                    'class':'success'
                    }
                return render(request,"gate_pass_registration.html",context)
            else:
                context = {'form':form,}
                return render(request,"gate_pass_registration.html",context)
        except IntegrityError as e:
            print('except block')
            e = 'user available in db'
            context = {
                'username':username,
                'form':form,
                'e':e}
    else:    
        print("get block executed")
        form = RegistrationForm()   # get emtpy form
        context = {'form':form,'username':username}
    return render(request,"gate_pass_registration.html",context)

# delete record
def delete_record(request,id):
    if request.method == 'POST':
        id = RegistrationModel.objects.get(pk=id)
        id.delete()
        return redirect('userlist')
# delete record
def delete_subadmin(request,id):
    if request.method == 'POST':
        id = AdminModel.objects.get(pk=id)
        id.delete()
        sub_admin_list = AdminModel.objects.order_by('-id')
        # for pagination
        paginator=Paginator(sub_admin_list,total_records)
        page_number=request.GET.get('page')
        sub_admin_list=paginator.get_page(page_number)
        context={
            'sub_admin_list':sub_admin_list,
            'message':'user deleted successfully',
            'class':'success'
        }
        return render(request,'sub_admin_list.html',context)

def admin_dashboard(request):
    admin_count=AdminModel.objects.count()
    emp_count=RegistrationModel.objects.count()
    context={
        'admin_count':admin_count,
        'emp_count':emp_count,
    }
    return render(request,"admin_dashboard.html",context)

# update_record record
def update_subadmin(request,id):
    if request.method == 'POST':
        id = AdminModel.objects.get(pk=id)
        form = AdminForm(request.POST,instance=id)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            form.save()
            form = IndexForm()
            sub_admin_list = AdminModel.objects.order_by('-id')
            # for pagination
            paginator=Paginator(sub_admin_list,total_records)
            page_number=request.GET.get('page')
            sub_admin_list=paginator.get_page(page_number)
            context ={
                    'sub_admin_list':sub_admin_list,
                    'form':form,
                    'id':id,
                    'message':'User Updated Successfully',
                    'class':'success'
                    }
            return render(request,"sub_admin_list.html",context)

    else:
        id = AdminModel.objects.get(pk=id)
        form=AdminForm(instance=id)
        context ={
            'form':form,
        }
    return render(request,"sub_admin_update.html",context)

def add_subadmin(request):
    try:
        if request.method == 'POST':
                form = AdminForm(request.POST)
                if form.is_valid():
                    name = form.cleaned_data['name']
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    reg_save = AdminModel(name=name,email=email,password=password)
                    reg_save.save()
                    return redirect('sub_admin_list')
        else:
            form = AdminForm()
        return render(request,'add_subadmin.html',{'form':form})
    except NoReverseMatch:
        form = IndexForm()
        context ={
                'form':form,
                'message':session_msg,
                'class':'danger'
                }
        return render(request,'admin_login.html',context)

# update_record record
def update_record(request,id,empid):
    get_image=''
    get_pdf=''

    id_no = RegistrationModel.objects.raw('select *from app_registrationmodel where empid=%s',[empid])
    for i in id_no:
        get_image = i.image
        get_pdf = i.pdf
        
    if request.method == 'POST':
        id = RegistrationModel.objects.get(pk=id)
        form = RegistrationForm(request.POST,instance=id)
        if form.is_valid():
                fname = form.cleaned_data['fname']
                lname = form.cleaned_data['lname']
                email = form.cleaned_data['email']
                mobile = form.cleaned_data['mobile']
                website = form.cleaned_data['website']
                password = form.cleaned_data['password']
                confirm = form.cleaned_data['confirm']
                print('in try generate block executed')
                firstname=fname
                fullname=fname+'_'+lname
                image = Image.new('RGB', (1000, 900), (255, 255, 255))
                draw = ImageDraw.Draw(image)
                font = ImageFont.truetype('arial.ttf', size=45)
                # os.system("Title: ID CARD Generator by Imran Shaikh")
                d_date = datetime.datetime.now()
                reg_format_date = d_date.strftime("  %d-%m-%Y\t\t\t\t\t ID CARD Generator\t\t\t\t\t  %I:%M:%S %p")
                print(
                    '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print(reg_format_date)
                print(
                    '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                today = date.today()
                current_date= today.strftime("%b-%d-%Y")
                # starting position of the message
                (x, y) = (50, 50)
                company = "GatePass"
                color = 'rgb(0, 0, 0)' # black color
                font = ImageFont.truetype('arial.ttf', size=80)
                draw.text((x, y), company, fill=color, font=font)
                # adding an unique id number. You can manually take it from user
                (x, y) = (50, 145) 
                username = request.session.get('username')
                message = str('modi by -> ' + username)
                color = 'rgb(0, 0, 0)'  # black color
                font = ImageFont.truetype('arial.ttf', size=39)
                draw.text((x, y), message, fill=color, font=font)

                (x, y) = (600, 65)
                idno = request.session.get('saved_id')
                if idno==None:
                    idno=empid
                    print('saved id ',idno)
                empid=idno
                message = str('EmpID:' + str(idno))
                color = 'rgb(0, 0, 0)'  # black color
                font = ImageFont.truetype('arial.ttf', size=45)
                draw.text((x, y), message, fill=color, font=font)
                # For the Name
                (x, y) = (50, 580)
                # name = firstname 
                fname = str('F: ' + str(fname))
                color = 'rgb(0, 0, 0)'  # black color
                font = ImageFont.truetype('arial.ttf', size=45)
                draw.text((x, y), fname.capitalize(), fill=color, font=font)
                # # For the gender
                (x, y) = (50, 650)
                fgender = str('L: ' + str(lname))
                color = 'rgb(0, 0, 0)'  # black color
                draw.text((x, y), fgender.capitalize(), fill=color, font=font)
                # For the Mob No
                (x, y) = (50, 720)
                fNo = str('M: ' + str(mobile))
                color = 'rgb(0, 0, 0)'  # black color
                draw.text((x, y), fNo, fill=color, font=font)
                # For the Address
                (x, y) = (50, 782)
                femail = str('E: ' + str(email))
                color = 'rgb(0, 0, 0)'  # black color
                draw.text((x, y), femail.capitalize(), fill=color, font=font)
                (x, y) = (50, 845)
                faddress = str('C: ' + str(website))
                color = 'rgb(0, 0, 0)'  # black color
                draw.text((x, y), faddress.capitalize(), fill=color, font=font)
                # save the edited image
                image.save("image/media/"+str(idno) + '.png')
                QR=qrcode.make(f"Emp-id:{empid}\nFirstName:{firstname}\nLastname:{lname}\nEmail:{email}\nMobile:{mobile}\nCompany:{website}")
                QR.save("image/media/"+str(idno)+'.bmp')
                # print('### image saved')
                # print('QR Code Generated Successfully')
                profile_pic = request.session.get('pic')
                print('profile pic 1',profile_pic)
                if profile_pic == None:
                    profile_pic = "image/profile_pic/"+str(empid) + '.jpg' 
                    print('profile pic 2',profile_pic)
                ID = Image.open("image/media/"+str(idno) + '.png')
                QR = Image.open("image/media/"+str(idno) + '.bmp')  # 25x25
                pic = Image.open(profile_pic)  # 25x25
                ID.paste(QR, (450, 175))
                ID.paste(pic, (35, 220))
                ID.save("image/media/"+str(idno) + '.png')
                img="image/media/"+str(idno) + '.png'
                print(('\n\n\nYour ID Card Successfully created in a PNG file ' + str(idno) + '.png'))
                
                image=Image.open(img)
                if image.mode == "RGBA":
                    image=image.convert("RGB")
                output = get_pdf
                image.save(output,"PDF",resolution=100.0)
                request.session['mobile']=mobile
                id = RegistrationModel.objects.all().last()
                user = firstname.capitalize() + " "+ lname.capitalize()
                username = request.session.get('username')
                userlist = RegistrationModel.objects.order_by('-id')
                # send email notification with pdf 
                subject = 'Welcome To GatePass QR-Code Generator'
                message = 'your qrcode updated successfully PFA '
                from django.core.mail import EmailMessage
                mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
                mail.attach_file(output)
                mail.send()
                form.save()
                context ={
                    'username':username,
                    'userlist':userlist,
                    'form':form,
                    'id':id,
                    'user':user,
                    'message':'Gate pass updated for '+user+ ' successfully and qrcode sent on '+email,
                    'class':'success'
                    }
                return render(request,"userlist.html",context)            
    else:
        id = RegistrationModel.objects.get(pk=id)
        form = RegistrationForm(instance=id)
        # try:
        #     # hide fname and lname on upadate page because qr code ganerated based on fname and lname
        #     form.fields['fname'].widget.attrs['readonly'] = True 
        #     form.fields['lname'].widget.attrs['readonly'] = True 
        #     form.fields['email'].widget.attrs['readonly'] = True 
        #     form.fields['mobile'].widget.attrs['readonly'] = True 
        #     form.fields['website'].widget.attrs['readonly'] = True 
        # except KeyError as k:
        #     print('key error for name and email ',k)
    return render(request,'gate_pass_user_update_record.html',{'form':form})
    
# update_profile record
def profile_update(request,id):
    try:
        if request.method == 'POST':
            id = AdminModel.objects.get(pk=id)
            form = AdminForm(request.POST,instance=id)
            if form.is_valid():
                form.save() 
                form = IndexForm()    
                context = {
                    'form':form,
                    'message':'profile updated successfully',
                    'class':'success' 
                }  
                return render(request,'login_page.html',context)
        else:
            id = AdminModel.objects.get(pk=id)
            form = AdminForm(instance=id)
            try:
                # hide password filled
                form.fields['password'].widget.attrs['readonly'] = True 
                form.fields['otp'].widget.attrs['readonly'] = True 
                form.fields['email'].widget.attrs['readonly'] = True 
            except KeyError as k:
                print('key error for paasword ',k)
        return render(request,'profile_update.html',{'form':form})
    except NoReverseMatch:
        form = IndexForm()
        context ={
                'form':form,
                'message':'',
                'class':'danger'
                }
        return render(request,'login_page.html',context)

def userlist_fun(request):
    # get q name from search box
    try:
        if 'q' in request.GET:
            q_search=request.GET['q']
            q = q_search.strip()
            # search in multiple columns
            multiple_q = Q(Q(empid__contains=q) | Q(fname__contains=q) | Q(lname__contains=q) | Q(email__contains=q) | 
            Q(mobile__contains=q)| Q(website__contains=q))
            # print('mul q ',multiple_q)
            userlist=RegistrationModel.objects.filter(multiple_q)
            # for pagination
            paginator=Paginator(userlist,total_records)
            page_number=request.GET.get('page')
            userlist=paginator.get_page(page_number)
        else:
            userlist = RegistrationModel.objects.order_by('-id')
            # for pagination
            paginator=Paginator(userlist,total_records)
            page_number=request.GET.get('page')
            userlist=paginator.get_page(page_number)
        context = {
            'userlist':userlist,
        }
        return render(request,'userlist.html',context)
    except NoReverseMatch:
        form = IndexForm()
        context ={
                'form':form,
                'message':session_msg,
                'class':'danger'
                }
        return render(request,'login_page.html',context)

def subadmin_list_fun(request):
    # get q name from search box
    if 'q' in request.GET:
        q_search=request.GET['q']
        q = q_search.strip()
            # search in multiple columns
        multiple_q = Q(Q(email__contains=q) | Q(name__contains=q))
            # print('mul q ',multiple_q)
        sub_admin_list=AdminModel.objects.filter(multiple_q)
            # for pagination
        paginator=Paginator(sub_admin_list,total_records)
        page_number=request.GET.get('page')
        sub_admin_list=paginator.get_page(page_number)
    else:
        sub_admin_list = AdminModel.objects.order_by('-id')
        # for pagination
        paginator=Paginator(sub_admin_list,total_records)
        page_number=request.GET.get('page')
        sub_admin_list=paginator.get_page(page_number)
    context = {
        'sub_admin_list':sub_admin_list,
    }
    return render(request,'sub_admin_list.html',context)



@csrf_exempt
def login_page(request):
    if request.method == 'POST':
        form = IndexForm(request.POST)
        try:
            if form.is_valid():
                username_f=form.cleaned_data['username']
                password_f=form.cleaned_data['password']
                # get user id, set session
                id = AdminModel.objects.get(name=username_f).pk
                name = AdminModel.objects.filter(name=username_f).exists()
                passw = AdminModel.objects.filter(password=password_f).exists()
                print('id ',id)
                print('username ',name)
                print('password ',passw)
                if name==True and passw==True:
                    # print('username and password is matched ')
                    request.session['username']=username_f # get value from form
                    request.session['id']=id # get value from database
                    print('session set successfully')
                    return redirect('/')
                elif name!=True and passw==True:
                    context ={
                        'form':form,
                        'message':'invalid username and password',
                        'class':'warning'
                        }
                    return render(request,"login_page.html",context)
                elif name==True and passw!=True:
                    context ={
                        'form':form,
                        'message':'invalid username and password',
                        'class':'warning'
                        }
                    return render(request,"login_page.html",context)
                elif name==False and passw==False:
                    context ={
                        'form':form,
                        'message':'username and password does not exist',
                        'class':'danger'
                        }
                    return render(request,"login_page.html",context)
                elif name==False and passw!=False:
                    context ={
                        'form':form,
                        'message':'username and password does not exist',
                        'class':'danger'
                        }
                    return render(request,"login_page.html",context)            
        except ObjectDoesNotExist as d:
            context ={
                    'form':form,
                    'message':'username and password does not exist',
                    'class':'danger'
                    }
            return render(request,'login_page.html',context)
    else:
        form = IndexForm()        
    return render(request,"login_page.html",{'form':form})

def logout(request):
    print(request.session.get('flag'))
    flag = request.session.get('flag')
    if flag:
        request.session.flush()
        request.session.clear_expired()
        form = IndexForm()    
        context = {
            'form':form,
            'message':'admin logout successfully',
            'class':'success' 
            }  
        # return render(request,'admin_app/myadmin/admin_login.html',context)
        return redirect('admin_home')
    else:
        request.session.flush()
        request.session.clear_expired()
        form = IndexForm()    
        context = {
            'form':form,
            'message':'user logout successfully',
            'class':'success' 
            }  
        return render(request,'login_page.html',context)
    # return redirect('/')

def change_password(request,id):
    try:
        username = request.session.get('username')
        if username == None:
            return redirect('login_page')
        if request.method == 'POST':
            id = AdminModel.objects.get(pk=id)
            print('id AdminForm Post ',id)
            form = AdminForm(request.POST,instance=id)
            form.fields['name'].widget.attrs['readonly'] = True 
            if form.is_valid():
                form.save()
                form = IndexForm()
                context = {
                    'form':form,
                    'message':'password changed successfully',
                    'class':'success' 
                }  
                return render(request,'login_page.html',context)
        else:
            try:
                id = AdminModel.objects.get(pk=id)
                print('id AdminForm Get ',id)
                form = AdminForm(instance=id)
                form.fields['name'].widget.attrs['readonly'] = True 
                form.fields['email'].widget.attrs['readonly'] = True 
                form.fields['otp'].widget.attrs['readonly'] = True 
            except KeyError as k:
                print('key error for name and email ',k)
 
        return render(request,'change_password.html',{'form':form,'username':username,'id':id})
    except NoReverseMatch:
        form = IndexForm()
        context ={
                'form':form,
                'message':session_msg,
                'class':'danger'
                }
        return render(request,'login_page.html',context)