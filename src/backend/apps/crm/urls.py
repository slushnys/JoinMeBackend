from django.conf.urls import url, include, patterns
from rest_framework.routers import DefaultRouter
from backend.apps.crm import resources

router = DefaultRouter()
router.register(r'accounts', resources.AccountViewSet)

urlpatterns = patterns('',
    url(r'^crm/', include(router.urls, namespace='v1')),
                       )