from django.test import TestCase
from django.core.management import call_command

from ovp.apps.users.models import User
from ovp.apps.users.models.profile import get_profile_model
from ovp.apps.projects.models import Project, Job, Work
from ovp.apps.organizations.models import Organization
from ovp.apps.core.models import GoogleAddress, Cause, Skill
from ovp.apps.search.helpers import whoosh_raw

from haystack.query import SearchQuerySet

class DisponibilityTestCase(TestCase):
  def setUp(self):
    call_command('clear_index', '--noinput', verbosity=0)

    self.user = User.objects.create_user(email="testmail@test.com", password="test_returned", object_channel="default")

    self.address1 = GoogleAddress(typed_address="São paulo, SP - Brazil")
    self.address1.save(object_channel="default")

    self.address2 = GoogleAddress(typed_address="São paulo, SP - Brazil")
    self.address2.save(object_channel="default")


  def test_disponibility_save_and_deletion_updates_index(self):
    """
    Test creating and deleting Job or Work updates Project index
    """
    self.assertTrue(SearchQuerySet().models(Project).all().count() == 0)

    project = Project.objects.create(name="test project", slug="test-slug", details="abc", description="abc", owner=self.user, address=self.address1, published=True, object_channel="default")

    project2 = Project.objects.create(name="test project", slug="test-slug", details="abc", description="abc", owner=self.user, address=self.address2, published=True, object_channel="default")

    job = Job(can_be_done_remotely=True, project=project)
    job.save(object_channel="default")

    work = Work(can_be_done_remotely=True, project=project2)
    work.save(object_channel="default")

    self.assertTrue(SearchQuerySet().models(Project).all().count() == 2)
    self.assertTrue(SearchQuerySet().models(Project).filter(can_be_done_remotely=True).count() == 2)

    job.delete()
    work.delete()

    self.assertTrue(SearchQuerySet().models(Project).all().count() == 0)
    self.assertTrue(SearchQuerySet().models(Project).filter(can_be_done_remotely=True).count() == 0)

class AddressTestCase(TestCase):
  """
    RealTimeSignalProcessor handles updates to a index tied to a model

    We need to be able to detect changes to a model a rebuild another index,
    such as detecting changes to GoogleAddress and updating the index
    for projects and organizations.

    This is what this class tests.

  """
  def setUp(self):
    call_command('clear_index', '--noinput', verbosity=0)

    self.user = User.objects.create_user(email="testmail@test.com", password="test_returned", object_channel="default")

    self.address1 = GoogleAddress(typed_address="São paulo, SP - Brazil")
    self.address1.save(object_channel="default")

  def test_project_index_on_address_update(self):
    """ Test project index gets reindexed if address changes """
    self.assertTrue(SearchQuerySet().models(Project).all().count() == 0)

    project = Project.objects.create(name="test project", slug="test-slug", details="abc", description="abc", owner=self.user, address=self.address1, published=True, object_channel="default")

    self.assertTrue(SearchQuerySet().models(Project).all().count() == 1)
    self.assertTrue(SearchQuerySet().models(Project).filter(address_components__exact=whoosh_raw("São Paulo-administrative_area_level_2")).count() == 1)

    project.address.typed_address = "Campinas, SP - Brazil"
    project.address.save()

    self.assertTrue(SearchQuerySet().models(Project).all().count() == 1)
    self.assertTrue(SearchQuerySet().models(Project).filter(address_components__exact=whoosh_raw("Campinas-administrative_area_level_2")).count() == 1)

    project.address.delete()
    self.assertTrue(SearchQuerySet().models(Project).all().count() == 0)
    self.assertTrue(SearchQuerySet().models(Project).filter(address_components__exact=whoosh_raw("Campinas-administrative_area_level_2")).count() == 0)


  def test_organization_index_on_address_update(self):
    """ Test organization index gets reindexed if address changes """
    self.assertTrue(SearchQuerySet().models(Organization).all().count() == 0)


    organization = Organization(name="test organization", details="abc", owner=self.user, address=self.address1, published=True, type=0)
    organization.save(object_channel="default")

    self.assertTrue(SearchQuerySet().models(Organization).all().count() == 1)
    self.assertTrue(SearchQuerySet().models(Organization).filter(address_components__exact=whoosh_raw("São Paulo-administrative_area_level_2")).count() == 1)

    organization.address.typed_address = "Campinas, SP - Brazil"
    organization.address.save()

    self.assertTrue(SearchQuerySet().models(Organization).all().count() == 1)
    self.assertTrue(SearchQuerySet().models(Organization).filter(address_components__exact=whoosh_raw("Campinas-administrative_area_level_2")).count() == 1)

    organization.address.delete()
    self.assertTrue(SearchQuerySet().models(Organization).all().count() == 0)
    self.assertTrue(SearchQuerySet().models(Organization).filter(address_components__exact=whoosh_raw("Campinas-administrative_area_level_2")).count() == 0)


class ProjectIndexTestCase(TestCase):
  def setUp(self):
    call_command('clear_index', '--noinput', verbosity=0)

    self.user = User.objects.create_user(email="testmail@test.com", password="test_returned", object_channel="default")

    self.address1 = GoogleAddress(typed_address="São paulo, SP - Brazil")
    self.address1.save(object_channel="default")
    self.address2 = GoogleAddress(typed_address="Campinas, SP - Brazil")
    self.address2.save(object_channel="default")

  def test_index_on_create_and_update(self):
    """ Test project index gets updated when a project is created or updated """
    self.assertTrue(SearchQuerySet().models(Project).all().count() == 0)

    project = Project.objects.create(name="test project", slug="test-slug", details="abc", description="abc", owner=self.user, address=self.address1, published=True, object_channel="default")

    self.assertTrue(SearchQuerySet().models(Project).all().count() == 1)
    self.assertTrue(SearchQuerySet().models(Project).filter(address_components__exact=whoosh_raw("São Paulo-administrative_area_level_2")).count() == 1)

    project.address = self.address2
    project.save()

    self.assertTrue(SearchQuerySet().models(Project).all().count() == 1)
    self.assertTrue(SearchQuerySet().models(Project).filter(address_components__exact=whoosh_raw("Campinas-administrative_area_level_2")).count() == 1)


  def test_index_on_causes_update(self):
    """ Test project index gets updated when a cause is modified """
    cause = Cause.objects.all().order_by('pk')[0]
    project = Project.objects.create(name="test project", slug="test-slug", details="abc", description="abc", owner=self.user, address=self.address1, published=True, object_channel="default")

    self.assertTrue(SearchQuerySet().models(Project).filter(causes=cause.pk).count() == 0)

    project.causes.add(cause)

    self.assertTrue(SearchQuerySet().models(Project).filter(causes=cause.pk).count() == 1)


  def test_index_on_skill_update(self):
    """ Test project index gets updated when a skill is modified """
    skill = Skill.objects.all().order_by('pk')[0]
    project = Project.objects.create(name="test project", slug="test-slug", details="abc", description="abc", owner=self.user, address=self.address1, published=True, object_channel="default")

    self.assertTrue(SearchQuerySet().models(Project).filter(skills=skill.pk).count() == 0)

    project.skills.add(skill)

    self.assertTrue(SearchQuerySet().models(Project).filter(skills=skill.pk).count() == 1)


class OrganizationIndexTestCase(TestCase):
  def setUp(self):
    call_command('clear_index', '--noinput', verbosity=0)

    self.user = User.objects.create_user(email="testmail@test.com", password="test_returned", object_channel="default")

    self.address1 = GoogleAddress(typed_address="São paulo, SP - Brazil")
    self.address1.save(object_channel="default")
    self.address2 = GoogleAddress(typed_address="Campinas, SP - Brazil")
    self.address2.save(object_channel="default")

  def test_index_on_create_and_update(self):
    """ Test organization index gets updated when a organization is created or updated """
    self.assertTrue(SearchQuerySet().models(Project).all().count() == 0)

    organization = Organization(name="test organization", details="abc", owner=self.user, address=self.address1, published=True, type=0)
    organization.save(object_channel="default")

    self.assertTrue(SearchQuerySet().models(Organization).all().count() == 1)
    self.assertTrue(SearchQuerySet().models(Organization).filter(address_components__exact=whoosh_raw("São Paulo-administrative_area_level_2")).count() == 1)

    organization.address = self.address2
    organization.save()

    self.assertTrue(SearchQuerySet().models(Organization).all().count() == 1)
    self.assertTrue(SearchQuerySet().models(Organization).filter(address_components__exact=whoosh_raw("Campinas-administrative_area_level_2")).count() == 1)


  def test_index_on_causes_update(self):
    """ Test organization index gets updated when a cause is modified """
    cause = Cause.objects.all().order_by('pk').first()
    organization = Organization(name="test organization", details="abc", owner=self.user, address=self.address1, published=True, type=0)
    organization.save(object_channel="default")

    self.assertTrue(SearchQuerySet().models(Organization).filter(causes=cause.pk).count() == 0)

    organization.causes.add(cause)

    self.assertTrue(SearchQuerySet().models(Organization).filter(causes=cause.pk).count() == 1)


class UserIndexTestCase(TestCase):
  def setUp(self):
    call_command('clear_index', '--noinput', verbosity=0)


  def test_index_on_create_and_update(self):
    """ Test user index gets updated when a project is created or updated """
    cause = Cause.objects.all().order_by('pk').first()
    skill = Skill.objects.all().order_by('pk').first()

    self.assertTrue(SearchQuerySet().models(User).all().count() == 0)

    user = User.objects.create_user(email="testmail@test.com", password="test_returned", object_channel="default")
    profile = get_profile_model()(user=user)
    profile.save(object_channel="default")

    self.assertTrue(SearchQuerySet().models(User).filter(skills=skill.pk).count() == 0)
    profile.skills.add(skill)
    self.assertTrue(SearchQuerySet().models(User).filter(skills=skill.pk).count() == 1)

    self.assertTrue(SearchQuerySet().models(User).filter(causes=cause.pk).count() == 0)
    profile.causes.add(cause)
    self.assertTrue(SearchQuerySet().models(User).filter(causes=cause.pk).count() == 1)

    profile.skills.clear()
    profile.causes.clear()
    self.assertTrue(SearchQuerySet().models(User).filter(skills=skill.pk).count() == 0)
    self.assertTrue(SearchQuerySet().models(User).filter(causes=cause.pk).count() == 0)


  def test_index_on_delete(self):
    """ Test user index gets updated when a project is created or updated """
    self.assertTrue(SearchQuerySet().models(User).all().count() == 0)

    user = User.objects.create_user(email="testmail@test.com", password="test_returned", object_channel="default")
    profile = get_profile_model()(user=user)
    profile.save(object_channel="default")

    self.assertTrue(SearchQuerySet().models(User).all().count() == 1)
    profile.delete()
    self.assertTrue(SearchQuerySet().models(User).all().count() == 1)
    user.delete()
    self.assertTrue(SearchQuerySet().models(User).all().count() == 0)
