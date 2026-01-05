
from django.conf import settings
from django.contrib import admin
from django.urls import path
from app import views as appViews
from admin_app import views as myAdmin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',appViews.registration,name='registration'),
    path('login_page/',appViews.login_page,name='login_page'),
    path('homepage/',appViews.homepage,name='homepage'),
    path('userlist/',appViews.userlist_fun,name='userlist'),
    path('forgot/',appViews.forgot_password,name='forgot'),
    path('forgotsuccess/',appViews.forgot_success,name='forgotsuccess'),
    path(r'delete/<int:id>/',appViews.delete_record,name='delete_record'),
    path(r'update/<int:id>/<int:empid>/',appViews.update_record,name='update_record'),
    path(r'profile_update/<int:id>/',appViews.profile_update,name='profile_update'),
    path(r'change_password/<int:id>/',appViews.change_password,name='change_password'),
    path('logout/',appViews.logout,name='logout'),
    path('camera_fun/',appViews.camera_fun,name='camera_fun'),
    #admin work
    path('myadmin/index/',myAdmin.admin_index,name='admin_home'),
    path('sub_admin_list/',appViews.subadmin_list_fun,name='sub_admin_list'),
    path(r'delete_subadmin/<int:id>/',appViews.delete_subadmin,name='delete_subadmin'),
    path(r'update_subadmin/<int:id>/',appViews.update_subadmin,name='update_subadmin'),
    path('add_subadmin/',appViews.add_subadmin,name='add_subadmin'),
    path('admin_dashboard/',appViews.admin_dashboard,name='admin_dashboard'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns + staticfiles_urlpatterns() 
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
