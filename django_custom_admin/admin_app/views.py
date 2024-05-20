from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from user_app.form import UserRegistrationForm
from .form import UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponseForbidden
from django.db.models import Q
########################### admin login #########################################################
@never_cache
def adminLogin(request):
    form = UserRegistrationForm()
    context = {'form':form}
    if request.user.is_authenticated:
        return redirect('adminPage')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        if not User.objects.filter(username=username).exists():
            messages.error(request,'Account not found')
            return redirect('adminLogin')
        user = authenticate(username = username,password = password)
        if user is None:
            messages.error(request,"Invalid username or password")
            return redirect('adminLogin')
        elif user and user.is_superuser:
            login(request,user)
            return redirect('adminPage')
        else:
            messages.error(request,f"{user} have no access to this page")
            return redirect('adminLogin')
    return render(request,'adminLogin.html',context)

########################### admin login end #########################################################

########################### admin page ##############################################################
@login_required(login_url='adminLogin')
@never_cache
def adminPage(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have access to this page.")
    if 'value' in request.GET:
        credential = request.GET['value']
        data = User.objects.filter(Q(username__icontains=credential) | Q(email__icontains=credential))
        context = {'data':data}
    else:
        data = User.objects.all()
        context = {'data':data}
        
    return render(request,'adminPage.html',context)

########################### admin page end #########################################################

########################### edit user ##############################################################
@login_required(login_url='adminLogin')
@never_cache
def editUser(request,pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have access to this page.")
    user = User.objects.get(pk=pk)
    form = UserUpdateForm(instance = user)
    if request.POST:
        form=UserUpdateForm(request.POST,instance = user)
        if form.is_valid():
            form.save()
            return redirect('adminPage')
        else:
            messages.error(request,"User name or email in invalid format")
    context = {'form':form}
    
    return render(request,'editUser.html',context)

########################### edit user end #########################################################

########################### delete user ###########################################################
@login_required(login_url='adminLogin')
@never_cache
def deleteUser(request,pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have access to this page.")
    user = User.objects.get(pk=pk)
    user.delete()
    return redirect('adminPage')

########################### delete user ###########################################################

########################### user creation #########################################################

@login_required(login_url='adminLogin')
@never_cache
def userCreation(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have access to this page.")
    form = UserRegistrationForm()
    context = {'form':form}
    
    #fetching data if the form were submitted
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        
        
        # Checking the credentials are unique     
        if User.objects.filter(username=username).exists():
            messages.error(request,f"User name '{username}' was already taken")
            return redirect('userCreation')
        elif User.objects.filter(email=email).exists():
            messages.error(request,f"Mail Id '{email}' already taken")
            return redirect('userCreation')
        elif password1!=password2:
            messages.error(request,"Password is unmaching")
            form = UserRegistrationForm(request.POST, initial={'username': request.POST['username']})
            return render(request,"userCreation.html",{'form':form})
        else:
            
            # Checking the email and password are valid using overrided fucrions clean_email() and clean_password()
            try:
                form.clean_email()
                form.clean_password()
            except Exception as e:
                messages.error(request,e.message)
                form = UserRegistrationForm(request.POST, initial={'username': request.POST['username']})
                return render(request,"userCreation.html",{'form':form})
            
            # Saving the password
            user = User.objects.create_user(username=username,email=email)
            user.set_password(password1)
            user.save()
            messages.success(request,f"New user '{username}' is created")
            return redirect('adminPage')
    return render(request,'userCreation.html',context)

########################### user creation end #####################################################


def adminLogout(request):
    logout(request)
    return redirect('login')