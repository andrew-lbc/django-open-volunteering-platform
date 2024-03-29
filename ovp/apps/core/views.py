from rest_framework import response
from rest_framework import decorators
from rest_framework import status

from ovp.apps.core import models
from ovp.apps.core import serializers
from ovp.apps.core import emails

from ovp.apps.users.models.user import User
from ovp.apps.organizations.models.organization import Organization

from drf_yasg.utils import swagger_auto_schema

from django.utils import translation

@swagger_auto_schema(methods=["GET"], responses={200: serializers.StartupSerializer})
@decorators.api_view(["GET"])
def startup(request):
  """ This view provides initial data to the client such as available skill and causes, organization and users count. """
  with translation.override(translation.get_language_from_request(request)):
    startup_data = serializers.StartupData(request)
    startup_serializer = serializers.StartupSerializer(startup_data, context={'request': request})
    return response.Response(startup_serializer.data)

@swagger_auto_schema(methods=["POST"], request_body=serializers.ContactFormSeralizer, responses={200: 'Sent', 400: 'Invalid recipients.'})
@decorators.api_view(["POST"])
def contact(request):
  """ Contact message form endpoint. """
  name = request.data.get("name", "")
  message = request.data.get("message", "")
  email = request.data.get("email", "")
  phone = request.data.get("phone", "")
  recipients = request.data.get("recipients", request.data.get("recipients[]", []))
  context = {"name": name, "message": message, "email": email, "phone": phone}

  if not type(recipients) is list:
    recipients = [recipients]

  # Check if all recipients are valid
  contacts = models.ChannelContact.objects.filter(email__in=recipients, channel__slug=request.channel)
  if contacts.count() != len(recipients):
    return response.Response({"detail": "Invalid recipients."}, status.HTTP_400_BAD_REQUEST)

  contact = emails.ContactFormMail(recipients, channel=request.channel)
  contact.sendContact(context=context)

  return response.Response({"success": True})

@swagger_auto_schema(methods=["POST"], request_body=serializers.LeadSerializer, responses={200: 'OK'})
@decorators.api_view(["POST"])
def record_lead(request):
  """ Subscribe to periodic newsletter. """
  serializer = serializers.LeadSerializer(data=request.data, context={"request": request})
  serializer.is_valid(raise_exception=True)
  serializer.save()

  return response.Response({"success": True}, status=status.HTTP_200_OK)