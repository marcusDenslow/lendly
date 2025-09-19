"""
URL konfigurasjon for skiutlån-systemet.

Denne filen definerer alle URL-ruter for applikasjonen.
URL-mønstre følger RESTful prinsipper for konsistens.

URL-struktur:
- / - Hjemside
- /ski/ - Ski-item operasjoner
- /brukere/ - Bruker operasjoner
- /utlan/ - Utlån operasjoner
- /sok/ - Søkefunksjonalitet
- /rapporter/ - Rapporter og statistikk
- /api/ - API endpoints

TODO for gruppen:
1. Teste alle URL-er etter implementering
2. Legg til URL-navngivning for enkelt reverse lookup
3. Vurder å gruppere relaterte URLs
4. Implementer URL-parametere validering
"""

from django.urls import path
from . import views

# Namespace for denne app-en
app_name = 'skiutlan'

urlpatterns = [
    # ========================================================================
    # HJEMSIDE / DASHBOARD
    # ========================================================================
    path('', views.hjem, name='hjem'),

    # ========================================================================
    # SKI-ITEM URLs (CRUD operasjoner)
    # ========================================================================

    # Liste og søk
    path('ski/', views.ski_item_liste, name='ski_item_liste'),

    # Detail view
    path('ski/<int:item_id>/', views.ski_item_detalj, name='ski_item_detalj'),

    # Create, Update, Delete
    path('ski/ny/', views.ski_item_opprett, name='ski_item_opprett'),
    path('ski/<int:item_id>/rediger/', views.ski_item_rediger, name='ski_item_rediger'),
    path('ski/<int:item_id>/slett/', views.ski_item_slett, name='ski_item_slett'),

    # TODO for gruppen: Legg til flere ski-item URLs
    # path('ski/<int:item_id>/historikk/', views.ski_item_historikk, name='ski_item_historikk'),
    # path('ski/<int:item_id>/qr/', views.ski_item_qr_kode, name='ski_item_qr'),

    # ========================================================================
    # BRUKER URLs (CRUD operasjoner)
    # ========================================================================

    # Liste og søk
    path('brukere/', views.bruker_liste, name='bruker_liste'),

    # Detail view
    path('brukere/<int:bruker_id>/', views.bruker_detalj, name='bruker_detalj'),

    # Create, Update, Delete
    path('brukere/ny/', views.bruker_opprett, name='bruker_opprett'),
    path('brukere/<int:bruker_id>/rediger/', views.bruker_rediger, name='bruker_rediger'),
    path('brukere/<int:bruker_id>/slett/', views.bruker_slett, name='bruker_slett'),

    # TODO for gruppen: Legg til bruker-spesifikke URLs
    # path('brukere/<int:bruker_id>/utlan/', views.bruker_utlan_liste, name='bruker_utlan'),
    # path('brukere/<int:bruker_id>/statistikk/', views.bruker_statistikk, name='bruker_statistikk'),

    # ========================================================================
    # UTLÅN URLs (CRUD operasjoner)
    # ========================================================================

    # Liste og søk
    path('utlan/', views.utlan_liste, name='utlan_liste'),

    # Detail view
    path('utlan/<int:utlan_id>/', views.utlan_detalj, name='utlan_detalj'),

    # Create - generelt og spesifikt for item
    path('utlan/ny/', views.utlan_opprett, name='utlan_opprett'),
    path('utlan/ny/<int:item_id>/', views.utlan_opprett_for_item, name='utlan_opprett_for_item'),

    # Special actions
    path('utlan/<int:utlan_id>/returner/', views.utlan_marker_returnert, name='utlan_marker_returnert'),

    # TODO for gruppen: Legg til flere utlån URLs
    # path('utlan/<int:utlan_id>/forleng/', views.utlan_forleng, name='utlan_forleng'),
    # path('utlan/<int:utlan_id>/rediger/', views.utlan_rediger, name='utlan_rediger'),
    # path('utlan/aktive/', views.utlan_aktive, name='utlan_aktive'),
    # path('utlan/forsinket/', views.utlan_forsinket, name='utlan_forsinket'),

    # ========================================================================
    # SØK og FILTRERING
    # ========================================================================

    path('sok/', views.avansert_sok, name='avansert_sok'),

    # TODO for gruppen: Legg til spesialiserte søk
    # path('sok/hurtig/', views.hurtig_sok, name='hurtig_sok'),
    # path('sok/lagret/', views.lagret_sok, name='lagret_sok'),

    # ========================================================================
    # RAPPORTER og STATISTIKK
    # ========================================================================

    path('rapporter/', views.rapporter, name='rapporter'),

    # TODO for gruppen: Legg til spesifikke rapporter
    # path('rapporter/populaere/', views.rapport_populaere_items, name='rapport_populaere'),
    # path('rapporter/brukere/', views.rapport_bruker_aktivitet, name='rapport_brukere'),
    # path('rapporter/utlan/', views.rapport_utlan_statistikk, name='rapport_utlan'),
    # path('rapporter/eksport/', views.rapport_eksport, name='rapport_eksport'),

    # ========================================================================
    # API ENDPOINTS (for AJAX og eksterne kall)
    # ========================================================================

    # API base path
    path('api/ski/<int:item_id>/tilgjengelighet/',
         views.api_ski_item_tilgjengelighet,
         name='api_ski_item_tilgjengelighet'),

    path('api/brukere/sok/', views.api_sok_brukere, name='api_sok_brukere'),

    # TODO for gruppen: Legg til flere API endpoints
    # path('api/utlan/aktive/', views.api_utlan_aktive, name='api_utlan_aktive'),
    # path('api/statistikk/', views.api_statistikk, name='api_statistikk'),
    # path('api/validering/telefon/', views.api_valider_telefon, name='api_valider_telefon'),

    # ========================================================================
    # UTILITY URLs
    # ========================================================================

    # TODO for gruppen: Legg til nyttige utility URLs
    # path('export/ski/', views.eksporter_ski_liste, name='eksporter_ski'),
    # path('import/ski/', views.importer_ski_data, name='importer_ski'),
    # path('backup/', views.backup_data, name='backup_data'),
    # path('qr/<int:item_id>/', views.generer_qr_kode, name='qr_kode'),
]

# TODO for gruppen: Vurder å organisere URLs i include-strukturer
# For eksempel:
#
# from django.urls import include
#
# # I hovedprosjektets urls.py:
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('skiutlan.urls')),
#     path('api/v1/', include('skiutlan.api_urls')),
# ]

"""
EKSEMPLER på hvordan URLs brukes i templates og views:

I templates:
{% url 'skiutlan:ski_item_detalj' item.id %}
{% url 'skiutlan:hjem' %}

I views:
from django.urls import reverse
redirect(reverse('skiutlan:ski_item_liste'))

Med parametere:
reverse('skiutlan:ski_item_detalj', args=[item.id])
reverse('skiutlan:ski_item_detalj', kwargs={'item_id': item.id})
"""