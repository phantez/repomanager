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


import sha, os
from base64 import b64encode
from django.contrib.auth.models import User
from django.conf import settings

class Htpasswd(object):
    def __init__(self, filename, mode="r"):
        self.mode = mode
        self.records = {}
        self.changed_keys = set()
        self.filename = filename
        if mode != 'c' or os.path.exists(filename):
            file = open(filename, "r")
            for line in file:
                try:
                    k, v = line.strip().split(':',1)
                except ValueError:
                    continue
                self.records[k] = v
            file.close()

    def __getitem__(self, k):
        return self.records[k]

    def __setitem__(self, k, v):
        if self.mode == "r":
            raise ValueError("Htpasswd file opened for reading only.")
        self.changed_keys.add(str(k))
        self.records[str(k)] = str(v)

    def close(self):
        if not self.changed_keys: return
        f = open(self.filename, 'w')
        f.writelines("%s:{SHA}%s\n" % i for i in self.records.iteritems())
        f.close()

def update_password(username, raw_password):
    db = Htpasswd(settings.HTPASSWD_FILE, "c")
    db[str(username)] = b64encode(sha.new(raw_password).digest())
    db.close()

def oveload_set_password():
    django_set_password = User.set_password
    def set_password(self, raw_password):
        update_password(self.username, raw_password)
        django_set_password(self, raw_password)
    User.set_password = set_password

