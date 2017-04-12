from ovp_search import helpers
from haystack.query import SQ

from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import NotAuthenticated

from django.db.models import When, F, IntegerField, Count, Case

import json

#####################
## ViewSet filters ##
#####################

class ProjectRelevanceOrderingFilter(OrderingFilter):
  def get_skills_and_causes(self, request):
    if not request.user.is_authenticated():
      raise NotAuthenticated()

    user = request.user
    output = {"skills": [], "causes": []}

    if user.profile:
      output["skills"] = user.profile.skills.values_list('id', flat=True)
      output["causes"] = user.profile.causes.values_list('id', flat=True)

    return output

  def annotate_queryset(self, queryset, request):
    self.get_skills_and_causes(request)

    queryset = queryset\
                .annotate(\
                  cause_relevance =
                    Count(
                      Case(When(causes__pk__in=[1,3], then=1),
                           output_field=IntegerField()),
                      distinct=True),
                  skill_relevance =
                    Count(
                      Case(When(skills__pk__in=[1,2,4], then=1),
                                output_field=IntegerField()),
                      distinct=True))\
                .annotate(relevance = F('cause_relevance') + F('skill_relevance'))

    return queryset

  def filter_queryset(self, request, queryset, view):
    ordering = self.get_ordering(request, queryset, view)

    if ordering:
      if "relevance" in ordering or "-relevance" in ordering:
        queryset = self.annotate_queryset(queryset, request)

    if ordering:
      return queryset.order_by(*ordering)

    return queryset


######################
## Haystack filters ##
######################

def by_skills(queryset, skill_string=''):
  """ Filter queryset by a comma delimeted skill list """
  if skill_string:
    skills = skill_string.split(',')
    q_obj = SQ()
    for s in skills:
      if len(s) > 0:
        q_obj.add(SQ(skills=s), SQ.OR)
    queryset = queryset.filter(q_obj)
  return queryset


def by_causes(queryset, cause_string=''):
  """ Filter queryset by a comma delimeted cause list """
  if cause_string:
    causes = cause_string.split(',')
    q_obj = SQ()
    for c in causes:
      if len(c) > 0:
        q_obj.add(SQ(causes=c), SQ.OR)
    queryset = queryset.filter(q_obj)
  return queryset


def by_published(queryset, published_string='true'):
  """ Filter queryset by publish status """
  if published_string == 'true':
    queryset = queryset.filter(published=True)
  elif published_string == 'false':
    queryset = queryset.filter(published=False)
  # Any other value will return both published and unpublished
  return queryset


def by_name(queryset, name=None):
  """ Filter queryset by name, with word wide auto-completion """
  if name:
    queryset = queryset.filter(name=name)
  return queryset

def by_name_autocomplete(queryset, name=None):
  """ Filter queryset by name, using char wide auto-completion """
  if name:
    queryset = queryset.autocomplete(name_autocomplete=name)
  return queryset


def by_address(queryset, address='', project=False):
  """
  Filter queryset by publish status.

  If project=True, we also apply a project exclusive filter
  """
  if address:
    address = json.loads(address)

    if u'address_components' in address:
      types = []

      if len(address[u'address_components']):
        for component in address[u'address_components']:
          for component_type in component[u'types']:
            type_string = u"{}-{}".format(component[u'long_name'], component_type).strip()

            if type_string not in types:
              types.append(type_string)

        # Filter all address components
        for address_type in types:
          queryset = queryset.filter(address_components=helpers.whoosh_raw(address_type))
      else: # remote projects
        if project:
          queryset = queryset.filter(can_be_done_remotely=True)
  return queryset
