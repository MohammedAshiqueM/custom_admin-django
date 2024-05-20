from django.shortcuts import render,redirect
from . form import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


########################## function for login ##############################
@never_cache
def login(request):
    
    #Instantiation of the form class UserRegistrationForm 
    form=UserRegistrationForm()
    context={'form':form}
    
    #For restrict the navigation back to the login page after login
    if request.user.is_authenticated:
        return redirect('home')        
    
    #fetching data if form is submitted
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        
        
        #checking wether the user is exists in User model
        if not User.objects.filter(username=username).exists():
            messages.error(request,f"Username '{username}' does not exist")
            return render(request,'login.html',context)
        
        #authenticating the username and password
        user = authenticate(username=username,password=password)
        if user is None:
            messages.error(request,"Invalid Password")
            return redirect('login')
        else:
            auth_login(request,user)
            return redirect('home')
    return render(request,"login.html",context)

########################## login function ends ###############################


########################## function for home page ############################

@login_required(login_url='login')
@never_cache
def home(request):
    if request.user.is_authenticated:
        return render(request,"home.html")

########################## home page function ends ############################


########################## function for register  #############################

def register(request):
    
    #Instantiation of the form class UserRegistrationForm
    form=UserRegistrationForm()
    context={'form':form}
    
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
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.error(request,f"Mail Id '{email}' already taken")
            return redirect('register')
        elif password1!=password2:
            messages.error(request,"Password is unmaching")
            form = UserRegistrationForm(request.POST, initial={'username': request.POST['username']})
            return render(request,"register.html",{'form':form})
        else:
            
            # Checking the email and password are valid using overrided fucrions clean_email() and clean_password()
            try:
                form.clean_email()
                form.clean_password()
            except Exception as e:
                messages.error(request,e.message)
                form = UserRegistrationForm(request.POST, initial={'username': request.POST['username']})
                return render(request,"register.html",{'form':form})
            
            # Saving the password
            user = User.objects.create_user(username=username,email=email)
            user.set_password(password1)
            user.save()
            messages.success(request,f"New user '{username}' is created")
            return redirect('login')
            
    return render(request,"register.html",context)

##########################  register function ends ###############################


########################## function for logout ############################

def logout(request):
    auth_logout(request)
    return redirect('login')

########################## logout function ends ###############################
