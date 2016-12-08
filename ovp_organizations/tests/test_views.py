from django.test import TestCase
from django.core import mail

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ovp_users.models import User
from ovp_organizations.models import Organization, OrganizationInvite

import copy

base_organization = {"name": "test organization", "slug": "test-override-slug", "description": "test description", "details": "test details", "type": 0, "address": {"typed_address": "r. tecainda, 81, sao paulo"}}

class OrganizationResourceViewSetTestCase(TestCase):
  def setUp(self):
    self.client = APIClient()

  def test_cant_create_organization_unauthenticated(self):
    """Assert that it's not possible to create an organization while unauthenticated"""
    response = self.client.post(reverse("organization-list"), {}, format="json")

    self.assertTrue(response.data["detail"] == "Authentication credentials were not provided.")
    self.assertTrue(response.status_code == 401)

  def test_can_create_organization(self):
    """Assert that it's possible to create a organization while authenticated"""
    user = User.objects.create_user(email="test_can_create_organization@gmail.com", password="testcancreate")
    data = copy.copy(base_organization)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(reverse("organization-list"), data, format="json")

    self.assertTrue(response.data["id"])
    self.assertTrue(response.data["name"] == data["name"])
    self.assertTrue(response.data["slug"] == "test-organization")
    self.assertTrue(response.data["details"] == data["details"])
    self.assertTrue(response.data["description"] == data["description"])

    organization = Organization.objects.get(pk=response.data["id"])
    self.assertTrue(organization.owner.id == user.id)
    self.assertTrue(user in organization.members.all())
    self.assertTrue(organization.address.typed_address == data["address"]["typed_address"])

  def test_cant_create_organization_empty_name(self):
    """Assert that it's not possible to create a organization with empty name"""
    user = User.objects.create_user(email="test_can_create_organization@gmail.com", password="testcancreate")

    client = APIClient()
    client.force_authenticate(user=user)

    data = copy.copy(base_organization)
    data["name"] = ""

    response = client.post(reverse("organization-list"), data, format="json")
    self.assertTrue(response.data["name"][0] == "This field may not be blank.")


  def test_organization_retrieval(self):
    """Assert organizations can be retrieved"""
    user = User.objects.create_user(email="test_retrieval@gmail.com", password="testretrieval")

    client = APIClient()
    client.force_authenticate(user=user)

    data = copy.copy(base_organization)
    response = client.post(reverse("organization-list"), data, format="json")

    response = client.get(reverse("organization-detail", ["test-organization"]), format="json")

    self.assertTrue(response.data["name"] == data["name"])
    self.assertTrue(response.data["slug"] == "test-organization")
    self.assertTrue(response.data["details"] == data["details"])
    self.assertTrue(response.data["description"] == data["description"])


class OrganizationInviteTestCase(TestCase):
  def setUp(self):
    user = User.objects.create_user(email="testemail@email.com", password="test_returned")
    user.save()
    self.user = user

    user2 = User.objects.create_user(email="valid@user.com", password="test_returned")
    user2.save()
    self.user2 = user2

    organization = Organization(name="test organization", slug="test-organization", owner=user, type=0, published=True)
    organization.save()
    self.organization = organization
    self.client = APIClient()
    self.client.force_authenticate(user)


  def test_cant_invite_invalid_email(self):
    """ Test serializer does not allow invalid emails """
    response = self.client.post(reverse("organization-invite-user", ["test-organization"]), {"email": "invalidemail"}, format="json")
    self.assertTrue(response.status_code == 400)
    self.assertTrue(response.data["email"] == ["Enter a valid email address."])

  def test_cant_invite_valid_email_but_invalid_user(self):
    """ Test serializer does not allow invalid user """
    response = self.client.post(reverse("organization-invite-user", ["test-organization"]), {"email": "invalid@user.com"}, format="json")
    self.assertTrue(response.status_code == 400)
    self.assertTrue(response.data["email"] == ["This user is not valid."])

  def test_cant_invite_already_invited(self):
    """ Test serializer does not allow multiple invites to user """
    self.test_can_invite_user()
    response = self.client.post(reverse("organization-invite-user", ["test-organization"]), {"email": "valid@user.com"}, format="json")
    self.assertTrue(response.status_code == 400)
    self.assertTrue(response.data["email"] == ["This user is already invited to this organization."])

  def test_can_invite_user(self):
    """ Test it's possible to invite user """
    mail.outbox = []
    self.assertTrue(OrganizationInvite.objects.all().count() == 0)
    self.assertTrue(len(mail.outbox) == 0)

    response = self.client.post(reverse("organization-invite-user", ["test-organization"]), {"email": "valid@user.com"}, format="json")
    self.assertTrue(response.status_code == 200)
    self.assertTrue(response.data["detail"] == "User invited.")

    self.assertTrue(OrganizationInvite.objects.all().count() == 1)
    invite = OrganizationInvite.objects.last()
    self.assertTrue(invite.invitator == self.user)
    self.assertTrue(invite.invited == self.user2)

    self.assertTrue(len(mail.outbox) == 2)
    self.assertTrue(mail.outbox[0].subject == "You are invited to an organization")
    self.assertTrue(mail.outbox[1].subject == "You invited a member to an organization you own")


    third_user = User(email="third@user.com")
    third_user.save()

    fourth_user = User(email="fourth@user.com")
    fourth_user.save()

    self.organization.members.add(third_user)
    self.client.force_authenticate(third_user)

    mail.outbox = []
    self.assertTrue(len(mail.outbox) == 0)
    response = self.client.post(reverse("organization-invite-user", ["test-organization"]), {"email": "fourth@user.com"}, format="json")

    self.assertTrue(len(mail.outbox) == 3)
    self.assertTrue(mail.outbox[0].subject == "You are invited to an organization")
    self.assertTrue(mail.outbox[1].subject == "A member has been invited to your organization")
    self.assertTrue(mail.outbox[2].subject == "You invited a member to an organization you are part of")

  def test_cant_invite_unauthenticated(self):
    """ Test it's not possible to invite user if not authenticated """
    client = APIClient()
    response = client.post(reverse("organization-invite-user", ["test-organization"]), {"email": "valid@user.com"}, format="json")
    self.assertTrue(response.status_code == 401)
    self.assertTrue(response.data["detail"] == "Authentication credentials were not provided.")

  def test_cant_invite_if_not_owner_or_member(self):
    """ Test it's not possible to invite user if not a member of organization """
    client = APIClient()
    client.force_authenticate(self.user2)
    response = client.post(reverse("organization-invite-user", ["test-organization"]), {"email": "valid@user.com"}, format="json")
    self.assertTrue(response.status_code == 403)
    self.assertTrue(response.data["detail"] == "You do not have permission to perform this action.")


  def test_cant_join_unauthenticated(self):
    """ Test it's not possible to join organization if not authenticated """
    client = APIClient()
    response = client.post(reverse("organization-join", ["test-organization"]), {}, format="json")
    self.assertTrue(response.status_code == 401)
    self.assertTrue(response.data["detail"] == "Authentication credentials were not provided.")

  def test_cant_join_if_not_invited(self):
    """ Test it's not possible to join organization if not invited """
    client = APIClient()
    client.force_authenticate(self.user2)
    response = client.post(reverse("organization-join", ["test-organization"]), {}, format="json")
    self.assertTrue(response.status_code == 403)
    self.assertTrue(response.data["detail"] == "You do not have permission to perform this action.")

  def test_can_join_if_invited(self):
    """ Test it's possible to join organization if invited """
    self.test_can_invite_user()
    self.assertTrue(self.user2 not in self.organization.members.all())

    client = APIClient()
    client.force_authenticate(self.user2)
    response = client.post(reverse("organization-join", ["test-organization"]), {}, format="json")
    self.assertTrue(response.status_code == 200)
    self.assertTrue(response.data["detail"] == "Joined organization.")
    self.assertTrue(self.user2 in self.organization.members.all())

  def test_cant_revoke_if_unauthenticated(self):
    """ Test it's not possible to revoke invitation if not authenticated"""
    client = APIClient()
    response = client.post(reverse("organization-revoke-invite", ["test-organization"]), {}, format="json")
    self.assertTrue(response.status_code == 401)
    self.assertTrue(response.data["detail"] == "Authentication credentials were not provided.")

  def test_cant_revoke_if_not_owner_or_member(self):
    """ Test it's not possible to revoke invitation if not owner or member """
    client = APIClient()
    client.force_authenticate(self.user2)
    response = client.post(reverse("organization-revoke-invite", ["test-organization"]), {}, format="json")
    self.assertTrue(response.status_code == 403)
    self.assertTrue(response.data["detail"] == "You do not have permission to perform this action.")

  def test_cant_revoke_if_user_does_not_exist(self):
    """ Test it's not possible to revoke invitation if user does not exist """
    response = self.client.post(reverse("organization-revoke-invite", ["test-organization"]), {"email": "invalid@user.com"}, format="json")
    self.assertTrue(response.status_code == 400)
    self.assertTrue(response.data["email"] == ["This user is not valid."])

  def test_cant_revoke_if_invite_does_not_exist(self):
    """ Test it's not possible to revoke invitation if invitation does not exist """
    response = self.client.post(reverse("organization-revoke-invite", ["test-organization"]), {"email": "valid@user.com"}, format="json")
    self.assertTrue(response.status_code == 400)
    self.assertTrue(response.data["detail"] == "This user is not invited to this organization.")

  def test_can_revoke_invite(self):
    """ Test it's possible to revoke invitation """
    self.test_can_invite_user()
    self.assertTrue(OrganizationInvite.objects.all().count() == 2)
    response = self.client.post(reverse("organization-revoke-invite", ["test-organization"]), {"email": "valid@user.com"}, format="json")
    self.assertTrue(response.status_code == 200)
    self.assertTrue(response.data["detail"] == "Invite has been revoked.")
    self.assertTrue(OrganizationInvite.objects.all().count() == 1)


class OrganizationLeaveTestCase(TestCase):
  def setUp(self):
    user = User.objects.create_user(email="testemail@email.com", password="test_returned")
    user.save()
    self.user = user

    user2 = User.objects.create_user(email="valid@user.com", password="test_returned")
    user2.save()
    self.user2 = user2

    organization = Organization(name="test organization", slug="test-organization", owner=user, type=0, published=True)
    organization.save()
    organization.members.add(user2)
    self.organization = organization
    self.client = APIClient()

  def test_cant_leave_organization_if_unauthenticated(self):
    """ Test it's not possible to leave the organization if user is not authenticated """
    response = self.client.post(reverse("organization-leave", ["test-organization"]), {}, format="json")

    self.assertTrue(response.status_code == 401)
    self.assertTrue(response.data["detail"] == "Authentication credentials were not provided.")

  def test_cant_leave_organization_if_not_member(self):
    """ Test it's not possible to leave the organization if user is not member """
    user = User.objects.create_user(email="not@member.com", password="test_returned")
    self.client.force_authenticate(user)
    response = self.client.post(reverse("organization-leave", ["test-organization"]), {}, format="json")

    self.assertTrue(response.status_code == 403)
    self.assertTrue(response.data["detail"] == "You do not have permission to perform this action.")

  def test_cant_leave_organization_if_owner(self):
    """ Test it's not possible to leave the organization if user is not owner """
    self.client.force_authenticate(self.user)
    response = self.client.post(reverse("organization-leave", ["test-organization"]), {}, format="json")

    self.assertTrue(response.status_code == 403)
    self.assertTrue(response.data["detail"] == "You do not have permission to perform this action.")

  def test_can_leave_organization(self):
    """ Test it's possible to leave the organization """
    self.assertTrue(self.user2 in self.organization.members.all())
    self.client.force_authenticate(self.user2)
    response = self.client.post(reverse("organization-leave", ["test-organization"]), {}, format="json")

    self.assertTrue(response.status_code == 200)
    self.assertTrue(response.data["detail"] == "You've left the organization.")
    self.assertTrue(self.user2 not in self.organization.members.all())

  def test_cant_remove_member_if_unauthenticated(self):
    """ Test it's not possible to remove a member while unauthenticated """
    response = self.client.post(reverse("organization-remove-member", ["test-organization"]), {"email": "valid@user.com"}, format="json")

    self.assertTrue(response.status_code == 401)
    self.assertTrue(response.data["detail"] == "Authentication credentials were not provided.")

  def test_cant_remove_member_if_not_owner(self):
    """ Test it's not possible to remove a member if not the owner """
    self.client.force_authenticate(self.user2)
    response = self.client.post(reverse("organization-remove-member", ["test-organization"]), {"email": "valid@user.com"}, format="json")

    self.assertTrue(response.status_code == 403)
    self.assertTrue(response.data["detail"] == "You do not have permission to perform this action.")

  def test_cant_remove_member_if_not_member(self):
    """ Test it's not possible to remove a member if the user is not a member """
    self.client.force_authenticate(self.user)
    response = self.client.post(reverse("organization-remove-member", ["test-organization"]), {"email": "invalid@user.com"}, format="json")

    self.assertTrue(response.status_code == 400)
    self.assertTrue(response.data["email"] == ["This user is not valid."])

  def test_can_remove_member(self):
    """ Test it's possible to remove a member """
    self.client.force_authenticate(self.user)
    self.client.force_authenticate(self.user)
    response = self.client.post(reverse("organization-remove-member", ["test-organization"]), {"email": "valid@user.com"}, format="json")

    self.assertTrue(response.status_code == 200)
    self.assertTrue(response.data["detail"] == "Member was removed.")
