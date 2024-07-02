from django.urls import reverse
from .forms import SignUpForm 
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError



@ensure_csrf_cookie
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate using your custom user model
        user = authenticate(request, username=username, password=password)
        #print(username)
        #print(password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have logged in successfully!"))
            return redirect(reverse('dashboard'))
        else:
            messages.error(request, ("Invalid username or password."))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out."))
    return redirect('/')

from django.contrib.auth import authenticate, login

@ensure_csrf_cookie
def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)  
        
        if form.is_valid():
            password = form.cleaned_data["password"]
            try:
                validate_password(password, form.instance)
            except ValidationError as e:
                form.add_error('password', e)
                return render(request, 'authenticate/register_user.html', {'form': form})
          
            user = form.save(commit=False)
                       
            user.set_password(password)
            user.save()

            # Log the user in
            login(request, user)

            messages.success(request, "Registration successful!")
            return redirect(reverse('dashboard'))
    else:
        form = SignUpForm()
    return render(request, 'authenticate/register_user.html', {'form': form})

