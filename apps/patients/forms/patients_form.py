from django.forms import ModelForm
from patients.models import *

class PatientForm(ModelForm):
    class Meta:
        model = Patient