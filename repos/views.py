from repomanager.repos.models import Repo
from repomanager.repos.forms import NewRepositoryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django import forms


def frontpage(request):
    if request.user.is_authenticated():
        return render_to_response('repo_frontpage.html', dict(), context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/accounts/")

@login_required
def create(request):
    user = request.user
    post_names = set(n for n,v in request.POST.items() if v)
    if post_names.intersection(('createrepository', 'reponame')) :
        # create repository
        repo_form = NewRepositoryForm(request.POST)
        repo_form.is_valid()
        if repo_form.clean() :
            repo = repo_form.create_repo(user) # FIXME : handle sql 
            repo.save()
            return HttpResponseRedirect("/repos/")
        return render_to_response('repo_create.html', dict(repo_form=repo_form), context_instance=RequestContext(request))
    else :
        # view repository
        repo_form=NewRepositoryForm()
        return render_to_response('repo_create.html', dict(repo_form=repo_form), context_instance=RequestContext(request))

@login_required
def delete(request):

    class RepositoryForm(forms.Form):
        reponame = forms.MultipleChoiceField([(r.name, r.name) for r in Repo.objects.all()])

    user = request.user
    post_names = set(n for n,v in request.POST.items() if v)
    if post_names.intersection(('createrepository', 'reponame')) :
        # create repository
        repo_form = RepositoryForm(request.POST)
        if repo_form.is_valid() :
            reponame=repo_form.cleaned_data['reponame']
            repo = Repo.objects.get(name=reponame[0]) # FIXME : handle sql 
            repo.delete()
            return HttpResponseRedirect("/repos/")
        return render_to_response('repo_delete.html', dict(repo_form=repo_form), context_instance=RequestContext(request))
    else :
        # view repository
        repo_form = RepositoryForm(request.POST)
        return render_to_response('repo_delete.html', dict(repo_form=repo_form), context_instance=RequestContext(request))

@login_required
def adduser(request):

    class RepositoryForm(forms.Form):
        reponame = forms.MultipleChoiceField([(r.name, r.name) for r in Repo.objects.all()])

    class UserForm(forms.Form):
        username = forms.MultipleChoiceField([(n.username, n.username) for n in User.objects.all()])

    user = request.user
    post_names = set(n for n,v in request.POST.items() if v)
    if post_names.intersection(('adduser', 'reponame', 'username')) :
        # add user to repository
        user_form = UserForm(request.POST)
        repo_form = RepositoryForm(request.POST)
        if user_form.is_valid() and repo_form.is_valid() :
            username=user_form.cleaned_data['username']
            reponame=repo_form.cleaned_data['reponame']
            user_to_add = User.objects.get(username=username[0]) # FIXME : handle sql 
            repo = Repo.objects.get(name=reponame[0]) # FIXME : handle sql 
            repo.allow_push.add(user_to_add) # FIXME : handle sql 
            repo.save()
            return HttpResponseRedirect("/repos/")
        return render_to_response('repo_add_user.html', dict(user_form=user_form, repo_form=repo_form), context_instance=RequestContext(request))
    else :
        # view repository
        user_form = UserForm(request.POST)
        repo_form = RepositoryForm(request.POST)
        return render_to_response('repo_add_user.html', dict(user_form=user_form, repo_form=repo_form), context_instance=RequestContext(request))

@login_required
def deluser(request):

    class RepositoryForm(forms.Form):
        reponame = forms.MultipleChoiceField([(r.name, r.name) for r in Repo.objects.all()])

    class UserForm(forms.Form):
        username = forms.MultipleChoiceField([(n.username, n.username) for n in User.objects.all()])

    user = request.user
    post_names = set(n for n,v in request.POST.items() if v)
    if post_names.intersection(('deluser', 'reponame', 'username')) :
        # delete repository
        user_form = UserForm(request.POST)
        repo_form = RepositoryForm(request.POST)
        if user_form.is_valid() and repo_form.is_valid() :
            username=user_form.cleaned_data['username']
            reponame=repo_form.cleaned_data['reponame']
            user_to_remove = User.objects.get(username=username[0]) # FIXME : handle sql 
            repo = Repo.objects.get(name=reponame[0]) # FIXME : handle sql 
            repo.allow_push.remove(user_to_remove) # FIXME : handle sql 
            repo.save()
            return HttpResponseRedirect("/repos/")
        return render_to_response('repo_del_user.html', dict(user_form=user_form, repo_form=repo_form), context_instance=RequestContext(request))
    else :
        # view repository
        user_form = UserForm(request.POST)
        repo_form = RepositoryForm(request.POST)
        return render_to_response('repo_del_user.html', dict(user_form=user_form, repo_form=repo_form), context_instance=RequestContext(request))

