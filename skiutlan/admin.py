
from django.contrib import admin
from .models import SkiItem, Bruker, Utlan
from django.utils import timezone


# Custom filter for å vise aktive/returnerte utlån
class AktiveFilter(admin.SimpleListFilter):
    title = 'Status'
    parameter_name = 'aktiv'

    def lookups(self, request, model_admin):
        return [
            ('ja', 'Kun aktive utlån'),
            ('nei', 'Kun returnerte utlån'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'ja':
            return queryset.filter(returnert_dato__isnull=True)
        if self.value() == 'nei':
            return queryset.filter(returnert_dato__isnull=False)
        return queryset


@admin.register(SkiItem)
class SkiItemAdmin(admin.ModelAdmin):

    # Hvilke felt som vises i listen over ski-items
    list_display = ['navn', 'type_ski', 'storrelse', 'tilstand', 'er_ledig']

    # Hvilke felt du kan søke på
    search_fields = ['navn', 'type_ski']

    # Hvilke felt du kan filtrere på (høyre side i admin)
    list_filter = ['type_ski', 'tilstand']

    # Felt som ikke kan redigeres
    readonly_fields = ['opprettet', 'oppdatert']

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
    """

    list_display = ['fornavn', 'etternavn', 'telefon', 'epost', 'aktive_utlan']
    search_fields = ['fornavn', 'etternavn', 'telefon']
    list_filter = ['registrert']
    readonly_fields = ['registrert']

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
    """

    list_display = ['bruker', 'ski_item', 'utlant_dato', 'planlagt_retur', 'er_aktivt', 'er_forsinket']
    search_fields = ['bruker__fornavn', 'bruker__etternavn', 'ski_item__navn']
    list_filter = [AktiveFilter, 'utlant_dato', 'planlagt_retur', 'returnert_dato']
    readonly_fields = ['utlant_dato', 'varighet']
    ordering = ['-utlant_dato']

    # Organiser feltene
    fieldsets = (
        ('Utlånsinformasjon', {
            'fields': ('bruker', 'ski_item')
        }),
        ('Datoer', {
            'fields': ('utlant_dato', 'planlagt_retur', 'returnert_dato')
        }),
    )

    # Custom action for å markere utlån som returnert
    actions = ['marker_som_returnert']

    def marker_som_returnert(self, request, queryset):
        """
        Marker valgte utlån som returnert.
        """
        updated = queryset.update(returnert_dato=timezone.now())
        self.message_user(request, f"{updated} utlån ble markert som returnert.")

    marker_som_returnert.short_description = "Marker valgte utlån som returnert"



# TODO for gruppen: Vurder å lage inline-views
# class UtlanInline(admin.TabularInline):
#     """Viser utlån direkte i bruker eller ski-item admin."""
#     model = Utlan
#     extra = 0  # Ikke vis tomme skjemaer
#     readonly_fields = ['opprettet']
