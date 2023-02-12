from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.safestring import mark_safe



from .forms import UserRegisterForm
from .decorators import user_not_authenticated
from .tokens import account_activation_token


@user_not_authenticated
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('home')
        else:
            messages.error(request, mark_safe('<b>Invalid</b> credentials.<br>Please make sure you entered <b>valid</b> information.'))
    form = UserRegisterForm()
    return render(request, 'register.html', {'register_form': form})


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('template-activate-account.html',
    {
        'user': user.first_name,
        'domain': get_current_site(request).domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to={to_email})
    if email.send():
        messages.success(request, mark_safe(f'Please go to your email <b>{to_email}</b> inbox and click on \
        the activation link to complete registration.<br><b>Note:</b> Check your spam folder.'))
    else:
        messages.error(request, mark_safe(f'There was a problem sending an email to <b>{to_email}</b>.Make sure you typed it <b>correctly!</b>'))


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, mark_safe(f'Your account was <b>activated succesfully!</b> Now you can login.'))
        return redirect('login')
    else:
        messages.error(request, mark_safe('Activation link <b>invalid</b> or <b>expired</b>.'))
    return redirect('home')


@user_not_authenticated
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are logged in as { request.user.first_name }')
                return redirect('home')
        else:
            messages.error(request, f'Invalid username or password')
    form = AuthenticationForm()
    return render(request, 'login.html', {'login_form': form})


@login_required
def change_password_view(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed succesfully! Please login again.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid password')
    form = PasswordChangeForm(user)
    return render(request, 'change-password.html', {'form':form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def not_found_view(request, exception):
    return render(request, 'templates/404.html')


@user_not_authenticated
def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            user = get_user_model().objects.filter(Q(email=user_email)).first()
            if user:
                mail_subject = 'Password Reset request'
                message = render_to_string('template-reset-password.html',
                {
                    'user': user.first_name,
                    'domain': get_current_site(request).domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                    'protocol': 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(mail_subject, message, to=[user.email])
                if email.send():
                    messages.success(request,
                    mark_safe(
                    f"""
                    <h4> Password reset sent</h4><hr>
                    <p>
                    We have emailed you instructions for <b>reseting your password</b>.                   
                    """))
                else:
                    messages.error(request, 'There was a problem sending the reset password email.')
            else:
                messages.error(request, 'The email provided does not match an active user.')
    form = PasswordResetForm()
    return render(request, 'reset-password.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, mark_safe(f'Your password was <b>succesfully reset!</b> Now you can login.'))
                return redirect('home')
            else:
                messages.error(request, mark_safe('<b>Invalid</b> data.Make sure you typed it <b>correctly</b>.'))
        form = SetPasswordForm(user)
        return render(request, 'change-password.html', {'form':form})
    else:
        messages.error(request, mark_safe('Reset password link <b>invalid</b> or <b>expired</b>.'))
    
    messages.error(request, 'Something went wrong, redirecting back to homepage')
    return redirect('home')