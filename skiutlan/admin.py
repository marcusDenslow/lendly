"""
Django Admin konfiguration for skiutlån-systemet.

Her registrerer vi modellene våre så de blir tilgjengelige i Django admin-panelet.
Admin-panelet er en ferdig webside som lar oss administrere data enkelt.

For å bruke admin-panelet:
1. Kjør: python manage.py createsuperuser
2. Start serveren: python manage.py runserver
3. Gå til http://127.0.0.1:8000/admin/
4. Logg inn med superuser-kontoen

TODO for gruppen:
1. Tilpass list_display for bedre oversikt
2. Legg til search_fields for søkefunksjonalitet
3. Legg til list_filter for filtrering
4. Vurder å lage custom admin actions
"""

from django.contrib import admin
from .models import SkiItem, Bruker, Utlan


@admin.register(SkiItem)
class SkiItemAdmin(admin.ModelAdmin):
    """
    Admin-konfigurasjon for SkiItem modellen.

    TODO for gruppen:
    1. Fyll inn list_display med relevante felt som vises i listen
    2. Legg til search_fields for å søke på navn og type
    3. Legg til list_filter for filtrering på type og tilstand
    4. Vurder readonly_fields for automatiske datoer
    """

    # Hvilke felt som vises i listen over ski-items
    list_display = []  # TODO: Fyll inn med f.eks ['navn', 'type_ski', 'storrelse', 'tilstand', 'er_ledig']

    # Hvilke felt du kan søke på
    search_fields = []  # TODO: Fyll inn med f.eks ['navn', 'type_ski']

    # Hvilke felt du kan filtrere på (høyre side i admin)
    list_filter = []  # TODO: Fyll inn med f.eks ['type_ski', 'tilstand', 'opprettet']

    # Felt som ikke kan redigeres
    readonly_fields = []  # TODO: Vurder å legge til ['opprettet', 'oppdatert']

    # Organiser feltene i fieldsets for bedre layout
    fieldsets = (
        ('Grunnleggende informasjon', {
            'fields': ('navn', 'type_ski', 'storrelse')
        }),
        ('Status', {
            'fields': ('tilstand',)
        }),
        # TODO: Legg til en 'Metadata' seksjon med datoer
    )


@admin.register(Bruker)
class BrukerAdmin(admin.ModelAdmin):
    """
    Admin-konfigurasjon for Bruker modellen.

    TODO for gruppen:
    1. Konfigurer list_display for å vise viktig brukerinformasjon
    2. Legg til søkefunksjonalitet på navn og telefon
    3. Vurder å vise antall aktive utlån i listen
    """

    list_display = []  # TODO: Fyll inn med f.eks ['fullt_navn', 'telefon', 'epost', 'aktive_utlan']
    search_fields = []  # TODO: Fyll inn med f.eks ['fornavn', 'etternavn', 'telefon']
    list_filter = []  # TODO: Vurder datoer som ['registrert']
    readonly_fields = []  # TODO: Vurder ['registrert']

    # Organiser feltene
    fieldsets = (
        ('Personopplysninger', {
            'fields': ('fornavn', 'etternavn', 'telefon', 'epost')
        }),
        # TODO: Legg til metadata seksjon
    )


@admin.register(Utlan)
class UtlanAdmin(admin.ModelAdmin):
    """
    Admin-konfigurasjon for Utlan modellen.

    TODO for gruppen:
    1. Vis viktig utlånsinformasjon i listen
    2. Legg til filtrering på status (aktiv/returnert)
    3. Legg til datofiltrering
    4. Vurder å lage en custom action for å markere som returnert
    """

    list_display = []  # TODO: f.eks ['bruker', 'ski_item', 'utlant_dato', 'planlagt_retur', 'er_aktivt', 'er_forsinket']
    search_fields = []  # TODO: f.eks ['bruker__fornavn', 'bruker__etternavn', 'ski_item__navn']
    list_filter = []  # TODO: f.eks ['utlant_dato', 'planlagt_retur', 'returnert_dato']
    readonly_fields = []  # TODO: f.eks ['opprettet', 'varighet']

    # Sortering - nyeste først
    ordering = ['-utlant_dato']

    # Organiser feltene
    fieldsets = (
        ('Utlånsinformasjon', {
            'fields': ('bruker', 'ski_item')
        }),
        ('Datoer', {
            'fields': ('utlant_dato', 'planlagt_retur', 'returnert_dato')
        }),
        # TODO: Legg til metadata seksjon
    )

    # TODO: Implementer custom actions
    # actions = ['marker_som_returnert']

    def marker_som_returnert(self, request, queryset):
        """
        Custom admin action for å markere utlån som returnert.

        TODO for gruppen:
        1. Iterer gjennom queryset (valgte utlån)
        2. Sett returnert_dato til timezone.now() for hvert utlån
        3. Lagre endringene
        4. Vis en success-melding

        Hint:
        from django.utils import timezone
        from django.contrib import messages
        """
        pass

    marker_som_returnert.short_description = "Marker valgte utlån som returnert"


# TODO for gruppen: Vurder å lage inline-views
# class UtlanInline(admin.TabularInline):
#     """Viser utlån direkte i bruker eller ski-item admin."""
#     model = Utlan
#     extra = 0  # Ikke vis tomme skjemaer
#     readonly_fields = ['opprettet']
