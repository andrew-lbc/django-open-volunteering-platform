from django.test import TestCase
from django.test.utils import override_settings
from django.core.management import call_command
from django.core.cache import cache

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ovp.apps.users.models import User
from ovp.apps.users.models.profile import get_profile_model
from ovp.apps.projects.models import Project, Job
from ovp.apps.organizations.models import Organization
from ovp.apps.core.models import GoogleAddress, Cause, Skill
from ovp.apps.channels.models import Channel
from ovp.apps.channels.models import ChannelSetting

import json



"""
Helpers
"""
def create_sample_projects():
  # Create sample projects
  user1 = User.objects.create_user(name="a", email="testmail-projects@test.com", password="test_returned", object_channel="default")
  user2 = User.objects.create_user(name="a", email="testmail-projects@test.com", password="test_returned", object_channel="test-channel")

  address1 = GoogleAddress(typed_address="São paulo, SP - Brazil")
  address2 = GoogleAddress(typed_address="Campinas, SP - Brazil")
  address3 = GoogleAddress(typed_address="New york, New york - United States")
  address4 = GoogleAddress(typed_address="New york, New york - United States")
  address5 = GoogleAddress(typed_address="New york, New york - United States")
  address1.save(object_channel="default")
  address2.save(object_channel="default")
  address3.save(object_channel="default")
  address4.save(object_channel="default")
  address5.save(object_channel="test-channel")

  project = Project(name="test project", slug="test-slug", details="abc", description="abc", owner=user1, address=address1, published=True)
  project.save(object_channel="default")
  project.causes.add(Cause.objects.get(pk=1))
  project.skills.add(Skill.objects.get(pk=1))
  project.skills.add(Skill.objects.get(pk=4))

  project = Project(name="test project2", slug="test-slug2", details="abc", description="abc", owner=user1, address=address2, highlighted=True, published=True)
  project.save(object_channel="default")
  project.causes.add(Cause.objects.get(pk=2))
  job = Job(can_be_done_remotely=True, project=project)
  job.save(object_channel="default")

  project = Project(name="test project3", slug="test-slug3", details="abc", description="abc", owner=user1, address=address3, published=True)
  project.save(object_channel="default")
  project.skills.add(Skill.objects.get(pk=2))
  project.causes.add(Cause.objects.get(pk=3))
  job = Job(can_be_done_remotely=True, project=project)
  job.save(object_channel="default")

  project = Project(name="test project4", slug="test-slug4", details="abc", description="abc", owner=user1, address=address4, published=False)
  project.save(object_channel="default")

  project = Project(name="test project5", slug="test-slug5", details="abc", description="abc", owner=user2, address=address5, published=True)
  project.save(object_channel="test-channel")

def create_sample_organizations():
  user1 = User.objects.create_user(name="z", email="testmail-organizations@test.com", password="test_returned", object_channel="default")
  user2 = User.objects.create_user(name="a", email="testmail-organizations@test.com", password="test_returned", object_channel="test-channel")

  address1 = GoogleAddress(typed_address="São paulo, SP - Brazil")
  address2 = GoogleAddress(typed_address="Santo André, SP - Brazil")
  address3 = GoogleAddress(typed_address="New york, New york - United States")
  address4 = GoogleAddress(typed_address="New york, New york - United States")
  address5 = GoogleAddress(typed_address="New york, New york - United States")
  address1.save(object_channel="default")
  address2.save(object_channel="default")
  address3.save(object_channel="default")
  address4.save(object_channel="default")
  address5.save(object_channel="test-channel")

  organization = Organization(name="test organization", details="abc", owner=user1, address=address1, published=True, type=0)
  organization.save(object_channel="default")
  organization.causes.add(Cause.objects.all().order_by('pk')[0])

  organization = Organization(name="test organization2", details="abc", owner=user1, address=address2, published=True, highlighted=True, type=0)
  organization.save(object_channel="default")
  organization.causes.add(Cause.objects.all().order_by('pk')[1])

  organization = Organization(name="test organization3", details="abc", owner=user1, address=address3, published=True, type=0)
  organization.save(object_channel="default")

  organization = Organization(name="test organization4", details="abc", owner=user1, address=address4, published=False, type=0)
  organization.save(object_channel="default")

  organization = Organization(name="test organization5", details="abc", owner=user2, address=address5, published=True, type=0)
  organization.save(object_channel="test-channel")


def create_sample_users():
  user1 = User(name="user one", email="testmail1@test.com", password="test_returned")
  user1.save(object_channel="default")

  user2 = User(name="user two", email="testmail2@test.com", password="test_returned")
  user2.save(object_channel="default")

  user3 = User(name="user three", email="testmail3@test.com", password="test_returned")
  user3.save(object_channel="default")

  user4 = User(name="user four", email="testmail4@test.com", password="test_returned", public=False)
  user4.save(object_channel="default")

  user5 = User(name="user five", email="testmail5@test.com", password="test_returned")
  user5.save(object_channel="test-channel")

  UserProfile = get_profile_model()
  profile1 = UserProfile(user=user1, full_name="user one", about="about one")
  profile1.save(object_channel="default")
  profile1.causes.add(Cause.objects.get(pk=1))
  profile1.causes.add(Cause.objects.get(pk=2))
  profile1.skills.add(Skill.objects.get(pk=1))
  profile1.skills.add(Skill.objects.get(pk=2))

  profile2 = UserProfile(user=user2, full_name="user two", about="about two")
  profile2.save(object_channel="default")
  profile2.causes.add(Cause.objects.get(pk=1))
  profile2.causes.add(Cause.objects.get(pk=3))
  profile2.skills.add(Skill.objects.get(pk=1))
  profile2.skills.add(Skill.objects.get(pk=3))

  profile3 = UserProfile(user=user3, full_name="user three", about="about three")
  profile3.save(object_channel="default")


"""
Tests
"""
class ProjectSearchTestCase(TestCase):
  def setUp(self):
    call_command('clear_index', '--noinput', verbosity=0)
    Channel.objects.create(name="Test channel", slug="test-channel")
    create_sample_projects()
    self.client = APIClient()

    cache.clear()

  def test_query_optimization(self):
    """
    Test project search does only 4 queries
    """
    # 5 queries are search related
    # 2 are middleware/channel related
    with self.assertNumQueries(7):
      response = self.client.get(reverse("search-projects-list"), format="json")

  def test_query_gets_cached(self):
    """
    Test project search gets cached
    """
    response = self.client.get(reverse("search-projects-list"), format="json")

    # Second request should not hit db
    with self.assertNumQueries(0):
      response = self.client.get(reverse("search-projects-list"), format="json")

  def test_no_filter(self):
    """
    Test searching with no filters return all available projects
    """
    response = self.client.get(reverse("search-projects-list"), format="json")
    self.assertEqual(len(response.data["results"]), 3)

  def test_channel_filter(self):
    """
    Test searching with with channel header return all channel projects
    """
    response = self.client.get(reverse("search-projects-list"), format="json", HTTP_X_OVP_CHANNEL="test-channel")
    self.assertEqual(len(response.data["results"]), 1)

  def test_result_hiding(self):
    """
    Test it's possible to hide results through settings
    """
    ChannelSetting.objects.create(key="FILTER_OUT_PROJECTS", value="'name': 'test project'", object_channel="default")

    response = self.client.get(reverse("search-projects-list"), format="json")
    self.assertEqual(len(response.data["results"]), 2)

  def test_publish_filter(self):
    """
    Test searching with publish filter == "true", "false" and "both" return correct projects
    """
    response = self.client.get(reverse("search-projects-list") + "?published=true", format="json")
    self.assertEqual(len(response.data["results"]), 3)

    response = self.client.get(reverse("search-projects-list") + "?published=false", format="json")
    self.assertEqual(len(response.data["results"]), 1)

    response = self.client.get(reverse("search-projects-list") + "?published=both", format="json")
    self.assertEqual(len(response.data["results"]), 4)

  def test_name_filter(self):
    """
    Test searching with name filter returns project filtered by name(ngram)
    """
    response = self.client.get(reverse("search-projects-list") + "?name=project2", format="json")
    self.assertEqual(len(response.data["results"]), 1)

  def test_highlighted_filter(self):
    """
    Test searching with highlighted=true returns only highlighted fields
    """
    response = self.client.get(reverse("search-projects-list") + "?highlighted=true", format="json")
    self.assertEqual(len(response.data["results"]), 1)
    self.assertEqual(str(response.data["results"][0]["name"]), "test project2")

  def test_address_filter(self):
    """
    Test searching with address filter returns only results filtered by address
    """
    # Filter by city
    response = self.client.get(reverse("search-projects-list") + '?address={"address_components":[{"types":["locality", "administrative_area_level_2"], "long_name":"São Paulo"}]}', format="json")
    self.assertEqual(len(response.data["results"]), 1)

    # Filter by state
    response = self.client.get(reverse("search-projects-list") + '?address={"address_components":[{"types":["administrative_area_level_1"], "long_name":"State of São Paulo"}]}', format="json")
    self.assertEqual(len(response.data["results"]), 2)

    # Filter by country
    response = self.client.get(reverse("search-projects-list") + '?address={"address_components":[{"types":["country"], "long_name":"United States"}]}', format="json")
    self.assertEqual(len(response.data["results"]), 1)

    # Filter remote jobs
    response = self.client.get(reverse("search-projects-list") + '?address={"address_components":[]}', format="json")
    self.assertEqual(len(response.data["results"]), 2)

  def test_causes_filter(self):
    """
    Test searching with causes filter returns only results filtered by cause
    """
    cause_id1 = Cause.objects.all().order_by('pk')[0].pk
    cause_id2 = Cause.objects.all().order_by('pk')[1].pk

    response = self.client.get(reverse("search-projects-list") + "?cause=" + str(cause_id1), format="json")
    self.assertEqual(len(response.data["results"]), 1)
    self.assertEqual(str(response.data["results"][0]["name"]), "test project")

    response = self.client.get(reverse("search-projects-list") + "?cause=" + str(cause_id2), format="json")
    self.assertEqual(len(response.data["results"]), 1)
    self.assertEqual(str(response.data["results"][0]["name"]), "test project2")

    response = self.client.get(reverse("search-projects-list") + "?cause={},{}".format(cause_id1, cause_id2), format="json")
    self.assertEqual(len(response.data["results"]), 2)

  def test_skills_filter(self):
    """
    Test searching with skill filter returns only results filtered by skill
    """
    skill_id1 = Skill.objects.all().order_by('pk')[0].pk
    skill_id2 = Skill.objects.all().order_by('pk')[1].pk

    response = self.client.get(reverse("search-projects-list") + "?skill=" + str(skill_id1), format="json")
    self.assertEqual(len(response.data["results"]), 1)
    self.assertEqual(str(response.data["results"][0]["name"]), "test project")

    response = self.client.get(reverse("search-projects-list") + "?skill=" + str(skill_id2), format="json")
    self.assertEqual(len(response.data["results"]), 1)
    self.assertEqual(str(response.data["results"][0]["name"]), "test project3")

    response = self.client.get(reverse("search-projects-list") + "?skill={},{}".format(skill_id1, skill_id2), format="json")
    self.assertEqual(len(response.data["results"]), 2)

  def test_query_filter(self):
    """
    Test searching with query filter returns only results filtered by text query
    """
    response = self.client.get(reverse("search-projects-list") + "?query=project3", format="json")
    self.assertEqual(len(response.data["results"]), 1)
    self.assertEqual(str(response.data["results"][0]["name"]), "test project3")

    response = self.client.get(reverse("search-projects-list") + "?query=project4", format="json")
    self.assertEqual(len(response.data["results"]), 0)


class OrganizationSearchTestCase(TestCase):
  def setUp(self):
    call_command('clear_index', '--noinput', verbosity=0)
    Channel.objects.create(name="Test channel", slug="test-channel")
    create_sample_organizations()
    self.client = APIClient()

    cache.clear()

  def test_query_optimization(self):
    """
    Test organization search does only 2 queries
    """
    # 2 queries are search related
    # 2 are middleware/channel related
    with self.assertNumQueries(4):
      response = self.client.get(reverse("search-organizations-list"), format="json")

  def test_query_gets_cached(self):
    """
    Test organization search gets cached
    """
    response = self.client.get(reverse("search-organizations-list"), format="json")

    # Second request should not hit db
    with self.assertNumQueries(0):
      response = self.client.get(reverse("search-organizations-list"), format="json")

  def test_no_filter(self):
    """
    Test searching with no filters return all available organizations
    """
    response = self.client.get(reverse("search-organizations-list"), format="json")
    self.assertEqual(len(response.data["results"]), 3)

  def test_channel_filter(self):
    """
    Test searching with with channel header return all channel organizations
    """
    response = self.client.get(reverse("search-organizations-list"), format="json", HTTP_X_OVP_CHANNEL="test-channel")
    self.assertEqual(len(response.data["results"]), 1)

  def test_result_hiding(self):
    """
    Test it's possible to hide results through settings
    """
    ChannelSetting.objects.create(key="FILTER_OUT_ORGANIZATIONS", value="'name': 'test organization'", object_channel="default")

    response = self.client.get(reverse("search-organizations-list"), format="json")
    self.assertEqual(len(response.data["results"]), 2)

  def test_publish_filter(self):
    """
    Test searching with publish filter == "true", "false" and "both" return correct organizations
    """
    response = self.client.get(reverse("search-organizations-list") + "?published=true", format="json")
    self.assertEqual(len(response.data["results"]), 3)

    response = self.client.get(reverse("search-organizations-list") + "?published=false", format="json")
    self.assertEqual(len(response.data["results"]), 1)

    response = self.client.get(reverse("search-organizations-list") + "?published=both", format="json")
    self.assertEqual(len(response.data["results"]), 4)

  def test_name_filter(self):
    """
    Test searching with name filter returns organizations filtered by name(ngram)
    """
    response = self.client.get(reverse("search-organizations-list") + "?name=organization2", format="json")
    self.assertEqual(len(response.data["results"]), 1)

  def test_highlighted_filter(self):
    """
    Test searching with highlighted=true returns only highlighted fields
    """
    response = self.client.get(reverse("search-organizations-list") + "?highlighted=true", format="json")
    self.assertEqual(len(response.data["results"]), 1)
    self.assertEqual(str(response.data["results"][0]["name"]), "test organization2")

  def test_address_filter(self):
    """
    Test searching with address filter returns only results filtered by address
    """
    # Filter by city
    response = self.client.get(reverse("search-organizations-list") + '?address={"address_components":[{"types":["locality"], "long_name":"São Paulo"}]}', format="json")
    self.assertEqual(len(response.data["results"]), 1)

    # Filter by state
    response = self.client.get(reverse("search-organizations-list") + '?address={"address_components":[{"types":["administrative_area_level_1"], "long_name":"State of São Paulo"}]}', format="json")
    self.assertEqual(len(response.data["results"]), 2)

    # Filter by country
    response = self.client.get(reverse("search-organizations-list") + '?address={"address_components":[{"types":["country"], "long_name":"United States"}]}', format="json")
    self.assertEqual(len(response.data["results"]), 1)

  def test_causes_filter(self):
    """
    Test searching with causes filter returns only results filtered by cause
    """
    cause_id1 = Cause.objects.all().order_by('pk')[0].pk
    cause_id2 = Cause.objects.all().order_by('pk')[1].pk

    response = self.client.get(reverse("search-organizations-list") + "?cause=" + str(cause_id1), format="json")
    self.assertEqual(len(response.data["results"]), 1)
    self.assertEqual(str(response.data["results"][0]["name"]), "test organization")

    response = self.client.get(reverse("search-organizations-list") + "?cause=" + str(cause_id2), format="json")
    self.assertEqual(len(response.data["results"]), 1)
    self.assertEqual(str(response.data["results"][0]["name"]), "test organization2")

    response = self.client.get(reverse("search-organizations-list") + "?cause={},{}".format(cause_id1, cause_id2), format="json")
    self.assertEqual(len(response.data["results"]), 2)

  def test_query_filter(self):
    """
    Test searching with query filter returns only results filtered by text query
    """
    response = self.client.get(reverse("search-organizations-list") + "?query=organization3", format="json")
    self.assertEqual(len(response.data["results"]), 1)
    self.assertEqual(str(response.data["results"][0]["name"]), "test organization3")

    response = self.client.get(reverse("search-organizations-list") + "?query=organization4", format="json")
    self.assertEqual(len(response.data["results"]), 0)



@override_settings(OVP_SEARCH={'ENABLE_USER_SEARCH': True})
class UserSearchTestCase(TestCase):
  def setUp(self):
    call_command('clear_index', '--noinput', verbosity=0)
    Channel.objects.create(name="Test channel", slug="test-channel")
    create_sample_users()
    self.client = APIClient()

    cache.clear()

  def test_query_optimization(self):
    """
    Test user search does only 3 queries
    """
    # 3 queries are search related
    # 2 are middleware/channel related
    with self.assertNumQueries(5):
      response = self.client.get(reverse("search-users-list"), format="json")

  def test_query_gets_cached(self):
    """
    Test user search gets cached
    """
    response = self.client.get(reverse("search-users-list"), format="json")

    # Second request should not hit db
    with self.assertNumQueries(0):
      response = self.client.get(reverse("search-users-list"), format="json")

  def test_no_filter(self):
    """
    Test searching with no filter returns all results
    """
    response = self.client.get(reverse("search-users-list"), format="json")
    self.assertEqual(len(response.data["results"]), 3)

  def test_channel_filter(self):
    """
    Test searching with with channel header return all channel users
    """
    response = self.client.get(reverse("search-users-list"), format="json", HTTP_X_OVP_CHANNEL="test-channel")
    self.assertEqual(len(response.data["results"]), 1)

  def test_causes_filter(self):
    """
    Test searching with causes filter returns only results filtered by cause
    """
    response = self.client.get(reverse("search-users-list") + "?cause=1,2", format="json")
    self.assertEqual(len(response.data["results"]), 2)
    self.assertEqual(str(response.data["results"][0]["profile"]["full_name"]), "user one")
    self.assertEqual(str(response.data["results"][1]["profile"]["full_name"]), "user two")

    response = self.client.get(reverse("search-users-list") + "?cause=OR,1,2", format="json")
    self.assertEqual(len(response.data["results"]), 2)
    self.assertEqual(str(response.data["results"][0]["profile"]["full_name"]), "user one")
    self.assertEqual(str(response.data["results"][1]["profile"]["full_name"]), "user two")

    response = self.client.get(reverse("search-users-list") + "?cause=AND,1,2", format="json")
    self.assertEqual(len(response.data["results"]), 1)
    self.assertEqual(str(response.data["results"][0]["profile"]["full_name"]), "user one")


  def test_skills_filter(self):
    """
    Test searching with skills filter returns only results filtered by cause
    """
    response = self.client.get(reverse("search-users-list") + "?skill=1,2", format="json")
    self.assertEqual(len(response.data["results"]), 2)
    self.assertEqual(str(response.data["results"][0]["profile"]["full_name"]), "user one")
    self.assertEqual(str(response.data["results"][1]["profile"]["full_name"]), "user two")

  def test_name_filter(self):
    """
    Test searching with name filter returns organizations filtered by name(ngram)
    """
    response = self.client.get(reverse("search-users-list") + "?name=user", format="json")
    self.assertEqual(len(response.data["results"]), 3)

    response = self.client.get(reverse("search-users-list") + "?name=one", format="json")

    self.assertEqual(len(response.data["results"]), 1)
    self.assertEqual(response.data["results"][0]["name"], "user one")

    response = self.client.get(reverse("search-users-list") + "?name=two", format="json")
    self.assertEqual(len(response.data["results"]), 1)
    self.assertEqual(response.data["results"][0]["name"], "user two")

    response = self.client.get(reverse("search-users-list") + "?name=three", format="json")
    self.assertEqual(len(response.data["results"]), 1)
    self.assertEqual(response.data["results"][0]["name"], "user three")

  @override_settings(OVP_SEARCH={'ENABLE_USER_SEARCH': False})
  def test_user_search_must_be_enabled(self):
    """
    Test searching for users must be enabled in settings
    """
    response = self.client.get(reverse("search-users-list"), format="json")
    self.assertEqual(response.status_code, 403)


@override_settings(OVP_SEARCH={'ENABLE_USER_SEARCH': True})
class OrderingTestCase(TestCase):
  def setUp(self):
    call_command('clear_index', '--noinput', verbosity=0)
    Channel.objects.create(name="Test channel", slug="test-channel")
    create_sample_projects()
    create_sample_organizations()
    self.client = APIClient()


  def test_ordering_descending(self):
    """ Assert it's possible to order projects, users and organizations by fields ascending """
    response = self.client.get(reverse("search-projects-list") + "?ordering=-name", format="json")
    self.assertEqual(str(response.data["results"][0]["name"]), "test project3")

    response = self.client.get(reverse("search-organizations-list") + "?ordering=-name", format="json")
    self.assertEqual(str(response.data["results"][0]["name"]), "test organization3")

    response = self.client.get(reverse("search-users-list") + "?ordering=-name", format="json")
    self.assertEqual(str(response.data["results"][0]["name"]), "z")


  def test_ordering_ascending(self):
    """ Assert it's possible to order projects, users and organizations by fields descending """
    response = self.client.get(reverse("search-projects-list") + "?ordering=name", format="json")
    self.assertEqual(str(response.data["results"][0]["name"]), "test project")

    response = self.client.get(reverse("search-organizations-list") + "?ordering=name", format="json")
    self.assertEqual(str(response.data["results"][0]["name"]), "test organization")

    response = self.client.get(reverse("search-users-list") + "?ordering=name", format="json")
    self.assertEqual(str(response.data["results"][0]["name"]), "a")


  def test_ordering_by_relevance(self):
    """ Assert it's possible to order projects by relevance """
    UserProfile = get_profile_model()
    user = User(name="b", email="testproject@relevance.com", password="testpassword")
    user.save(object_channel="default")

    self.client.force_authenticate(user=user)
    response = self.client.get(reverse("search-projects-list") + "?ordering=-relevance,-created_date", format="json")
    self.assertEqual(response.status_code, 200)

    profile = UserProfile(user=user)
    profile.save(object_channel="default")
    profile.causes.add(Cause.objects.get(pk=1))
    profile.skills.add(Skill.objects.get(pk=1))
    profile.skills.add(Skill.objects.get(pk=2))
    profile.causes.add(Cause.objects.get(pk=3))

    response = self.client.get(reverse("search-projects-list") + "?ordering=-relevance,-created_date", format="json")
    self.assertEqual(str(response.data["results"][0]["name"]), "test project3")
    self.assertEqual(str(response.data["results"][1]["name"]), "test project")
    self.assertEqual(str(response.data["results"][2]["name"]), "test project2")

  def test_ordering_by_relevance_unauthenticated(self):
    """ Assert it's not possible to order projects by relevance while unauthenticated """
    response = self.client.get(reverse("search-projects-list") + "?ordering=-relevance", format="json")
    self.assertEqual(response.status_code, 401)


class CityCountryTestCase(TestCase):
  def setUp(self):
    call_command('clear_index', '--noinput', verbosity=0)
    Channel.objects.create(name="Test channel", slug="test-channel")
    create_sample_projects()
    create_sample_organizations()

  def test_query_country_deprecated(self):
    client = APIClient()

    response = client.get(reverse("search-query-country", ["Brazil"]), format="json")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 2)
    self.assertIn("Campinas", response.data)
    self.assertIn("São Paulo", response.data)

    response = client.get(reverse("search-query-country", ["United States"]), format="json")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 1)
    self.assertIn("New York", response.data)

  def test_available_country_cities(self):
    client = APIClient()

    response = client.get(reverse("available-country-cities", ["Brazil"]), format="json")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data["projects"]), 1)
    self.assertEqual(len(response.data["organizations"]), 1)
    self.assertEqual(len(response.data["common"]), 1)
    self.assertIn("Campinas", response.data["projects"])
    self.assertIn("Santo André", response.data["organizations"])
    self.assertIn("São Paulo", response.data["common"])

    response = client.get(reverse("available-country-cities", ["United States"]), format="json")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data["projects"]), 0)
    self.assertEqual(len(response.data["organizations"]), 0)
    self.assertEqual(len(response.data["common"]), 1)
    self.assertIn("New York", response.data["common"])

  def test_available_country_cities_cache(self):
    self.test_available_country_cities()
    self.assertTrue(cache.get("available-cities-default-{}".format(hash("Brazil"))))
    self.assertTrue(cache.get("available-cities-default-{}".format(hash("United States"))))

  def test_available_country_cities_per_channel(self):
    client = APIClient()

    response = client.get(reverse("available-country-cities", ["Brazil"]), format="json", HTTP_X_OVP_CHANNEL="test-channel")
    self.assertEqual(len(response.data["projects"]), 0)
    self.assertEqual(len(response.data["organizations"]), 0)
    self.assertEqual(len(response.data["common"]), 0)

    response = client.get(reverse("available-country-cities", ["United States"]), format="json", HTTP_X_OVP_CHANNEL="test-channel")
    self.assertEqual(len(response.data["projects"]), 0)
    self.assertEqual(len(response.data["organizations"]), 0)
    self.assertEqual(len(response.data["common"]), 1)
    self.assertIn("New York", response.data["common"])
