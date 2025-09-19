import re
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
    context = {
        'totalt_ski_items': SkiItem.objects.count(),
        'ledige_items': SkiItem.objects.exclude(id__in=Utlan.objects.filter(returnert_dato__isnull=True).values_list('ski_item_id', flat=True)).count(),
        'aktive_utlan': Utlan.objects.filter(returnert_dato__isnull=True).count(),
        'forsinket_utlan': Utlan.objects.filter(returnert_dato__isnull=True, planlagt_retur__lt=date.today())[:5],
        'nylige_utlan': Utlan.objects.order_by('-utlant_dato')[:5],
    }

    return render(request, 'skiutlan/hjem.html', context)


# ============================================================================
# SKI-ITEM VIEWS (CRUD operasjoner)
# ============================================================================

def ski_item_liste(request):
    # Hent alle ski-items (standard)
    ski_items = SkiItem.objects.all()

    sok_tekst = request.GET.get('sok', '')
    if sok_tekst:
        ski_items = ski_items.filter(
            Q(navn__icontains=sok_tekst) | Q(type_ski__icontains=sok_tekst))

    type_filter = request.GET.get('type', '')
    if type_filter:
        ski_items = ski_items.filter(type_ski=type_filter)

    tilstand_filter = request.GET.get('tilstand', '')
    if tilstand_filter:
        ski_items = ski_items.filter(tilstand=tilstand_filter)

    bare_ledige = request.GET.get('ledig', False)
    if bare_ledige:
        utlante_item_ids = Utlan.objects.filter(
            returnert_dato__isnull=True).values_list('ski_item_id', flat=True)
        ski_items = ski_items.exclude(id__in=utlante_item_ids)

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
    ski_item = get_object_or_404(SkiItem, id=item_id)
    utlan_historikk = ski_item.utlan_set.all().order_by('-utlant_dato')
    er_ledig = ski_item.er_ledig

    context = {
        'ski_item': ski_item,
        'utlan_historikk': utlan_historikk,
        'er_ledig': er_ledig,
    }

    return render(request, 'skiutlan/ski_item_detalj.html', context)


def ski_item_opprett(request):
    if request.method == 'POST':
        form = SkiItemForm(request.POST)
        if form.is_valid():
            try:
                ski_item = form.save()
                messages.success(
                    request, f'Ski-item "{ski_item.navn}" ble opprettet!')
                return redirect('skiutlan:ski_item_detalj', item_id=ski_item.id)
            except Exception as e:
                messages.error(request, f'Feil ved lagring: {e}')
    else:
        form = SkiItemForm()

    context = {
        'form': form,
        'action': 'Opprett nytt ski-item'
    }

    return render(request, 'skiutlan/ski_item_form.html', context)


def ski_item_rediger(request, item_id):
    ski_item = get_object_or_404(SkiItem, id=item_id)

    if request.method == 'POST':
        form = SkiItemForm(request.POST, instance=ski_item)
        if form.is_valid():
            try:
                ski_item = form.save()
                messages.success(request, f'Ski-item "{ski_item.navn}" ble oppdatert!')
                return redirect('skiutlan:ski_item_detalj', item_id=ski_item.id)
            except Exception as e:
                messages.error(request, f'Feil ved lagring: {e}')
    else:
        form = SkiItemForm(instance=ski_item)

    context = {
        'form': form,
        'ski_item': ski_item,
        'action': 'Rediger ski-item'
    }

    return render(request, 'skiutlan/ski_item_form.html', context)


def ski_item_slett(request, item_id):
    ski_item = get_object_or_404(SkiItem, id=item_id)
    aktive_utlan = Utlan.objects.filter(
        ski_item=ski_item, returnert_dato__isnull=True)
    if aktive_utlan.exists():
        messages.error(request, f'Kan ikke slette: "{ski_item.navn}" - er i aktiv utlån!')
        return redirect('skiutlan:ski_item_detalj', item_id=item_id)

    if request.method == 'POST':
        navn = ski_item.navn
        ski_item.delete()
        messages.success(request, f'Ski-item "{navn}" ble slettet!')
        return redirect('skiutlan:ski_item_liste')

    context = {
        'ski_item': ski_item,
        'aktive_utlan': aktive_utlan
    }

    return render(request, 'skiutlan/ski_item_slett_bekreft.html', context)


# ============================================================================
# BRUKER VIEWS (CRUD operasjoner)
# ============================================================================

def bruker_liste(request):
    brukere = Bruker.objects.all()
    sok_tekst = request.GET.get('sok', '')
    if sok_tekst:
        brukere = brukere.filter(
            Q(fornavn__icontains=sok_tekst) |
            Q(etternavn__icontains=sok_tekst) |
            Q(telefon__icontains=sok_tekst)
        )

    brukere = brukere.order_by('etternavn', 'fornavn')

    context = {
        'brukere': brukere,
        'sok_tekst': sok_tekst
    }
    return render(request, 'skiutlan/bruker_liste.html', context)


def bruker_detalj(request, bruker_id):
    bruker = get_object_or_404(Bruker, id=bruker_id)
    alle_utlan = Utlan.objects.filter(bruker=bruker).order_by('-utlant_dato')
    aktive_utlan = alle_utlan.filter(returnert_dato__isnull=True)
    utlan_historie = alle_utlan.filter(returnert_dato__isnull=False)

    context = {
        'bruker': bruker,
        'aktive_utlan': aktive_utlan,
        'utlan_historie': utlan_historie,
        'antall_aktive': aktive_utlan.count()
    }

    return render(request, 'skiutlan/bruker_detalj.html', context)


def bruker_opprett(request):
    if request.method == 'POST':
        form = BrukerForm(request.POST)
        if form.is_valid():
            try:
                bruker = form.save()
                messages.success(request, f'Bruker "{bruker.fullt_navn}" ble opprettet!')
                return redirect('skiutlan:bruker_detalj', bruker_id=bruker.id)
            except Exception as e:
                messages.error(request, f'Feil ved lagring: {e}')
    else:
        form = BrukerForm()

    context = {
        'form': form,
        'action': 'Opprett ny bruker'
    }
    return render(request, 'skiutlan/bruker_form.html', context)


def bruker_rediger(request, bruker_id):
    bruker = get_object_or_404(Bruker, id=bruker_id)

    if request.method == 'POST':
        form = BrukerForm(request.POST, instance=bruker)
        if form.is_valid():
            try:
                bruker = form.save()
                messages.success(request, f'Bruker "{bruker.fullt_navn}" ble oppdatert!')
                return redirect('skiutlan:bruker_detalj', bruker_id=bruker.id)
            except Exception as e:
                messages.error(request, f'Feil ved lagring: {e}')
    else:
        form = BrukerForm(instance=bruker)

    context = {
        'form': form,
        'bruker': bruker,
        'action': 'Rediger bruker'
    }

    return render(request, 'skiutlan/bruker_form.html', context)


def bruker_slett(request, bruker_id):
    bruker = get_object_or_404(Bruker, id=bruker_id)

    # sjekk om brukeren har aktive utlån
    aktive_utlan = Utlan.objects.filter(
        bruker=bruker, returnert_dato__isnull=True)
    if aktive_utlan.exists():
        messages.error(request, f'Kan ikke slette "{bruker.fullt_navn}" - har aktive utlån!')
        return redirect('skiutlan:bruker_detalj', bruker_id=bruker_id)

    if request.method == 'POST':
        navn = bruker.fullt_navn
        bruker.delete()
        messages.success(request, f'Bruker "{navn}" ble slettet!')
        return redirect('skiutlan:bruker_liste')

    context = {
        'bruker': bruker,
        'aktive_utlan': aktive_utlan
    }
    return render(request, 'skiutlan/bruker_slett_bekreft.html', context)


# ============================================================================
# UTLÅN VIEWS (CRUD operasjoner)
# ============================================================================

def utlan_liste(request):
    utlan = Utlan.objects.all().order_by('-utlant_dato')
    print(f"DEBUG utlan_liste: Totalt {utlan.count()} utlån i databasen")

    # Filtrering
    status_filter = request.GET.get('status', '')
    if status_filter == 'aktive':
        utlan = utlan.filter(returnert_dato__isnull=True)
    elif status_filter == 'returnerte':
        utlan = utlan.filter(returnert_dato__isnull=False)
    elif status_filter == 'forsinket':
        utlan = utlan.filter(returnert_dato__isnull=True, planlagt_retur__lt=date.today())

    # Søk
    sok_tekst = request.GET.get('sok', '')
    if sok_tekst:
        utlan = utlan.filter(
            Q(bruker__fornavn__icontains=sok_tekst) |
            Q(bruker__etternavn__icontains=sok_tekst) |
            Q(ski_item__navn__icontains=sok_tekst)
        )

    print(f"DEBUG utlan_liste: Etter filtrering {utlan.count()} utlån")
    for u in utlan:
        print(f"  - {u}")

    context = {
        'utlan': utlan,
        'sok_tekst': sok_tekst,
        'status_filter': status_filter,
    }

    return render(request, 'skiutlan/utlan_liste.html', context)


def utlan_detalj(request, utlan_id):
    utlan = get_object_or_404(Utlan, id=utlan_id)

    context = {
        'utlan': utlan,
    }

    return render(request, 'skiutlan/utlan_detalj.html', context)


def utlan_opprett(request):
    if request.method == 'POST':
        form = UtlanForm(request.POST)
        if form.is_valid():
            try:
                utlan = form.save()
                messages.success(request, 'Utlån opprettet!')
                return redirect('skiutlan:utlan_detalj', utlan_id=utlan.id)
            except Exception as e:
                messages.error(request, f'Feil ved lagring: {e}')
    else:
        form = UtlanForm()

    context = {
        'form': form,
        'action': 'Opprett nytt utlån'
    }

    return render(request, 'skiutlan/utlan_form.html', context)


def utlan_opprett_for_item(request, item_id):
    ski_item = get_object_or_404(SkiItem, id=item_id)

    if request.method == 'POST':
        try:
            # Hent data direkte fra POST uten form-validering
            bruker_id = request.POST.get('bruker')
            planlagt_retur = request.POST.get('planlagt_retur')

            print(f"DEBUG POST data: bruker_id={bruker_id}, planlagt_retur={planlagt_retur}, ski_item_id={ski_item.id}")

            if not bruker_id or not planlagt_retur:
                messages.error(request, 'Alle felt må fylles ut.')
                return redirect('skiutlan:ski_item_detalj', item_id=ski_item.id)

            bruker = Bruker.objects.get(id=bruker_id)
            print(f"DEBUG: Bruker funnet: {bruker}")

            # Konverter dato-string til datetime.date
            from datetime import datetime
            planlagt_retur_date = datetime.strptime(planlagt_retur, '%Y-%m-%d').date()
            print(f"DEBUG: Dato konvertert til: {planlagt_retur_date}")

            # Sjekk om ski_item allerede er utlånt
            eksisterende_utlan = Utlan.objects.filter(ski_item=ski_item, returnert_dato__isnull=True)
            if eksisterende_utlan.exists():
                existing = eksisterende_utlan.first()
                messages.error(request, f'{ski_item.navn} er allerede lånt ut til {existing.bruker.fornavn} {existing.bruker.etternavn}!')
                return redirect('skiutlan:ski_item_detalj', item_id=ski_item.id)

            # Lag utlån direkte
            print(f"DEBUG: Lager utlån med bruker={bruker}, ski_item={ski_item}, planlagt_retur={planlagt_retur_date}")

            from django.db import transaction
            with transaction.atomic():
                utlan = Utlan(
                    bruker=bruker,
                    ski_item=ski_item,
                    planlagt_retur=planlagt_retur_date
                )

                # Eksplisitt sett utlant_dato
                from django.utils import timezone
                utlan.utlant_dato = timezone.now()

                print(f"DEBUG: Før save - alle felter: bruker={utlan.bruker}, ski_item={utlan.ski_item}, planlagt_retur={utlan.planlagt_retur}, utlant_dato={utlan.utlant_dato}")

                try:
                    utlan.save()
                    print(f"DEBUG: Save() fullført - ID: {utlan.id}")
                except Exception as save_error:
                    print(f"DEBUG: Save() feilet: {save_error}")
                    raise

                if utlan.id:
                    # Test at den faktisk er i databasen
                    test_utlan = Utlan.objects.filter(id=utlan.id).first()
                    print(f"DEBUG: Test query fra DB: {test_utlan}")
                else:
                    print(f"DEBUG: Utlån ble 'lagret' men har ingen ID - dette er et database-problem")

            print(f"DEBUG: Final utlån objekt: {utlan}")
            messages.success(request, f'Utlån opprettet! {ski_item.navn} er nå lånt ut til {bruker.fornavn}.')
            return redirect('skiutlan:utlan_liste')

        except Exception as e:
            import traceback
            print(f"DEBUG: Exception occurred: {e}")
            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            messages.error(request, f'Feil ved lagring: {e}')
            return redirect('skiutlan:ski_item_detalj', item_id=ski_item.id)

    # Lag form og inkluder ski_item i queryset
    form = UtlanForm()
    # Sørg for at ski_item er i queryset
    form.fields['ski_item'].queryset = SkiItem.objects.filter(id=ski_item.id)
    form.fields['ski_item'].initial = ski_item

    context = {
        'form': form,
        'ski_item': ski_item,
        'action': f'Lån ut {ski_item.navn}'
    }

    return render(request, 'skiutlan/utlan_form.html', context)


def utlan_marker_returnert(request, utlan_id):
    utlan = get_object_or_404(Utlan, id=utlan_id)

    if utlan.returnert_dato:
        messages.warning(request, 'Utlån er allerede returnert!')
        return redirect('skiutlan:utlan_detalj', utlan_id=utlan_id)

    if request.method == 'POST':
        utlan.returnert_dato = timezone.now()
        utlan.save()
        messages.success(request, 'Utlån markert som returnert!')
        return redirect('skiutlan:utlan_detalj', utlan_id=utlan_id)

    context = {
        'utlan': utlan,
    }

    return render(request, 'skiutlan/utlan_returner_bekreft.html', context)


# ============================================================================
# SØK OG RAPPORTER
# ============================================================================

def avansert_sok(request):
    sok_tekst = request.GET.get('sok_tekst', '').strip()
    ski_type = request.GET.get('ski_type', '')
    tilstand = request.GET.get('tilstand', '')
    utlan_status = request.GET.get('utlan_status', '')
    dato_fra = request.GET.get('dato_fra', '')
    dato_til = request.GET.get('dato_til', '')

    ski_items = []
    brukere = []
    utlan = []

    #bare om det er noe som blir søkt
    if any([sok_tekst, ski_type, tilstand, utlan_status, dato_fra, dato_til]):

        # søk i ski-items
        ski_items_qs = SkiItem.objects.all()
        if sok_tekst:
            ski_items_qs = ski_items_qs.filter(
                Q(navn__icontains=sok_tekst) |
                Q(type_ski__icontains=sok_tekst)
            )
        if ski_type:
            ski_items_qs = ski_items_qs.filter(type_ski=ski_type)
        if tilstand:
            ski_items_qs = ski_items_qs.filter(tilstand=tilstand)
        ski_items = ski_items_qs[:20]

        
        # søk i brukere
        if sok_tekst:
            brukere = Bruker.objects.filter(
                Q(fornavn__icontains=sok_tekst) |
                Q(etternavn__icontains=sok_tekst) |
                Q(telefon__icontains=sok_tekst) | 
                Q(epost__icontains=sok_tekst)
            )[:20]

        # søk i utlan
        utlan_qs = Utlan.objects.all()
        if sok_tekst:
            utlan_qs = utlan_qs.filter(
                Q(bruker__fornavn__icontains=sok_tekst) |
                Q(bruker__etternavn__icontains=sok_tekst) |
                Q(ski_item__navn__icontains=sok_tekst)
            )
        if utlan_status == 'aktive':
            utlan_qs = utlan_qs.filter(returnert_dato__isnull=True)
        elif utlan_status == 'returnerte':
            utlan_qs = utlan_qs.filter(returnert_dato__isnull=False)
        elif utlan_status == 'forsinket':
            from datetime import date
            utlan_qs = utlan_qs.filter(returnert_dato__isnull=True, planlagt_retur__lt=date.today())

        # Dato filtrering
        if dato_fra:
            from datetime import datetime
            dato_fra_obj = datetime.strptime(dato_fra, '%Y-%m-%d').date()
            utlan_qs = utlan_qs.filter(utlant_dato__date__gte=dato_fra_obj)
        if dato_til:
            from datetime import datetime
            dato_til_obj = datetime.strptime(dato_til, '%Y-%m-%d').date()
            utlan_qs = utlan_qs.filter(utlant_dato__date__lte=dato_til_obj)

        utlan = utlan_qs.order_by('returnert_dato', '-utlant_dato')[:20]


    context = {
        'ski_items': ski_items,
        'brukere': brukere,
        'utlan': utlan,

        'sok_tekst': sok_tekst,
        'ski_type': ski_type,
        'tilstand': tilstand,
        'utlan_status': utlan_status,
        'dato_fra': dato_fra,
        'dato_til': dato_til,

        'har_sokt': any([sok_tekst, ski_type, tilstand, utlan_status, dato_fra, dato_til]),
        'totale_resultater': len(ski_items) + len(brukere) + len(utlan)
    }

    return render(request, 'skiutlan/avansert_sok.html', context)




def rapporter(request):
    context = {
        'totalt_ski_items': SkiItem.objects.count(),
        'totalt_brukere': Bruker.objects.count(),
        'aktive_utlan': Utlan.objects.filter(returnert_dato__isnull=True).count(),
        'forsinket_utlan': Utlan.objects.filter(
            returnert_dato__isnull=True,
            planlagt_retur__lt=date.today()
        ).count(),
    }

    return render(request, 'skiutlan/rapporter.html', context)


# ============================================================================
# API ENDPOINTS (for AJAX kall)
# ============================================================================

def api_ski_item_tilgjengelighet(request, item_id):
    try:
        ski_item = get_object_or_404(SkiItem, id=item_id)
        return JsonResponse({
            'ledig': not Utlan.objects.filter(ski_item=ski_item, returnert_dato__isnull=True).exists(),
            'navn': ski_item.navn
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def api_sok_brukere(request):
    sok_tekst = request.GET.get('q', '')
    if sok_tekst:
        brukere = Bruker.objects.filter(
            Q(fornavn__icontains=sok_tekst) |
            Q(etternavn__icontains=sok_tekst) |
            Q(telefon__icontains=sok_tekst)
        )[:10]

        results = [
            {
                'id': bruker.id,
                'navn': bruker.fullt_navn,
                'telefon': bruker.telefon
            }
            for bruker in brukere
        ]

        return JsonResponse({'results': results})

    return JsonResponse({'results': []})
