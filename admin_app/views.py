from django.shortcuts import render,redirect
from .forms import IndexAdminForm
from .models import AdminLoginModel 
from django.core.exceptions import ObjectDoesNotExist
# messages
from django.contrib import messages
# Create your views here.
def admin_index(request):
    if request.method == 'POST':
        form = IndexAdminForm(request.POST)
        try:
            if form.is_valid():
                username_f=form.cleaned_data['username']
                password_f=form.cleaned_data['password']
                # get user id, set session
                id = AdminLoginModel.objects.get(username=username_f).pk
                name = AdminLoginModel.objects.filter(username=username_f).exists()
                passw = AdminLoginModel.objects.filter(password=password_f).exists()
                print('id ',id)
                print('username ',name)
                print('password ',passw)
                if name==True and passw==True:
                    # print('username and password is matched ')
                    flag='admin'
                    request.session['flag']=flag
                    request.session['username']=username_f # get value from form
                    request.session['id']=id # get value from database
                    print('session set successfully')
                    return redirect('/')
                    # return render(request,"myadmin/admin_login.html",{'flag':flag})
                elif name!=True and passw==True:
                    context ={
                        'form':form,
                        'message':'invalid username and password',
                        'class':'warning'
                        }
                    return render(request,"myadmin/admin_login.html",context)
                elif name==True and passw!=True:
                    context ={
                        'form':form,
                        'message':'invalid username and password',
                        'class':'warning'
                        }
                    return render(request,"myadmin/admin_login.html",context)
                elif name==False and passw==False:
                    context ={
                        'form':form,
                        'message':'username and password does not exist',
                        'class':'danger'
                        }
                    return render(request,"myadmin/admin_login.html",context)
                elif name==False and passw!=False:
                    context ={
                        'form':form,
                        'message':'username and password does not exist',
                        'class':'danger'
                        }
                    return render(request,"myadmin/admin_login.html",context)            
        except ObjectDoesNotExist as d:
            context ={
                    'form':form,
                    'message':'username and password does not exist',
                    'class':'danger'
                    }
            return render(request,'myadmin/admin_login.html',context)
    else:
        form = IndexAdminForm()        
    return render(request,"myadmin/admin_login.html",{'form':form})
