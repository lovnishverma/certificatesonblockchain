from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StudentMaster, CourseMaster
from .models import CertificatesMaster

class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentMaster
        fields = '__all__'

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username', 'password1', 'password2']

class CourseForm(forms.ModelForm):
    class Meta:
        model = CourseMaster
        fields = '__all__'

class CertificatesMasterAdminForm(forms.ModelForm):
    class Meta:
        model = CertificatesMaster
        fields =  fields = ['student', 'certificate_name', 'certificate', 'email_sent']