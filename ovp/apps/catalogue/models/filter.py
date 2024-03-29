from dateutil.relativedelta import relativedelta

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from ovp.apps.channels.models.abstract import ChannelRelationship

class Filter(ChannelRelationship):
  """
  This base class can be extended to create custom catalogue filters.
  """
  def __str__(self):
    return "Base filter"

  class Meta:
    abstract = True

  def get_filter_kwargs(self):
    """
    This should return a dictionary. This dictionary will be passed as
    **kwargs to Project.filter() when building a catalogue.

    Unfortunately we cannot operate on the queryset directly as catalogues
    get cached for performance reasons and we can't pickle functions.
    """
    raise NotImplementedError("You must override .get_filter_kwargs when implementing your custom catalogue filter.")


###################
# Category Filter #
###################

class CategoryFilter(Filter):
  categories = models.ManyToManyField("projects.Category")

  def __str__(self):
    return _("Category Filter")

  def filter_information(self):
    categories_str = ""
    for category in self.categories.all():
      categories_str += "%s\n" % category.name
    return categories_str

  def get_filter_kwargs(self):
    pks = list(self.categories.all().values_list("pk", flat=True))
    return {"categories__pk__in": pks}


####################
# DateDelta Filter #
####################

DATEDELTA_OPERATORS = (
  ("exact", _("Exact")),
  ("gt", _("Greater than")),
  ("gte", _("Greater than or equal to")),
  ("lt", _("Lesser than")),
  ("lte", _("Lesser than or equal to")),
)

class DateDeltaFilter(Filter):
  days = models.IntegerField(_("Days"), default=0)
  weeks = models.IntegerField(_("Weeks"), default=0)
  months = models.IntegerField(_("Months"), default=0)
  years = models.IntegerField(_("Years"), default=0)
  operator = models.CharField(_("Operator"), choices=DATEDELTA_OPERATORS, default="exact", max_length=30)

  def __str__(self):
    return _("DateDelta Filter")

  def filter_information(self):
    return  "{} {} days, {} weeks, {} months, {} years".format(self.get_operator_display(), self.days, self.weeks, self.months, self.years)

  def get_filter_kwargs(self):
    k = "published_date__{}".format(self.operator)
    v = timezone.now() + relativedelta(days=self.days, weeks=self.weeks, months=self.months, years=self.years)
    return {k: v}
