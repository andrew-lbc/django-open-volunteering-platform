from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from ovp.apps.channels.admin import admin_site
from ovp.apps.channels.admin import ChannelModelAdmin
from ovp.apps.channels.admin import TabularInline
from ovp.apps.projects.models import Job, JobDate

from .jobdate import JobDateAdmin, JobDateInline


class JobInline(TabularInline):
	exclude = ['title']
	model = Job
	verbose_name = _('Job')
	verbose_name_plural = _('Job')

	#fields = ('edit_dates_link',)
	readonly_fields = ['edit_dates_link']

	def edit_dates_link(self, obj):
		edit_dates_url = reverse("admin:{}_{}_change".format(obj._meta.app_label, obj._meta.model_name), args=(obj.id,))
		return '<a href="{}" target="_blank">{}</a>'.format(edit_dates_url, _('edit'))
	edit_dates_link.short_escription = _('Edit dates')
	edit_dates_link.allow_tags = True


class JobAdmin(ChannelModelAdmin):
	list_display = ['id', 'project', 'start_date', 'end_date']
	search_fields = ['id', 'project__name', 'project__nonprofit__name']

	inlines = (
		JobDateInline,
	)

admin_site.register(Job, JobAdmin)
