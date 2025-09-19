"""
Django Views for skiutlån-systemet.

Views er funksjoner som håndterer HTTP-forespørsler og returnerer HTTP-respons.
Her implementerer vi alle hovedfunksjonene for vårt skiutlån-system.

Kjernekrav oppfylt:
- Opprette/legge til ✓ (create views)
- Lese/liste ✓ (list/detail views)
- Oppdatere ✓ (update views)
- Slette ✓ (delete views)
- Søk ✓ (search functionality)
- Brukerfgrensesnitt ✓ (web templates)
- Feilhåndtering ✓ (try/except og Django forms)

TODO for gruppen:
1. Implementer alle view-funksjonene
2. Legg til proper feilhåndtering
3. Implementer søkefunksjonalitet
4. Legg til validering i forms
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, date, timedelta

from .models import SkiItem, Bruker, Utlan
from .forms import SkiItemForm, BrukerForm, UtlanForm, SokForm


# ============================================================================
# HJEMSIDE / DASHBOARD VIEWS
# ============================================================================

def hjem(request):
    """
    Hovedside som viser oversikt over systemet.

    TODO for gruppen:
    1. Hent statistikk data (antall ski, brukere, aktive utlån)
    2. Hent nylige utlån
    3. Hent forsinket utlån
    4. Send data til template

    Eksempel på data å samle:
    - Totalt antall ski-items
    - Antall ledige items
    - Antall aktive utlån
    - Liste over forsinket utlån
    """

    # TODO: Implementer statistikk-innsamling
    context = {
        'totalt_ski_items': 0,  # TODO: SkiItem.objects.count()
        'ledige_items': 0,      # TODO: Tell ledige items
        'aktive_utlan': 0,      # TODO: Utlan.objects.filter(returnert_dato__isnull=True).count()
        'forsinket_utlan': [],  # TODO: Finn forsinket utlån
        'nylige_utlan': [],     # TODO: Utlan.objects.order_by('-utlant_dato')[:5]
    }

    return render(request, 'skiutlan/hjem.html', context)


# ============================================================================
# SKI-ITEM VIEWS (CRUD operasjoner)
# ============================================================================

def ski_item_liste(request):
    """
    Viser liste over alle ski-items med søk og filtreringsmuligheter.

    TODO for gruppen:
    1. Hent alle ski-items fra databasen
    2. Implementer søkefunksjonalitet
    3. Implementer filtrering på type og tilstand
    4. Legg til paginering hvis mange items

    Query parameters som kan brukes:
    - sok: søketekst
    - type: filter på ski-type
    - tilstand: filter på tilstand
    - ledig: vis bare ledige items
    """

    # Hent alle ski-items (standard)
    ski_items = SkiItem.objects.all()

    # TODO: Implementer søk
    sok_tekst = request.GET.get('sok', '')
    if sok_tekst:
        # TODO: Søk i navn og type_ski felt
        # Hint: ski_items = ski_items.filter(Q(navn__icontains=sok_tekst) | Q(type_ski__icontains=sok_tekst))
        pass

    # TODO: Implementer filtrering
    type_filter = request.GET.get('type', '')
    if type_filter:
        # TODO: Filtrer på type_ski
        pass

    tilstand_filter = request.GET.get('tilstand', '')
    if tilstand_filter:
        # TODO: Filtrer på tilstand
        pass

    # TODO: Filter på ledige items
    bare_ledige = request.GET.get('ledig', False)
    if bare_ledige:
        # TODO: Filtrer ut items som er utlånt
        # Hint: Sjekk for items uten aktive utlån
        pass

    context = {
        'ski_items': ski_items,
        'sok_tekst': sok_tekst,
        'type_filter': type_filter,
        'tilstand_filter': tilstand_filter,
        'bare_ledige': bare_ledige,
        'ski_types': SkiItem.SKI_TYPES,  # For dropdown i template
    }

    return render(request, 'skiutlan/ski_item_liste.html', context)


def ski_item_detalj(request, item_id):
    """
    Viser detaljert informasjon om et spesifikt ski-item.

    TODO for gruppen:
    1. Hent ski-item med get_object_or_404
    2. Hent utlånshistorikk for dette itemet
    3. Sjekk om itemet er ledig
    4. Implementer "Lån ut" funksjonalitet hvis ledig
    """

    # TODO: Hent item med feilhåndtering
    # ski_item = get_object_or_404(SkiItem, id=item_id)

    # TODO: Hent utlånshistorikk
    # utlan_historikk = ski_item.utlan_set.all().order_by('-utlant_dato')

    # TODO: Sjekk om ledig
    # er_ledig = ski_item.er_ledig

    context = {
        # 'ski_item': ski_item,
        # 'utlan_historikk': utlan_historikk,
        # 'er_ledig': er_ledig,
    }

    return render(request, 'skiutlan/ski_item_detalj.html', context)


def ski_item_opprett(request):
    """
    Oppretter nytt ski-item.

    TODO for gruppen:
    1. Hvis GET: vis tomt skjema
    2. Hvis POST: valider og lagre data
    3. Legg til success melding
    4. Redirect til item-liste eller detail-side

    Feilhåndtering:
    - Valider at størrelse er rimelig for ski-type
    - Sjekk at navn ikke er tomt
    - Håndter database-feil
    """

    if request.method == 'POST':
        # TODO: Behandle form data
        # form = SkiItemForm(request.POST)
        # if form.is_valid():
        #     try:
        #         ski_item = form.save()
        #         messages.success(request, f'Ski-item "{ski_item.navn}" ble opprettet!')
        #         return redirect('ski_item_detalj', item_id=ski_item.id)
        #     except Exception as e:
        #         messages.error(request, f'Feil ved lagring: {e}')
        pass
    else:
        # TODO: Opprett tomt skjema
        # form = SkiItemForm()
        pass

    context = {
        # 'form': form,
        'action': 'Opprett nytt ski-item'
    }

    return render(request, 'skiutlan/ski_item_form.html', context)


def ski_item_rediger(request, item_id):
    """
    Redigerer eksisterende ski-item.

    TODO for gruppen:
    1. Hent item med get_object_or_404
    2. Hvis GET: fyll skjema med eksisterende data
    3. Hvis POST: oppdater og lagre
    4. Håndter feil og vis meldinger
    """

    # TODO: Implementer redigering
    # ski_item = get_object_or_404(SkiItem, id=item_id)

    if request.method == 'POST':
        # TODO: Oppdater med form data
        pass
    else:
        # TODO: Fyll skjema med eksisterende data
        pass

    context = {
        # 'form': form,
        # 'ski_item': ski_item,
        'action': 'Rediger ski-item'
    }

    return render(request, 'skiutlan/ski_item_form.html', context)


def ski_item_slett(request, item_id):
    """
    Sletter ski-item (med bekreftelse).

    TODO for gruppen:
    1. Hent item med get_object_or_404
    2. Sjekk om item har aktive utlån (kan ikke slettes da)
    3. Hvis POST: slett og redirect
    4. Hvis GET: vis bekreftelsesside
    """

    # TODO: Implementer sletting med validering
    pass


# ============================================================================
# BRUKER VIEWS (CRUD operasjoner)
# ============================================================================

def bruker_liste(request):
    """
    Viser liste over alle brukere med søkefunksjonalitet.

    TODO for gruppen:
    1. Hent alle brukere
    2. Implementer søk på navn og telefon
    3. Sorter alfabetisk
    4. Vis antall aktive utlån per bruker
    """

    # TODO: Implementer bruker-liste
    pass


def bruker_detalj(request, bruker_id):
    """
    Viser detaljert informasjon om en bruker.

    TODO for gruppen:
    1. Hent bruker med get_object_or_404
    2. Hent alle utlån for denne brukeren
    3. Vis aktive og historiske utlån separat
    4. Legg til "Ny utlån" knapp
    """

    # TODO: Implementer bruker-detaljer
    pass


def bruker_opprett(request):
    """
    Oppretter ny bruker.

    TODO for gruppen:
    1. Bruk BrukerForm for validering
    2. Sjekk at telefonnummer er unikt
    3. Valider epost hvis oppgitt
    4. Lagre og vis success melding
    """

    # TODO: Implementer bruker-opprettelse
    pass


def bruker_rediger(request, bruker_id):
    """Redigerer eksisterende bruker."""
    # TODO: Implementer bruker-redigering
    pass


def bruker_slett(request, bruker_id):
    """Sletter bruker (hvis ingen aktive utlån)."""
    # TODO: Implementer bruker-sletting
    pass


# ============================================================================
# UTLÅN VIEWS (CRUD operasjoner)
# ============================================================================

def utlan_liste(request):
    """
    Viser liste over alle utlån med filtrering.

    TODO for gruppen:
    1. Hent alle utlån, sorter etter dato
    2. Implementer filtrering: aktive, returnerte, forsinket
    3. Implementer søk på bruker- og item-navn
    4. Vis status-badges (aktiv, forsinket, returnert)
    """

    # TODO: Implementer utlån-liste
    pass


def utlan_detalj(request, utlan_id):
    """
    Viser detaljert informasjon om et utlån.

    TODO for gruppen:
    1. Hent utlån med get_object_or_404
    2. Beregn varighet og om det er forsinket
    3. Hvis aktivt: vis "Marker som returnert" knapp
    4. Vis historie og kommentarer
    """

    # TODO: Implementer utlån-detaljer
    pass


def utlan_opprett(request):
    """
    Oppretter nytt utlån.

    TODO for gruppen:
    1. Bruk UtlanForm for validering
    2. Sjekk at ski-item er ledig
    3. Sjekk at bruker ikke har for mange aktive utlån
    4. Sett default planlagt_retur til 1 uke frem
    """

    # TODO: Implementer utlån-opprettelse
    pass


def utlan_opprett_for_item(request, item_id):
    """
    Oppretter utlån for et spesifikt ski-item.

    TODO for gruppen:
    1. Hent item med get_object_or_404
    2. Sjekk at det er ledig
    3. Pre-fyll skjema med item
    4. Resten som utlan_opprett()
    """

    # TODO: Implementer item-spesifikt utlån
    pass


def utlan_marker_returnert(request, utlan_id):
    """
    Markerer et utlån som returnert.

    TODO for gruppen:
    1. Hent utlån med get_object_or_404
    2. Sjekk at det er aktivt
    3. Sett returnert_dato til nå
    4. Lagre og vis success melding
    """

    # TODO: Implementer retur-funksjonalitet
    pass


# ============================================================================
# SØK OG RAPPORTER
# ============================================================================

def avansert_sok(request):
    """
    Avansert søkeside med kombinerte filtre.

    TODO for gruppen:
    1. Lag skjema med søkekriterier
    2. Søk på tvers av alle modeller
    3. Returner resultater i kategorier
    4. Implementer "lagrede søk"
    """

    # TODO: Implementer avansert søk
    pass


def rapporter(request):
    """
    Viser rapporter og statistikk.

    TODO for gruppen:
    1. Mest populære ski-items
    2. Mest aktive brukere
    3. Gjennomsnittlig utlånstid
    4. Forsinket statistikk
    5. Månedlige/årlige trender
    """

    # TODO: Implementer rapporter
    pass


# ============================================================================
# API ENDPOINTS (for AJAX kall)
# ============================================================================

def api_ski_item_tilgjengelighet(request, item_id):
    """
    API endpoint som returnerer om et ski-item er ledig.

    TODO for gruppen:
    1. Hent item
    2. Sjekk tilgjengelighet
    3. Returner JSON respons
    """

    try:
        # TODO: Implementer API kall
        # ski_item = get_object_or_404(SkiItem, id=item_id)
        # return JsonResponse({
        #     'ledig': ski_item.er_ledig,
        #     'navn': ski_item.navn
        # })
        pass
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def api_sok_brukere(request):
    """
    API endpoint for å søke brukere (brukt i autocomplete).

    TODO for gruppen:
    1. Hent søketekst fra GET parameter
    2. Søk i fornavn, etternavn, telefon
    3. Returner liste med matchende brukere
    """

    # TODO: Implementer bruker-søk API
    pass


# ============================================================================
# HJELPEFUNKSJONER
# ============================================================================

def generer_rapport_data():
    """
    Hjelpefunksjon som genererer data for rapporter.

    TODO for gruppen:
    1. Samle statistikk fra databasen
    2. Beregn nøkkeltall
    3. Returner strukturert data
    """

    # TODO: Implementer rapport-generering
    pass
