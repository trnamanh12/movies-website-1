# path: app/user/views.py
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
# from .models import CustomUser
# from .forms import CustomUserCreationForm, CustomUserChangeForm
import uuid
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import Profile
from .forms import CustomUserChangeForm
import logging

logger = logging.getLogger(__name__)

"""
home : redirect to home at mysites
register: 
user_login
user_logout
view_profile
edit_profile
delete_account
"""

def home(request):
    # redirect to home at mysites
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return render(request, 'base_user.html', {'message': 'Registered successfully, congratulations! Please login.'})
        else:
            return render(request, 'register.html', {'error': 'Invalid information!', 'form': UserCreationForm()})
    else:
        return render(request, "register.html", {'form': UserCreationForm()})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

# @login_required
# def user_logout(request):
#     if request.method == 'POST':
#         logout(request)  # This logs out the user
#         return redirect('login')
#     else:
#         return redirect('home')  # Redirect to home if not a POST request



@login_required
def user_logout(request):
    logger.info(f"Logout request method: {request.method}")
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    else:
        return redirect('home')


@login_required
def view_profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(email=request.user.email, password=password)
        if user is not None:
            user.delete()
            messages.success(request, 'Your account has been deleted.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid password.')
    return render(request, 'delete_account.html')


# def view_balance(request):
#     profile = Profile.objects.get(user=request.user)
#     return render(request, 'user/balance.html', {'profile': profile})

#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = True 
#             user.is_email_verified = True # Assume that user email is verified
#             user.save()
            
#             # Generate verification token
#             token = str(uuid.uuid4())
#             user.email_verification_token = token
#             user.save()
            
#             # Send verification email
#             subject = 'Verify your email'
#             message = f'Please click the link to verify your email: {settings.SITE_URL}/verify-email/{token}'
#             send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            
#             messages.success(request, 'Please check your email to verify your account.')
#             return redirect('login')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'register.html', {'form': form})

# def verify_email(request, token):
#     try:
#         user = CustomUser.objects.get(email_verification_token=token)
#         user.is_active = True
#         user.is_email_verified = True
#         user.email_verification_token = ''
#         user.save()
#         messages.success(request, 'Your email has been verified. You can now log in.')
#     except CustomUser.DoesNotExist:
#         messages.error(request, 'Invalid verification token.')
#     return redirect('login')