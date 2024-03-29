from django.db.models import Q

from ovp.apps.projects.serializers import project as serializers
from ovp.apps.projects import models
from ovp.apps.projects.permissions import ProjectCreateOwnsOrIsOrganizationMember
from ovp.apps.projects.permissions import ProjectRetrieveOwnsOrIsOrganizationMember

from ovp.apps.channels.viewsets.decorators import ChannelViewSet
from ovp.apps.channels.cache import get_channel_setting

from ovp.apps.core.helpers.xls import Response as XLSResponse
from ovp.apps.core.mixins import PostCreateMixin
from ovp.apps.core.mixins import BookmarkMixin
from ovp.apps.core.serializers import post as post_serializers
from ovp.apps.core.serializers import EmptySerializer
from ovp.apps.core.pagination import StandardResultsSetPagination

from rest_framework import decorators
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from django.utils.timezone import get_current_timezone
from django.utils.translation import ugettext as _


EXPORT_APPLIED_USERS_HEADERS = [
  _('User Name'), _('User Email'), _('User Phone'), _('Applied At'), _('Role'), _('Status')
]

@ChannelViewSet
class ProjectResourceViewSet(BookmarkMixin, PostCreateMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
  """
  ProjectResourceViewSet resource endpoint
  """
  queryset = models.Project.objects.filter(deleted=False)
  lookup_field = 'slug'
  lookup_value_regex = '[^/]+' # default is [^/.]+ - here we're allowing dots in the url slug field

  ##################
  # ViewSet routes #
  ##################
  def retrieve(self, *args, **kwargs):
    """ Retrieve a project. """
    return super(ProjectResourceViewSet, self).retrieve(*args, **kwargs)

  def create(self, request, *args, **kwargs):
    """ Create a project. """
    request.data['owner'] = request.data.get('owner', None) or request.user.pk

    serializer = self.get_serializer(data=request.data, context=self.get_serializer_context())
    serializer.is_valid(raise_exception=True)
    serializer.save()

    headers = self.get_success_headers(serializer.data)
    return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

  def partial_update(self, request, *args, **kwargs):
    """ Partially update an organization object. """
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=True, context=self.get_serializer_context())
    serializer.is_valid(raise_exception=True)
    serializer.save()

    if getattr(instance, '_prefetched_objects_cache', None): #pragma: no cover
      instance = self.get_object()
      serializer = self.get_serializer(instance)

    return response.Response(serializer.data)

  @swagger_auto_schema(method="POST", responses={200: "OK"})
  @decorators.detail_route(['POST'])
  def close(self, request, *args, **kwargs):
    """ Close a project. """
    project = self.get_object()
    project.closed = True
    project.save()
    serializer = self.get_serializer_class()(project, context=self.get_serializer_context())
    return response.Response(serializer.data)

  @swagger_auto_schema(method="GET", responses={200: "OK"})
  @decorators.detail_route(['GET'])
  def export_applied_users(self, request, *args, **kwargs):
    """ Export a list of applied volunteers in xls format. """
    project = self.get_object()

    applied_users = [EXPORT_APPLIED_USERS_HEADERS]
    for apply in project.apply_set.all():
      user = apply.user
      role = apply.role.name if apply.role is not None else ''
      applied_users.append([
        apply.username, apply.email or apply.user.email, apply.phone or apply.user.phone,
        apply.date.astimezone(get_current_timezone()).strftime('%d/%m/%Y %T %z'), role, apply.status,
        ])

    filename = '{}-applied-users.xls'.format(project.slug)
    return XLSResponse(applied_users, filename, _('Applied Users'))

  @decorators.list_route(['GET'])
  def manageable(self, request, *args, **kwargs):
    """ Retrieve a list of projects the authenticated user can manage. """
    paginator = StandardResultsSetPagination()
    projects = self.get_queryset().filter(Q(owner=request.user) | Q(organization__owner=request.user) | Q(organization__members=request.user))
    projects = projects.order_by('created_date')

    params = request.query_params
    if params.get('no_organization') == 'true':
      projects = projects.filter(organization=None)
    if params.get('published'):
      published = params.get('published') == 'true'
      projects = projects.filter(published=published)
    if params.get('closed'):
      closed = params.get('closed') == 'true'
      projects = projects.filter(closed=closed)
    if params.get('query'):
      query = params.get('query')
      projects = projects.filter(content=query)


    page = paginator.paginate_queryset(projects, request)
    if page is not None:
      serializer = self.get_serializer_class()(page, many=True, context=self.get_serializer_context())
      return paginator.get_paginated_response(serializer.data)

    serializer = self.get_serializer_class()(projects, many=True, context=self.get_serializer_context())
    return response.Response(serializer.data)


  ###################
  # ViewSet methods #
  ###################
  def get_bookmark_model(self):
    return models.ProjectBookmark

  def get_bookmark_kwargs(self):
    return {"project": self.get_object()}

  def get_permissions(self):
    request = self.get_serializer_context()['request']
    if self.action == 'create':
      if int(get_channel_setting(request.channel, "CAN_CREATE_PROJECTS_IN_ANY_ORGANIZATION")[0]):
        self.permission_classes = (permissions.IsAuthenticated, )
      else:
        self.permission_classes = (permissions.IsAuthenticated, ProjectCreateOwnsOrIsOrganizationMember)

    if self.action == 'partial_update':
      self.permission_classes = (permissions.IsAuthenticated, ProjectRetrieveOwnsOrIsOrganizationMember)

    if self.action == 'retrieve':
      self.permission_classes = ()

    if self.action == 'manageable':
      self.permission_classes = (permissions.IsAuthenticated, )

    if self.action == 'close':
      self.permission_classes = (permissions.IsAuthenticated, ProjectRetrieveOwnsOrIsOrganizationMember)

    if self.action in ['bookmark', 'unbookmark', 'bookmarked']:
      self.permission_classes = self.get_bookmark_permissions()

    if self.action == 'export_applied_users':
      self.permission_classes = (permissions.IsAuthenticated, ProjectRetrieveOwnsOrIsOrganizationMember)

    if self.action == 'post':
      self.permission_classes = (permissions.IsAuthenticated, ProjectRetrieveOwnsOrIsOrganizationMember)

    if self.action == 'post_patch_delete':
      self.permission_classes = (permissions.IsAuthenticated, ProjectRetrieveOwnsOrIsOrganizationMember)

    return super(ProjectResourceViewSet, self).get_permissions()

  def get_serializer_class(self):
    if self.action in ['create', 'partial_update']:
      return serializers.ProjectCreateUpdateSerializer
    if self.action == 'manageable':
      return serializers.ProjectManageableSerializer
    if self.action == 'close':
      return EmptySerializer
    if self.action == 'bookmarked':
      return serializers.ProjectRetrieveSerializer
    if self.action == 'post':
      return post_serializers.PostCreateSerializer
    if self.action == 'post_patch_delete':
      return post_serializers.PostUpdateSerializer
    if self.action == 'retrieve':
      if ProjectRetrieveOwnsOrIsOrganizationMember().has_object_permission(self.request, None, self.get_object()):
        return serializers.ProjectManageableRetrieveSerializer
      else:
        return serializers.ProjectRetrieveSerializer

    return serializers.ProjectRetrieveSerializer
