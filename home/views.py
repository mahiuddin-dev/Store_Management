from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, DeleteView

from account.models import User


class IndexView(TemplateView):
    template_name = 'index.html'

class Deshborad(TemplateView):
    template_name = 'deshboard.html'


class StaffView(LoginRequiredMixin, View):

    def get(self, request):
        staff_user = Group.objects.get(name='staff user').user_set.all()

        return render(request, 'staff.html', {'staff_user': staff_user})

    def post(self, request):
        if request.method == 'POST' and 'add_staff' in request.POST:
            first_name = request.POST.get('first_name').title()
            last_name = request.POST.get('last_name').title()
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirmPassword = request.POST.get('confirm_password')
            address = request.POST.get('address')
            phone = request.POST.get('phone')

            context = {
                'data': request.POST,
                'has_error': False
            }

            if password != confirmPassword:
                context['msg'] = "password don't match"
                context['color'] = 'alert-danger'
                context['has_error'] = True

            if User.objects.filter(email=email).exists():
                context['msg'] = "Email address already exists"
                context['color'] = 'alert-danger'
                context['has_error'] = True

            if context['has_error']:
                return render(request, 'staff.html', context)

            user = User.objects.create_user(email=email)
            user.set_password(password)
            user.is_active = True
            user.first_name = first_name
            user.last_name = last_name
            user.address = address
            user.phone_number = phone
            user.save()
            group, created = Group.objects.get_or_create(name='staff user')
            user.groups.add(group)

        return render(request, 'staff.html')




