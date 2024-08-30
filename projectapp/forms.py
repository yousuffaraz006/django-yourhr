from django.forms import ModelForm
from .models import *

class ApplicantForm(ModelForm):
    class Meta:
        model = Applicant
        fields = ['full_name', 'phone', 'image', 'resume']