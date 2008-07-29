from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django import newforms as forms

def frontpage(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/repos/manage/")
    else:
        return HttpResponseRedirect("/accounts/")

@login_required
def manage(request):
    user = request.user
    form = dict(
            new_repository_form=NewRepositoryForm(),
        )
        
    post_names = set(n for n,v in request.POST.items() if v)
    if post_names.intersection(('createrepository', 'name')) :
        # create repository
        return render_to_response('repo_frontpage.html', dict(form=form), context_instance=RequestContext(request))
    elif post_names.intersection(('deleterepository', 'name')) :
        # delete repository
        return render_to_response('repo_frontpage.html', dict(form=form), context_instance=RequestContext(request))
    elif post_names.intersection(('addusertorepository', 'username', 'userpassword')) :
        # add user to repository
        return render_to_response('repo_frontpage.html', dict(form=form), context_instance=RequestContext(request))
    elif post_names.intersection(('deleteusertorepository', 'username')) :
        # delete user from repository
        return render_to_response('repo_frontpage.html', dict(form=form), context_instance=RequestContext(request))
    else :
        # view repository
        return render_to_response('repo_frontpage.html', dict(form=form), context_instance=RequestContext(request))
    # view repository
    return render_to_response('repo_frontpage.html', dict(form=form), context_instance=RequestContext(request))

required_dict = {'class': 'required text short'}

class NewRepositoryForm(forms.Form):
    name = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs=required_dict),
                               label=u'name')
    def clean(self):
        return self.cleaned_data

