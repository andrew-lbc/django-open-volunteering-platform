from django.core.cache import cache

from ovp.apps.catalogue.models import Catalogue

from ovp.apps.projects.models import Project

from ovp.apps.search.querysets import get_project_queryset

from collections import OrderedDict

def get_catalogue(channel, slug):
  """
  Generates and caches a dictionary containing information about
  a given catalogue. This does not query the database to fetch
  the projects for a given catalog, it should be passed to fetch_catalogue
  for that.
  """
  key = "catalogue-{}-{}".format(channel, slug)
  cache_ttl = 60
  result = cache.get(key)

  if not result:
    try:
      catalogue = Catalogue.objects.prefetch_related("sections", "sections__filters").get(slug=slug, channel__slug=channel)
    except Catalogue.DoesNotExist:
      result = None
    else:
      result = {
        "name": catalogue.name,
        "slug": catalogue.slug,
        "fetched": False,
        "sections": [],
      }

      for section in catalogue.sections.all():
        section_dict = {
          "name": section.name,
          "slug": section.slug,
          "amount": section.amount,
          "filters": [],
        }

        for section_filter in section.filters.all():
          section_dict["filters"].append(section_filter.filter.get_filter_kwargs())

        result["sections"].append(section_dict)

    cache.set(key, result, cache_ttl)

  return result

def fetch_catalogue(catalogue_dict, serializer=None, request=None, context=None, channel='default'):
  """
  Fetchs a catalogue dict generated by get_catalogue()

  It removes the key "filters" and add the key "projects" to
  every section in the catalogue.

  The projects key added is a QuerySet. It can be serialized
  by passing a serializer argument.
  """
  # Base queryset
  base_queryset = get_project_queryset(request=request).filter(closed=False, published=True, channel__slug=channel)

  for i, section in enumerate(catalogue_dict["sections"]):
    qs = base_queryset

    # Filter queryset
    for kwargs in section["filters"]:
      qs = qs.filter(**kwargs)
    del catalogue_dict["sections"][i]["filters"]

    # Limit queryset
    qs = qs[:section["amount"]]

    # Serialize queryset
    if serializer:
      result = serializer(qs, many=True, context=context).data
    else:
      result = qs

    catalogue_dict["sections"][i]["projects"] = result

  catalogue_dict["fetched"] = True

  return catalogue_dict
