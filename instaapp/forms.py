from django import forms
from .models import Image,Profile,Comments
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text = 'Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
class Form(forms.ModelForm):
   
    class Meta:
        model = Image
        exclude = ['likes', 'post_date', 'profile']  
class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget = forms.TextInput()
        self.fields['comment'].widget.attrs['placeholder'] = 'Add a comment...'

    class Meta:
        model = Comments
        exclude = ['image', 'user']             
