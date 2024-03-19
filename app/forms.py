# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
 
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Enter your email'}))
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your firstname'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your lastname'}))
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Enter your password'}))
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Enter your password confirmation'}))
    class Meta:
        model = User
        fields = ['username','email', 'first_name','last_name','password1','password2']

# myproject/accounts/forms.py

from django import forms
from .models import File

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['title', 'content']
        
class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(label='Your Message', widget=forms.Textarea)

from .models import UploadedPDF

class UploadPDFForm(forms.ModelForm):
    class Meta:
        model = UploadedPDF
        fields = ['title', 'pdf_file']

from django import forms
from .models import UploadedImage

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['name', 'image_file', 'public_url']

