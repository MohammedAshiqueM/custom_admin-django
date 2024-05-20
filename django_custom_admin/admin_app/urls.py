from django.urls import path
from . import views

urlpatterns = [
    path('',views.adminLogin,name='adminLogin'),
    path('adminPage',views.adminPage,name='adminPage'),
    path('editUser/<pk>',views.editUser,name='editUser'),
    path('deleteUser/<pk>',views.deleteUser,name='deleteUser'),
    path('userCreation',views.userCreation,name='userCreation'),
    path('adminLogout',views.adminLogout,name='adminLogout'),
    
]