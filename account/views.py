import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View


from account.models import User


# Create your views here.


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home:home')
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if request.GET.get('next', None):
                return HttpResponseRedirect(request.GET['next'])
            return redirect('home:home')
        else:
            context = {'email': email}
            messages.error(request, 'Invalid email or password')
            # return redirect('Authentication:loginview',)
            return render(request, 'login.html', context)


# Account Logout views
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('account:login')


class SignupView(View):
    template_name = 'signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home:home')
        return render(request, self.template_name)

    def post(self, request):
        first_name = request.POST.get('first_name').title()
        last_name = request.POST.get('last_name').title()
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        context = {
            'data': request.POST,
            'has_error': False
        }

        while True:
            random_number = random.randint(1000000000, 9999999999)
            if User.objects.filter(unique_id=random_number).exists():
                continue
            else:
                break

        if password != confirmPassword:
            context['msg'] = "password don't match"
            context['color'] = 'alert-danger'
            context['has_error'] = True

        # if password < 8:
        #     context['msg'] = 'password must be 8 digit or more'

        if User.objects.filter(email=email).exists():
            context['msg'] = "Email address already exists"
            context['color'] = 'alert-danger'
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'signup.html', context)

        user = User.objects.create_user(email=email)
        user.set_password(password)
        user.is_active = True
        user.first_name = first_name
        user.last_name = last_name
        user.address = address
        user.phone_number = phone
        user.unique_id = random_number
        user.save()

        return render(request, 'login.html')








