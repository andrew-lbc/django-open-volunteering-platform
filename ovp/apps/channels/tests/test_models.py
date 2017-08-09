from django.test import TestCase
from ovp.apps.channels.models import Channel
from ovp.apps.channels.exceptions import UnexpectedMultipleChannelsError
from ovp.apps.projects.models import Project
from ovp.apps.users.models import User

class MultiChannelTestCase(TestCase):
  def setUp(self):
    self.user = User(email="test@user.com", password="test_password")
    self.user.save()

  def test_migrations_create_default_channel(self):
    self.assertTrue(Channel.objects.count() == 1)
    self.assertTrue(Channel.objects.first().name == "default")

  def test_models_that_extend_multi_channel_relationship_default_channel_on_save(self):
    """ Assert models that extend MultiChannelRelationship model automatically get associated with default channel on save method """
    project = Project(name="test", owner=self.user)
    project.save()

    self.assertTrue(project.channels.all().count() == 1)
    self.assertTrue(project.channels.first().slug == "default")

  def test_models_that_extend_multi_channel_relationship_can_be_created_with_custom_channels_on_save(self):
    """ Assert models that extend MultiChannelRelationship can be created with custom channels on save method """
    Channel(name="Test", slug="test-channel").save()

    project = Project(name="test", owner=self.user)
    project.save(object_channels=["test-channel"])

    self.assertTrue(project.channels.all().count() == 1)
    self.assertTrue(project.channels.first().slug == "test-channel")

    project = Project(name="test", owner=self.user)
    project.save(object_channels=["default", "test-channel"])

    self.assertTrue(project.channels.all().count() == 2)
    self.assertTrue(project.channels.first().slug == "default")
    self.assertTrue(project.channels.last().slug == "test-channel")

  def test_models_that_extend_multi_channel_relationship_default_channel_on_create(self):
    """ Assert models that extend MultiChannelRelationship model automatically get associated with default channel on manager create method """
    project = Project.objects.create(name="test", owner=self.user)

    self.assertTrue(project.channels.all().count() == 1)
    self.assertTrue(project.channels.first().slug == "default")

  def test_models_that_extend_multi_channel_relationship_can_be_created_with_custom_channels_on_create(self):
    """ Assert models that extend MultiChannelRelationship can be created with custom channels on manager create method """
    Channel(name="Test", slug="test-channel").save()

    project = Project.objects.create(name="test", owner=self.user, object_channels=["test-channel"])

    self.assertTrue(project.channels.all().count() == 1)
    self.assertTrue(project.channels.first().slug == "test-channel")

    project = Project.objects.create(name="test", owner=self.user, object_channels=["default", "test-channel"])

    self.assertTrue(project.channels.all().count() == 2)
    self.assertTrue(project.channels.first().slug == "default")
    self.assertTrue(project.channels.last().slug == "test-channel")


class SingleChannelTestCase(TestCase):
  def test_models_that_extend_single_channel_relationship_default_channel_on_save(self):
    """ Assert models that extend SingleChannelRelationship model automatically get associated with default channel on save method """
    user = User(email="test@user.com", password="test_password")
    user.save()

    self.assertTrue(user.channel.slug == "default")

  def test_models_that_extend_single_channel_relationship_can_be_created_with_custom_channel_on_save(self):
    """ Assert models that extend SingleChannelRelationship can be created with custom channel on save method """
    Channel(name="Test", slug="test-channel").save()
    user = User(email="test@user.com", password="test_password")
    user.save(object_channels=["test-channel"])

    self.assertTrue(user.channel.slug == "test-channel")

  def test_models_that_extend_single_channel_relationship_default_channel_on_create(self):
    """ Assert models that extend SingleChannelRelationship model automatically get associated with default channel on manager create method """
    user = User.objects.create(email="test@user.com", password="test_password")
    self.assertTrue(user.channel.slug == "default")

  def test_models_that_extend_single_channel_relationship_can_be_created_with_custom_channel_on_create(self):
    """ Assert models that extend SingleChannelRelationship can be created with custom channel on manager create method """
    Channel(name="Test", slug="test-channel").save()
    user = User.objects.create(email="test@user.com", password="test_password", object_channels=["test-channel"])
    self.assertTrue(user.channel.slug == "test-channel")

  def test_models_that_extend_single_channel_relationship_raise_exception_if_associated_with_multiple_channels(self):
    """ Assert models that extend SingleChannelRelationship raise exception if associated_with_multiple_channels """
    Channel(name="Test", slug="test-channel").save()
    with self.assertRaises(UnexpectedMultipleChannelsError):
      user = User.objects.create(email="test@user.com", password="test_password", object_channels=["default", "test-channel"])

    user = User(email="test@user.com", password="test_password")
    with self.assertRaises(UnexpectedMultipleChannelsError):
      user.save(object_channels=["default", "test-channel"])

  def test_models_that_extend_single_channel_cant_associate_channel_directly(self):
    """ Assert models that extend SingleChannelRelationship raise exception when trying to associate channel directly """
    pass
    # TODO: write testcase
