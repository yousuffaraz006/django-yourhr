from django.contrib.auth.models import User
from django.db import models

class EmailVerification(models.Model):
    user = models.CharField(max_length=30)
    auth_token = models.CharField(max_length=100, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user

class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    image = models.ImageField(upload_to='images/', default='static/images/user.jpg', null=True, blank=True)
    resume = models.FileField(upload_to='docs/', null=True, blank=True)

    def __str__(self):
        return str(self.user)