from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm,UserChangeForm


class LoginForm(forms.Form):
    username = forms.CharField(label='Username',max_length=40)
    password = forms.CharField(label='Password',max_length=40,widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email address', max_length=254, required=True)
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class PasswordReset(PasswordResetForm):
    class Meta:
        model = User
        fields = ['email']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['lastName','firstName','phoneNumber','state','address','Janre','language','gender']

    lastName = forms.CharField(label='성', widget=forms.TextInput(attrs={'class':'form-label','max_length':'40'}), required=False)
    firstName = forms.CharField(label='이름',widget=forms.TextInput(attrs={'class':'form-label','max_length':'20'}), required=False)
    phoneNumber = forms.CharField(label='전화번호',widget=forms.TextInput(attrs={'class':'form-label','max_length':'20'}), required=False)
    state = forms.CharField(label='시',widget=forms.TextInput(attrs={'class':'form-label','max_length':'40'}), required=False)
    address = forms.CharField(label='주소',widget=forms.TextInput(attrs={'class':'form-label','max_length':'200'}), required=False)
    Janre = forms.CharField(label='좋아하는 장르',widget=forms.TextInput(attrs={'class':'form-label','max_length':'200'}), required=False)
    language = forms.ChoiceField(label='언어', widget=forms.Select(attrs={'class': 'select2 form-select'}), choices=[
        ('kr', 'Korea, Republic of'),
        ('en', 'English'),
        ('fr', 'French'),
        ('de', 'German'),
        ('pt', 'Portuguese'),
    ], required=False)
    gender = forms.ChoiceField(label='성별', widget=forms.Select(attrs={'class': 'select2 form-select'}), choices=[
        ('male', '남'),
        ('female', '여'),
    ], required=False)