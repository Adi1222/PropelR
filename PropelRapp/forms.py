from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm

class ClusterForm(forms.ModelForm):
    class Meta:
        model = Cluster
        fields = ['cluster_name', 'description']


class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = ['camname','x1_cord', 'x2_cord', 'y1_cord', 'y2_cord', 'algo_type']


class AlgoithmForm(forms.ModelForm):
    class Meta:
        model = Algo_master
        fields = ['algo', 'algo_desc']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Cust_org
        fields = ['cust_org', 'cust_org_acro', 'status', 'bill_plan']


class BillPlanForm(forms.ModelForm):
    class Meta:
        model = Bill_plan
        fields = ['billplan', 'billplan_cd']


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['menu']


class SubMenuForm(forms.ModelForm):
    class Meta:
        model = Submenu
        fields = ['menu', 'submenu']



class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role', 'role_desc']


class RoleDetailForm(forms.ModelForm):
    class Meta:
        model = Roledetail
        fields = ['role', 'menu', 'submenu']


class UserForm1(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')

class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    password2 = forms.CharField(widget=forms.PasswordInput(),help_text='Enter the same password as before, for verification', label='Confirm')

    def clean_username(self):
        username = self.cleaned_data['username'].upper()
        r = User.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  forms.ValidationError("Email already exists")
        return email



    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')


class SuperAdminUserForm(forms.ModelForm):
    class Meta:
        model = Appuser
        fields = ('mobile', 'customer', 'role')


class OtherUserForm(forms.ModelForm):
    class Meta:
        model = Appuser
        fields = ('mobile', 'role')


class ProfileForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model = Appuser
        fields = ('username', 'first_name', 'last_name')


class ProfileForm1(forms.ModelForm):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+91'. Up to 15 digits allowed.")
    mobile = forms.CharField(max_length=12,validators=[phone_regex],widget=forms.TextInput(attrs={'class':'form-control'}))
    #profile_pic = forms.FileField()

    class Meta:
        model = Appuser
        fields = ('mobile','profile_pic')


class PasswordChangeCustomForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirm Password')
