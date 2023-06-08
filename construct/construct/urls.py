from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from dashboard import views


schema_view = get_schema_view(
    openapi.Info(
        title="Swagger",
        default_version="v1",
        description="Swagger API requests AutoDocumentation",
        # terms_of_service=path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
        contact=openapi.Contact(email="quasar360@mail.ru"),
        license=openapi.License(name="License"),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls"), name="dashboard"),
    path("api/", include("api.urls"), name="api"),
    path("cart/", include("cart.urls"), name="cart"),
    path("shop/", include("shop.urls"), name="shop"),
    path("news/", include("news.urls"), name="news"),
    path("crm/", include("crm.urls"), name="crm"),
    path("sharp-draft/", include("sharp_draft.urls"), name="sharp_draft"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
