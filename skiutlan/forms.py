"""
Django Forms for skiutlån-systemet.

Forms håndterer brukerinput, validering og rendering av HTML-skjemaer.
Dette gir oss sikker og brukervennlig datainntasting.
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, timedelta

from .models import SkiItem, Bruker, Utlan


class SkiItemForm(forms.ModelForm):
    """
    Skjema for å opprette og redigere ski-items.
    """

    class Meta:
        model = SkiItem
        fields = ['navn', 'type_ski', 'storrelse', 'tilstand']
        widgets = {
            'navn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'F.eks. Rossignol Hero Elite'
            }),
            'type_ski': forms.Select(attrs={
                'class': 'form-control'
            }),
            'storrelse': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Størrelse i cm eller EU'
            }),
            'tilstand': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'navn': 'Navn på ski-element',
            'type_ski': 'Type',
            'storrelse': 'Størrelse',
            'tilstand': 'Tilstand',
        }

    def clean_storrelse(self):
        """Validerer størrelse basert på ski-type."""
        storrelse = self.cleaned_data.get('storrelse')
        type_ski = self.cleaned_data.get('type_ski')

        if storrelse:
            if type_ski == 'stovler' and (storrelse < 20 or storrelse > 50):
                raise ValidationError('Skistøvler må være mellom størrelse 20-50.')
            elif type_ski in ['alpinski', 'langrenn'] and (storrelse < 80 or storrelse > 220):
                raise ValidationError('Ski må være mellom 80-220 cm.')
            elif type_ski == 'staver' and (storrelse < 80 or storrelse > 160):
                raise ValidationError('Staver må være mellom 80-160 cm.')
            elif type_ski == 'snowboard' and (storrelse < 120 or storrelse > 180):
                raise ValidationError('Snowboard må være mellom 120-180 cm.')

        return storrelse


class BrukerForm(forms.ModelForm):
    """
    Skjema for å opprette og redigere brukere.
    """

    class Meta:
        model = Bruker
        fields = ['fornavn', 'etternavn', 'telefon', 'epost']
        widgets = {
            'fornavn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fornavn'
            }),
            'etternavn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Etternavn'
            }),
            'telefon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+47 12 34 56 78'
            }),
            'epost': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'navn@example.com (valgfri)'
            }),
        }
        labels = {
            'fornavn': 'Fornavn',
            'etternavn': 'Etternavn',
            'telefon': 'Telefonnummer',
            'epost': 'E-post (valgfri)',
        }

    def clean_telefon(self):
        """Validerer telefonnummer format."""
        telefon = self.cleaned_data.get('telefon')

        if telefon:
            # Fjern mellomrom og bindestrek
            telefon_clean = telefon.replace(' ', '').replace('-', '')

            # Sjekk at det starter med +47 eller er 8 siffer
            if not (telefon_clean.startswith('+47') or (telefon_clean.isdigit() and len(telefon_clean) == 8)):
                raise ValidationError('Telefonnummer må være norsk format (+47 eller 8 siffer).')

        return telefon

    def clean_epost(self):
        """Validerer e-post hvis oppgitt."""
        epost = self.cleaned_data.get('epost')

        if epost:
            # Django's EmailField håndterer grunnleggende validering
            # Vi kan legge til ekstra validering her hvis nødvendig
            pass

        return epost


class UtlanForm(forms.ModelForm):
    """
    Skjema for å opprette utlån.
    """

    class Meta:
        model = Utlan
        fields = ['bruker', 'ski_item', 'planlagt_retur']
        widgets = {
            'bruker': forms.Select(attrs={
                'class': 'form-control'
            }),
            'ski_item': forms.Select(attrs={
                'class': 'form-control'
            }),
            'planlagt_retur': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'bruker': 'Hvem låner',
            'ski_item': 'Hva lånes',
            'planlagt_retur': 'Planlagt returdag',
        }

    def __init__(self, *args, **kwargs):
        """Setter default verdier og filtrerer valg."""
        super().__init__(*args, **kwargs)

        # Sett default planlagt_retur til 1 uke frem
        if not self.instance.pk:  # Bare for nye utlån
            self.fields['planlagt_retur'].initial = date.today() + timedelta(days=7)

        # Filtrer ski_items til bare ledige
        ledige_items = []
        for item in SkiItem.objects.all():
            # Sjekk om item er ledig (ingen aktive utlån)
            if not Utlan.objects.filter(ski_item=item, returnert_dato__isnull=True).exists():
                ledige_items.append(item.id)

        self.fields['ski_item'].queryset = SkiItem.objects.filter(id__in=ledige_items)

        # Sorter brukere alfabetisk
        self.fields['bruker'].queryset = Bruker.objects.order_by('etternavn', 'fornavn')

    def clean_planlagt_retur(self):
        """Validerer at planlagt retur ikke er i fortiden."""
        planlagt_retur = self.cleaned_data.get('planlagt_retur')

        if planlagt_retur and planlagt_retur < date.today():
            raise ValidationError('Planlagt retur kan ikke være i fortiden.')

        return planlagt_retur

    def clean_ski_item(self):
        """Validerer at ski-item er ledig."""
        ski_item = self.cleaned_data.get('ski_item')

        if ski_item:
            # Sjekk om det finnes aktive utlån for dette itemet
            aktive_utlan = Utlan.objects.filter(
                ski_item=ski_item,
                returnert_dato__isnull=True
            )

            # Hvis vi redigerer et eksisterende utlån, ekskluder det fra sjekken
            if self.instance and self.instance.pk:
                aktive_utlan = aktive_utlan.exclude(pk=self.instance.pk)

            if aktive_utlan.exists():
                raise ValidationError(f'"{ski_item.navn}" er allerede utlånt.')

        return ski_item

    def clean(self):
        """Kryssfelt-validering."""
        cleaned_data = super().clean()
        bruker = cleaned_data.get('bruker')

        if bruker:
            # Sjekk om bruker har for mange aktive utlån (maks 3)
            aktive_utlan_count = Utlan.objects.filter(
                bruker=bruker,
                returnert_dato__isnull=True
            ).count()

            # Hvis vi redigerer et eksisterende utlån, trekk det fra tellingen
            if self.instance and self.instance.pk:
                aktive_utlan_count -= 1

            if aktive_utlan_count >= 3:
                raise ValidationError(
                    f'{bruker.fullt_navn} har allerede 3 aktive utlån. '
                    'Maksimalt antall utlån er 3 per bruker.'
                )

        return cleaned_data


class SokForm(forms.Form):
    """
    Skjema for avansert søk på tvers av alle modeller.
    """

    sok_tekst = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Søk etter navn, type, telefon...'
        }),
        label='Søketekst'
    )

    ski_type = forms.ChoiceField(
        choices=[('', 'Alle typer')] + SkiItem.SKI_TYPES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Ski-type'
    )

    tilstand = forms.ChoiceField(
        choices=[('', 'Alle tilstander')] + [
            ('utmerket', 'Utmerket'),
            ('god', 'God'),
            ('slitt', 'Slitt'),
            ('reparasjon', 'Trenger reparasjon'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Tilstand'
    )

    utlan_status = forms.ChoiceField(
        choices=[
            ('', 'Alle'),
            ('aktive', 'Aktive utlån'),
            ('returnerte', 'Returnerte utlån'),
            ('forsinket', 'Forsinket utlån'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Utlån status'
    )

    dato_fra = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Utlånt fra dato'
    )

    dato_til = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Utlånt til dato'
    )

    def clean(self):
        """Validerer at dato_fra er før dato_til."""
        cleaned_data = super().clean()
        dato_fra = cleaned_data.get('dato_fra')
        dato_til = cleaned_data.get('dato_til')

        if dato_fra and dato_til and dato_fra > dato_til:
            raise ValidationError('Fra-dato må være før til-dato.')

        return cleaned_data