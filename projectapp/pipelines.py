from django.contrib.auth.models import Group
from .models import *
import uuid

def create_applicant(backend, user, response, *args, **kwargs):
    employee_group = Group.objects.get(name='User')
    user.groups.add(employee_group)
    if not Applicant.objects.filter(user=user).exists():
        Applicant.objects.create(user=user)
        verifyemail = EmailVerification.objects.filter(user=user.email).first()
        if verifyemail:
            verifyemail.delete()
        else:
            print('Not Found')