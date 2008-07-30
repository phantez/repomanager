from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import escape, linebreaks, urlize


from mercurial import hg, ui
import os

class RepoManager(models.Manager):

    def update_all_disk_usage(self):
        for repo in self.all():
            repo.update_disk_usage()
            repo.save()

    def update_all_hgrc(self):
        for repo in self.all():
            repo.write_hgrc()

class Repo(models.Model) :

    name = models.CharField(max_length=30,unique=True)

    long_name = models.CharField(max_length=50, blank=True)

    description = models.TextField(max_length=5000, blank=True)

    owner = models.ForeignKey(User)

    admin = models.ManyToManyField(User, related_name="admin", blank=True)

    allow_push = models.ManyToManyField(User, related_name="allow_push", blank=True)

    allow_pull = models.ManyToManyField(User, related_name="allow_pull", blank=True)

    creation_date = models.DateTimeField(auto_now_add=True)

    disk_usage = models.IntegerField(blank=True, null=True)

    vcstype = models.CharField(max_length=30, null=True)

    objects = RepoManager()

    def update_disk_usage(self):
        pass

    @property
    def file_path(self):
        return settings.HG_REPOS_PATH+'/'+self.name

    def write_hgrc(self):
        assert(os.path.exists(self.file_path+"/.hg"))
        f = open(self.file_path+"/.hg/hgrc", 'w')
        allow_push = [n.username for n in self.allow_push.all()]
        allow_push.append(self.owner.username)
        c = dict({
            'push_ssl' : 'false',
            'name' : self.name,
            'allow_push' : ", ".join(allow_push),
            'contact' : (self.owner.get_full_name() or escape(self.owner.username)),
            'description' : escape(self.description)
            })
        f.write(render_to_string('hgrc',c))

    def update(self):
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
            hg.repository(ui.ui(), self.file_path, create=True)
        self.write_hgrc()
        return True

    def delete_repo(self):
        if os.path.exists(self.file_path):
            top = self.file_path
            for root, dirs, files in os.walk(top, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.file_path)
        return True

