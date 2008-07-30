from django.db import models
from django.contrib.auth.models import User

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

    def write_hgrc(self):
        pass

