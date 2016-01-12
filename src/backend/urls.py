"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, patterns, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from backend.apps.ems.resources import EventViewSet
from backend.apps.crm.resources import AccountViewSet

admin.autodiscover()

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'accounts', AccountViewSet)


urlpatterns = patterns(

    (r'^api-auth/', include('rest_framework.urls',
                            namespace='rest_framework')),

    (r'^admin/', include(admin.site.urls)),
    (r'^api/v1/', include(router.urls, namespace='v1')),

    url('^social', include('social.apps.django_app.urls', namespace='social')),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
)
