from django import newforms as forms
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
import re

class ChangeProfileForm(forms.Form):
    # clean data get from post
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)

    def update_user(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

username_re = re.compile(r'^\w+$')

class NewAccountForm(forms.Form):
    username = forms.CharField(max_length=30, label=u'Username',
            widget=forms.TextInput(attrs={'class': 'required text short'}))
    password1 = forms.CharField(label=u'Password',
            widget=forms.PasswordInput(attrs={'class': 'required text short'}))
    password2 = forms.CharField(label=u'Password (again)',
            widget=forms.PasswordInput(attrs={'class': 'required text short'}),
            help_text="What if you made a typo?")
    tos = forms.BooleanField()

    def clean_username(self):
        """
        Validates that the username is alphanumeric and is not already
        in use.
        
        """
        if 'username' in self.cleaned_data:
            if not username_re.search(self.cleaned_data['username']):
                msg = (u'Usernames can only contain letters, ' +
                        u'numbers and underscores')
                raise forms.ValidationError(msg)
            try:
                user = User.objects.get(
                        username__exact=self.cleaned_data['username'])
            except User.DoesNotExist:
                return self.cleaned_data['username']
            raise forms.ValidationError(u'This username is already taken. ' +
                    u'Please choose another.')

    def clean_password2(self):
        """
        Validates that the two password inputs match.
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data and \
           self.cleaned_data['password1'] == self.cleaned_data['password2']:
            return self.cleaned_data['password2']
        raise forms.ValidationError(u'You must type the same password each time')
    
    def clean_tos(self):
        """
        Validates that the user accepted the Terms of Service.
        """
        if self.cleaned_data.get('tos', False):
            return self.cleaned_data['tos']
        raise forms.ValidationError(u'You must agree to the terms to register')

required_dict = {'class': 'required text short'}

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs=required_dict),
                               label=u'Username')
    password = forms.CharField(widget=forms.PasswordInput(attrs=required_dict),
                                label=u'Password')

    def clean(self):
        print self._errors
        if not self._errors:
            self.user = authenticate(username=self.cleaned_data['username'],
                    password=self.cleaned_data['password'])
            if not self.user:
                raise forms.ValidationError(u'Invalid username and password.')
            elif not self.user.is_active:
                raise forms.ValidationError(u'Your account has been disabled.')
            else:
                return self.cleaned_data['username']
        return self.cleaned_data

