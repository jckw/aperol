from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from django.conf.urls.static import static
from django.conf import settings
from server.schema import schema

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^graphql', csrf_exempt(GraphQLView.as_view(graphiql=True,
                                                     schema=schema))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Not suitable for production!
# See https://docs.djangoproject.com/en/2.1/howto/static-files/deployment/
