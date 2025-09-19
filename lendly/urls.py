"""
Hovedprosjekt URL konfiguration for lendly (skiutlån-systemet).

TODO for gruppen:
1. Test at alle URLs fungerer
2. Vurder å legge til custom error pages (404, 500)
3. Legg til static files serving for development
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin panel - bruk dette for dataadministrasjon
    path('admin/', admin.site.urls),

    # Inkluder alle app URLs - hovedsystemet starter på root
    path('', include('skiutlan.urls')),

    # TODO for gruppen: Legg til flere URL patterns hvis nødvendig
    # path('api/', include('skiutlan.api_urls')),  # Hvis dere lager separat API
    # path('docs/', include('django.contrib.admindocs.urls')),  # Auto-dokumentasjon
]

# TODO for gruppen: Legg til static files serving for development
# from django.conf import settings
# from django.conf.urls.static import static
#
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
