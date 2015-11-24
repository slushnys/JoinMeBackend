from django.conf.urls import url, include, patterns
from rest_framework.routers import DefaultRouter
from backend.apps.ems import resources

router = DefaultRouter()
router.register(r'events', resources.EventViewSet)

urlpatterns = patterns('',
                       url(r'^ems/', include(router.urls, namespace='v1')),
                       )
