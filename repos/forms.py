from repomanager.repos.models import Repo
from django import forms
from django.contrib.auth.models import User

required_dict = {'class': 'required text short'}

class NewRepositoryForm(forms.Form):

    reponame = forms.CharField(max_length=30,
            widget=forms.TextInput(attrs={'class': 'required title'}),
            label=u"Repository Name", help_text=u"the name used in the url. " +
            u"(Changing this will change the url.)")
    long_name = forms.CharField(max_length=50, required=False,
            label=u"Aesthetic Name",
            widget=forms.TextInput(attrs={'class': 'required text'}),
            help_text=u"optional version of the name fit for human consumption")
    description = forms.CharField(max_length=5000, required=False,
            widget=forms.Textarea())

    def create_repo(self, user):
        """
        Creates a new repository, but doesn't save it.

        This method assumes that self.user is a valid user.
        """
        return user.repo_set.create(
                name=self.cleaned_data['reponame'],
                long_name=self.cleaned_data['long_name'],
                description=self.cleaned_data['description'])

class RepositoryForm(forms.Form):

    reponame = forms.CharField(max_length=30,
            widget=forms.TextInput(attrs={'class': 'required title'}),
            label=u"Repository Name")

class UserForm(forms.Form):

    username = forms.CharField(max_length=30,
            label=u"User Name",
            widget=forms.TextInput(attrs={'class': 'required text'}))



