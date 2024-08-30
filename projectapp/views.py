from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from YourHR.settings import DEBUG
from django.contrib import messages
from django.conf import settings
from .decorators import *
from .models import *
from .forms import *
import uuid

@unauthenticated_user
def sendmailUser(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        username = email.split("@")[0]
        user_obj = User.objects.filter(username=username).first()
        if not user_obj:
            auth_token = str(uuid.uuid4())
            profile_obj = EmailVerification.objects.create(user=username, auth_token=auth_token)
            profile_obj.save()
            send_mail_before_signup(email, auth_token)
            messages.info(request, 'Email has been sent to your mail address. Please verify your account to proceed.')
            return redirect('sendmailpage')
        else:
            messages.info(request, 'User already exists.')
            return redirect('sendmailpage')
    return render(request, 'projectapp/sendmailpage.html')

@unauthenticated_user
def signupUser(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        username = email.split("@")[0]
        user_exist = User.objects.filter(username=username).first()
        if user_exist:
            messages.info(request, 'Username has already been taken.')
            return redirect('signuppage')
        elif password1 != password2:
            messages.info(request, 'Passwords did not match.')
            return redirect('signuppage')
        else:
            profile_obj = EmailVerification.objects.filter(user=username).first()
            if profile_obj:
                if profile_obj.is_verified:
                    user_obj = User.objects.create_user(username, first_name=firstname, last_name=lastname, email=email, password=password1)
                    employee_group = Group.objects.get(name='User')
                    user_obj.groups.add(employee_group)
                    applicant_obj = Applicant.objects.create(user=user_obj, full_name=firstname + ' ' + lastname)
                    applicant_obj.save()
                    verifyemail = EmailVerification.objects.filter(user=username).first()
                    verifyemail.delete()
                    applicant = authenticate(username=username, password=password1)
                    login(request, applicant)
                    return redirect('formpage')
                else:
                    auth_token = str(uuid.uuid4())
                    profile_obj.auth_token = auth_token
                    profile_obj.save()
                    email_obj = User.objects.get(username=username).username
                    send_mail_before_signup(email_obj, auth_token)
                    messages.info(request, 'Your account is not verified. Please check your mailbox for "Account Verification" mail and click on the link to verify your account. We have sent a new "Account Verification" mail.')
                    return redirect('signuppage')
            else:
                messages.info(request, 'You need to provide your mail address for account verification before you sign up.')
                return redirect('sendmailpage')
    return render(request, 'projectapp/signuppage.html')

def send_mail_before_signup(email, token):
    if DEBUG:
        link = '127.0.0.1:8000'
    else:
        link = 'https://yourhr.pythonanywhere.com'
    subject = 'Account Verification'
    user = email.split("@")[0]
    message = f'Hi {user}, please click on the link to verify your account on YourHR. {link}/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

def verify(request, auth_token):
    try:
        profile_obj = EmailVerification.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.info(request, 'Your account is already verified.')
                return redirect('signuppage')
            else:
                print(auth_token)
                profile_obj.is_verified = True
                profile_obj.auth_token = ''
                profile_obj.save()
                messages.info(request, 'Your account has been verified.')
                return redirect('signuppage')
        else:
            messages.info(request, 'Encountered some error!')
            return redirect('signuppage')
    except Exception as e:
        messages.info(request, e)
        return render(request, 'projectapp/signuppage.html')

@unauthenticated_user
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.info(request, 'User not found.')
            return redirect('loginpage')
        else:
            applicant = authenticate(username=username, password=password)
            if applicant is None:
                messages.info(request, 'Please enter the credentials correctly.')
                return redirect('loginpage')
            else:
                if username == 'yfara':
                    login(request, applicant)
                    return redirect('homepage')
                else:
                    login(request, applicant)
                    return redirect('formpage')
    else:
        return render(request, 'projectapp/loginpage.html')

@login_required(login_url='loginpage')
def logoutUser(request):
    logout(request)
    return redirect('loginpage')

@login_required(login_url='loginpage')
@admin_only
def home(request):
    usertype = request.user.groups.all()[0].name
    applicants = Applicant.objects.all()
    context = {'applicants':applicants, 'usertype':usertype}
    return render(request, 'projectapp/homepage.html', context)

@login_required(login_url='loginpage')
@allowed_beings(allowed_roles=['User'])
def form(request):
    usertype = request.user.groups.all()[0].name
    applicant = get_object_or_404(Applicant, user=request.user)
    if request.method == 'POST':
        try:
            form = ApplicantForm(request.POST, request.FILES, instance=applicant)
            if form.is_valid:
                form.save()
            messages.info(request, 'All Set')
        except ValueError:
            messages.info(request, 'Error : Bad data passed in. Try again.')
        return redirect('formpage')
    context = {'applicant':applicant, 'usertype':usertype}
    return render(request, 'projectapp/formpage.html', context)