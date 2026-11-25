from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import Http404
from django.urls import include, path

from accounts.views import home_redirect


# shortcut: temporary route for previewing 404.html locally; remove before production.
def test_404(request):
    raise Http404


urlpatterns = [
    path("", home_redirect, name="home"),
    path("test-404/", test_404),
    path("admin/", admin.site.urls),
    path("converter/", include("converter.urls")),
    path("", include("accounts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "django.views.defaults.page_not_found"
handler500 = 'django.views.defaults.server_error'

