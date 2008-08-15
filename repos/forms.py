# -*- coding: utf-8 -*-
#
# This file is part of RepoManager Project
# Copyright (C) 2008 the RepoManager team, see AUTHORS for details
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

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

