from django.db import models
from ovp.apps.channels.models.abstract import ChannelRelationship

class FavoriteProject(ChannelRelationship):
  project = models.ForeignKey('projects.Project')
  user = models.ForeignKey('users.User')
