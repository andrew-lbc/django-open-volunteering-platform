from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter, NestedDefaultRouter

from ovp.apps.projects import views

router = routers.DefaultRouter()
router.register(r'projects', views.ProjectResourceViewSet, 'project')
router.register(r'categories', views.CategoryResourceViewSet, 'category')

applies = NestedDefaultRouter(router, r'projects', lookup='project')
applies.register(r'applies', views.ApplyResourceViewSet, 'project-applies')

urlpatterns = [
  url(r'^', include(router.urls)),
  url(r'^', include(applies.urls)),
]