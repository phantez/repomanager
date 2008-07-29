from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from repomanager.accountsform import NewAccountForm, LoginForm

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        # edit profile
        form = ChangeProfileForm(request.POST)
        if form.is_valid():
            form.update_user(user)
            user.save()
            user.message_set.create(message="Profile updated.")
            return HttpResponseRedirect("/accounts/profile/")
    else:
        # display profile
        form = ChangeProfileForm(dict(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email))
    return render_to_response('profile.html', dict(form=form), context_instance=RequestContext(request))

def frontpage(request):
    if request.user.is_authenticated():
        new_account_form = login_form = None
    else:
        post_names = set(n for n,v in request.POST.items() if v)
        if post_names.intersection(('newaccount', 'new-username',
                    'new-password1', 'new-password2')):
            new_account_form = NewAccountForm(request.POST, prefix='new')
            if new_account_form.is_valid():
                user = User.objects.create_user(
                        new_account_form.cleaned_data['username'],
                        '', # email
                        new_account_form.cleaned_data['password1'])
                user.save()
                user = authenticate(
                        username=new_account_form.cleaned_data['username'],
                        password=new_account_form.cleaned_data['password1'])
                login(request, user)
                user.message_set.create(message=
                        "Your account has been created.")
        else:
            new_account_form = NewAccountForm(prefix='new')
        if post_names.intersection(('username', 'password')):
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = login_form.user
                login(request, user)
                user.message_set.create(message="You have been logged in.")
        else:
            login_form = LoginForm()

    return render_to_response('frontpage.html',
        dict(
            new_account_form=new_account_form,
            login_form=login_form,
        ), context_instance=RequestContext(request)
    )

