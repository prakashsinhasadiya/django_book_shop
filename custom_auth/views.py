# -*- coding: utf-8 -*-

from django.views import View
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.http import Http404
from .forms import LoginForm, SignupForm, ResetPasswordForm, ConfirmPasswordForm, ProfileForm

from django.core.files.storage import FileSystemStorage
from .models import UserProfile,BookDetail
import uuid
from datetime import datetime
import pytz


# Get redirect url from settings file or else redirect to admin page.
profile_redirect_url = settings.PROFILE_REDIRECT_URL or '/admin'
login_redirect_url = settings.LOGIN_URL or ''


class Login(View):

    def get(self, request):
        """
        Return login template
        """
        if request.user.is_authenticated:
            return redirect(profile_redirect_url)
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        """
        Login user and redirect to Profile
        """
        form = LoginForm()
        login_form = LoginForm(request.POST)
        if not login_form.is_valid():
            return render(request, 'registration/login.html', {'errors': login_form.errors, 'form': form})
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            error = {'general_error': "user don't match"}
            return render(request, 'registration/login.html', {'errors': error, 'form': form})

        if user.check_password(password):
            login(request, user)
            return redirect(profile_redirect_url)
        error = {'general_error': "Passwords don't match"}
        return render(request, 'registration/login.html', {'errors': error, 'form': form})


class Signup(View):

    def get(self, request):
        """
        Return signup template
        """
        if request.user.is_authenticated:
            return redirect(login_redirect_url)
        form = SignupForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        """
        Signup and redirect to Profile
        """
        # form = SignupForm()
        signup_form = SignupForm(request.POST)
        if not signup_form.is_valid():
            return render(request, 'registration/signup.html', {'errors': signup_form.errors, 'form': signup_form})
        first_name = signup_form.cleaned_data.get('first_name')
        last_name = signup_form.cleaned_data.get('last_name')
        username = signup_form.cleaned_data.get('username')
        email = signup_form.cleaned_data.get('email')
        password_1 = signup_form.cleaned_data.get('password_1')
        password_2 = signup_form.cleaned_data.get('password_2')
        mobile = signup_form.cleaned_data.get('mobile')
        gender = signup_form.cleaned_data.get('gender')
        try:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password_1)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.mobile = mobile
                user.gender = gender
                user.save()
                user_profile, user_profile_create = UserProfile.objects.get_or_create(
                    user=user)
                user_profile.mobile = mobile
                # user_profile.gender = gender
                user_profile.email = email
                user_profile.first_name = first_name
                user_profile.last_name = last_name
                user_profile.save()
                login(request, user)
                return redirect(login_redirect_url)
            else:
                error = {'general_error': 'User already registered.'}
                return render(request, 'registration/signup.html', {'errors': error, 'form': signup_form})
        except Exception:
            error = {'general_error': 'Cannot create user at the moment..'}
            return render(request, 'registration/signup.html', {'errors': error, 'form': signup_form})


class Profile(View):

    def get(self, request):
        """
        Return Profile template
        """
        if not request.user.is_authenticated:
            return redirect(login_redirect_url)
        return render(request, 'registration/profile.html')


class ResetPassword(View):

    def get(self, request):
        form = ResetPasswordForm()
        return render(request, 'registration/reset_password.html', {'form': form})

    def post(self, request):

        reset_password_form = ResetPasswordForm(request.POST)
        if not reset_password_form.is_valid():
            return render(request, 'registration/reset_password.html', {'form': reset_password_form, 'errors': reset_password_form.errors})
        username = reset_password_form.cleaned_data.get('username')
        user = User.objects.filter(username=username)
        if not user:
            return render(request, 'registration/reset_password.html', {'form': reset_password_form, 'errors': {'general_error': 'User doesnot exist.'}})
        token_obj = PasswordResetTokens.objects.create(
            user=user[0], token=uuid.uuid4().hex)
        url = ''
        url += request.get_host()
        url += '/set_password'
        url += '?token=' + token_obj.token
        # data = {'token' : token_obj.token}
        message = render_to_string('registration/reset_password_email_template.html', {
            'user': user[0],
            'url': url,
        })
        res = send_mail('Password Reset', message,
                        settings.FROM_EMAIL, [user[0].email])
        return render(request, 'registration/reset_email_sent.html')


class ChangePassword(View):

    def get(self, request):
        """
        Check if authorized to reset password.
        Return reset password template
        """
        form = ConfirmPasswordForm()
        token = request.GET.get('token')
        if not token:
            raise Http404('Page not found.')
        token_obj = PasswordResetTokens.objects.filter(token=token)
        if not token_obj:
            raise Http404('Fake token supplied.')
        # tz = pytz.timezone("UTC")
        # if tz.localize(datetime.now(), is_dst=None) > token_obj[0].expired_time:
        #     raise Http404('Token Expired. Try again')
        return render(request, 'registration/set_password.html', {'form': form, 'token': token})

    def post(self, request):
        """
        Save new password and redirect to Login
        """
        form = ConfirmPasswordForm(request.POST)
        token = request.GET.get('token')
        if not token:
            raise Http404('Tocken not found.')
        if not form.is_valid():
            return render(request, 'registration/set_password.html', {'form': form, 'token': token, 'errors': form.errors})
        token_obj = PasswordResetTokens.objects.filter(token=token)
        if not token_obj:
            raise Http404('Fake token supplied.')
        password_1 = form.cleaned_data.get('password_1')
        user = token_obj[0].user
        user.set_password(password_1)
        user.save()
        token_obj[0].delete()
        return HttpResponseRedirect(reverse('login'))


class UpdateProfile(View):

    def get(self, request):
        import pdb
        pdb.set_trace()
        if not request.user.is_authenticated:
            return redirect(login_redirect_url)
        form = ProfileForm()
        profile_form = ProfileForm(request.POST or None, initial={
                                   'mobile': request.user.userprofile.mobile, 'first_name': request.user.userprofile.first_name, 'last_name': request.user.userprofile.last_name, 'email': request.user.userprofile.email})
        return render(request, 'registration/update_profile.html', {'form': profile_form})

    def post(self, request):

        profile_form = ProfileForm(request.POST, request.FILES)
        if not profile_form.is_valid():
            return render(request, 'registration/update_profile.html', {'errors': profile_form.errors, 'form': profile_form})
        mobile = profile_form.cleaned_data.get('mobile')
        first_name = profile_form.cleaned_data.get('first_name')
        last_name = profile_form.cleaned_data.get('last_name')
        email = profile_form.cleaned_data.get('email')
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        profile_image = profile_form.cleaned_data.get('profile_image')
        # gender = profile_form.cleaned_data.get('gender')
        user_update_profile, user_update_profile_create = UserProfile.objects.get_or_create(
            user=request.user)
        user_update_profile.mobile = mobile
        user_update_profile.first_name = first_name
        user_update_profile.last_name = last_name
        user_update_profile.email = email
        user_update_profile.profile_image = filename
        user_update_profile.save()
        import pdb; pdb.set_trace()
        user_profile_url = request.user.userprofile.profile_image.url
        return render(request, 'registration/simple_upload.html', {
            'uploaded_file_url': user_profile_url
        })

class BookShop(View):

    def get(self,request):
        objects = BookDetail.objects.filter()
        import pdb; pdb.set_trace()
        return render(request, 'registration/book_shop.html', {
            'objects': objects
        })

def logoutuser(request):
    logout(request)
    return redirect(login_redirect_url)


class BookDetails(View):

    def get(self,request,slug):
        import pdb; pdb.set_trace()