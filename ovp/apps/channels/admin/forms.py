from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth import authenticate

class ChannelAdminAuthenticationForm(AdminAuthenticationForm):
  def clean(self):
    username = self.cleaned_data.get('username')
    password = self.cleaned_data.get('password')

    if username is not None and password:
      self.user_cache = authenticate(self.request, username=username, password=password, channel=self.request.channel)
      if self.user_cache is None:
        raise forms.ValidationError(
          self.error_messages['invalid_login'],
          code='invalid_login',
          params={'username': self.username_field.verbose_name},
        )
      else:
        self.confirm_login_allowed(self.user_cache)

    return self.cleaned_data
