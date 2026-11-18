from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.defaults import page_not_found

urlpatterns = [
    path("admin/", admin.site.urls),
    path("converter/", include("converter.urls")),
    path("", include("accounts.urls")),
    # temporary: call the handler directly so 404.html shows even with DEBUG=True
    path("test-404/", lambda request: page_not_found(request, None)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "django.views.defaults.page_not_found"

