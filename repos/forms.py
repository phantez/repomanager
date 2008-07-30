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

def get_users_names():
    users = []
    for n in User.objects.all() :
        users.append((n.username, n.username))
    return users

def get_repos_names():
    repos = []
    for r in Repo.objects.all() :
        repos.append((r.name, r.name))
    return repos

class oldRepositoryForm(forms.Form):
    reponame = forms.MultipleChoiceField([(r.name, r.name) for r in Repo.objects.all()])

class oldUserForm(forms.Form):
    username = forms.MultipleChoiceField([(n.username, n.username) for n in User.objects.all()])

class RepositoryForm(forms.Form):
    reponame = forms.MultipleChoiceField(get_repos_names())

class UserForm(forms.Form):
    username = forms.MultipleChoiceField(get_users_names())




