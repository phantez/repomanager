from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django import newforms as forms

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

class ChangeProfileForm(forms.Form):
    # clean data get from post
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)

    def update_user(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']


