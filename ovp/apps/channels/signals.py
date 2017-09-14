from ovp.apps.channels.cache import get_channel

from corsheaders.signals import check_request_enabled

from django.utils.six.moves.urllib.parse import urlparse

def channel_cors(sender, request, **kwargs):
  """
  This signal checks for channel `CORS_ORIGIN_WHITELIST` settings.
  If the channel as a setting where the value match the Origin header
  the request will have the correct Access-Control-Allow-Origin on the response.
  """
  channel = get_channel(request.channel)
  if channel:
    origin = request.META.get("HTTP_ORIGIN", "")
    domain = urlparse(origin).netloc
    if domain in channel["settings"].get("CORS_ORIGIN_WHITELIST", []):
      return True

  return False

check_request_enabled.connect(channel_cors)