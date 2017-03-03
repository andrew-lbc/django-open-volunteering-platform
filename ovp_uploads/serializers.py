from django.conf import settings
from ovp_uploads.models import UploadedImage

from rest_framework import serializers

#
# GCS is actually the default ovp's bucket, so, lets try to optimize for it
# As images *never* changes urls, we can concat domain, bucket and url to obtain a full qualified
# absolute uri, preventing a #get_blog for each image
#
if hasattr(settings, 'GCS_BUCKET'):
  GCS_BASE_URI = str.join('/', ('https://storage.googleapis.com', settings.GCS_BUCKET))
  def build_absolute_uri(req, image):
    return str.join('/', (GCS_BASE_URI, image.url)) if image else None
else:
  def build_absolute_uri(req, image):
    return req.build_absolute_uri(image.url) if image else None

class UploadedImageSerializer(serializers.ModelSerializer):
  image_url = serializers.SerializerMethodField()
  image_small_url = serializers.SerializerMethodField()
  image_medium_url = serializers.SerializerMethodField()
  image_large_url = serializers.SerializerMethodField()

  class Meta:
    model = UploadedImage
    fields = ('id', 'user', 'image', 'image_url', 'image_small_url', 'image_medium_url', 'image_large_url')
    read_only_fields = ('image_small', 'image_medium', 'image_large')
    extra_kwargs = {'image': {'write_only': True}}

  def get_image_url(self, obj):
    return build_absolute_uri(self.context['request'], obj.image)

  def get_image_small_url(self, obj):
    return build_absolute_uri(self.context['request'], obj.image_small)

  def get_image_medium_url(self, obj):
    return build_absolute_uri(self.context['request'], obj.image_medium)

  def get_image_large_url(self, obj):
    return build_absolute_uri(self.context['request'], obj.image_large)
