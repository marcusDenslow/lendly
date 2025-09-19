"""
Django Forms for skiutlån-systemet.

Forms håndterer brukerinndata, validering og rendering av HTML-skjemaer.
Dette er en viktig del av feilhåndteringen i systemet.

Kjernekrav oppfylt:
- Feilhåndtering ✓ (automatisk validering)
- Brukervennlighet ✓ (fine skjemaer med hjelpetekst)
- Datavalidering ✓ (clean-metoder)

TODO for gruppen:
1. Implementer custom validering i clean_* metoder
2. Legg til widgets for bedre UI
3. Implementer dynamic choices (f.eks. bare ledige ski-items)
4. Legg til AJAX-validering
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, timedelta

from .models import SkiItem, Bruker, Utlan


class SkiItemForm(forms.ModelForm):
    """
    Form for opprettelse og redigering av ski-items.

    TODO for gruppen:
    1. Legg til custom widgets for bedre UI
    2. Implementer clean_storrelse() for validering
    3. Legg til validering som sjekker rimelige størrelser per type
    4. Vurder å legge til et bilde-felt
    """

    class Meta:
        model = SkiItem
        fields = ['navn', 'type_ski', 'storrelse', 'tilstand']
        widgets = {
            # TODO: Legg til custom widgets
            # 'navn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'F.eks. Rossignol Hero Elite'}),
            # 'type_ski': forms.Select(attrs={'class': 'form-control'}),
            # 'storrelse': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 300}),
            # 'tilstand': forms.Select(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'navn': 'Merke og modell på ski-elementet',
            'storrelse': 'Størrelse i cm for ski/staver, EU-størrelse for støvler',
            'tilstand': 'Vurder tilstanden realistisk for trygg utlån',
        }

    def clean_navn(self):
        """
        Validerer at navnet ikke er tomt og ikke inneholder upassende tegn.

        TODO for gruppen:
        1. Hent navn-data med self.cleaned_data['navn']
        2. Sjekk at det ikke er tomt eller bare whitespace
        3. Sjekk at det ikke inneholder spesialtegn som kan være problematiske
        4. Returner det rensede navnet

        Hint: if not navn or not navn.strip():
                  raise ValidationError("Navn kan ikke være tomt")
        """
        pass

    def clean_storrelse(self):
        """
        Validerer at størrelsen er rimelig for den valgte ski-typen.

        TODO for gruppen:
        1. Hent størrelse og type_ski fra cleaned_data
        2. Definer rimelige områder for hver type:
           - Alpinski: 120-200 cm
           - Langrenn: 150-210 cm
           - Snowboard: 130-170 cm
           - Støvler: 20-50 (EU størrelse)
           - Staver: 80-140 cm
        3. Valider at størrelsen er innenfor område
        4. Returner størrelsen

        Eksempel:
        type_ski = self.cleaned_data.get('type_ski')
        storrelse = self.cleaned_data.get('storrelse')

        if type_ski == 'stovler' and (storrelse < 20 or storrelse > 50):
            raise ValidationError("Skistøvler må være mellom størrelse 20-50")
        """
        pass


class BrukerForm(forms.ModelForm):
    """
    Form for opprettelse og redigering av brukere.

    TODO for gruppen:
    1. Legg til konfirmasjon på telefonnummer
    2. Implementer epost-validering
    3. Legg til GDPR-consent checkbox
    4. Valider at telefonnummer følger norsk format
    """

    class Meta:
        model = Bruker
        fields = ['fornavn', 'etternavn', 'telefon', 'epost']
        widgets = {
            # TODO: Legg til Bootstrap-styling
            # 'fornavn': forms.TextInput(attrs={'class': 'form-control'}),
            # 'etternavn': forms.TextInput(attrs={'class': 'form-control'}),
            # 'telefon': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': '+47 12345678',
            #     'pattern': r'\+47\s?\d{8}'
            # }),
            # 'epost': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_telefon(self):
        """
        Validerer telefonnummer-format.

        TODO for gruppen:
        1. Hent telefonnummer fra cleaned_data
        2. Sjekk at det starter med +47 eller 47
        3. Sjekk at det har 8 siffer etter landkode
        4. Normaliser format til +47 XXXXXXXX
        5. Returner normalisert telefonnummer

        Hint: Bruk re (regular expressions) eller string-metoder
        """
        pass

    def clean_epost(self):
        """
        Validerer epost hvis oppgitt.

        TODO for gruppen:
        1. Hent epost fra cleaned_data
        2. Hvis tom: returner None (ok, siden det er valgfritt)
        3. Hvis ikke tom: valider format grundig
        4. Sjekk at domenet eksisterer (valgfritt, avansert)
        """
        pass

    def clean(self):
        """
        Cross-field validering.

        TODO for gruppen:
        1. Sjekk at minst ett kontaktfelt er oppgitt (telefon eller epost)
        2. Hvis bare epost: gi en advarsel
        3. Sjekk at navn ikke er identiske (fornavn != etternavn)
        """
        pass


class UtlanForm(forms.ModelForm):
    """
    Form for opprettelse av nye utlån.

    Dette er den mest komplekse formen siden den må validere
    relasjoner mellom brukere og ski-items.

    TODO for gruppen:
    1. Filtrer ski_item til bare ledige items
    2. Implementer kompleks validering
    3. Legg til kalendar-widget for datoer
    4. Legg til AJAX for dynamisk validering
    """

    class Meta:
        model = Utlan
        fields = ['bruker', 'ski_item', 'planlagt_retur']
        widgets = {
            # TODO: Legg til datepicker for planlagt_retur
            # 'planlagt_retur': forms.DateInput(attrs={
            #     'class': 'form-control',
            #     'type': 'date',
            #     'min': date.today().strftime('%Y-%m-%d')
            # }),
            # 'bruker': forms.Select(attrs={'class': 'form-control'}),
            # 'ski_item': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialiser form med filtrerte valg.

        TODO for gruppen:
        1. Kall super().__init__(*args, **kwargs)
        2. Filtrer ski_item queryset til bare ledige items
        3. Sett default planlagt_retur til 1 uke frem
        4. Ordne querysets for bedre brukervennlighet

        Eksempel:
        self.fields['ski_item'].queryset = SkiItem.objects.filter(...)
        self.fields['planlagt_retur'].initial = date.today() + timedelta(days=7)
        """
        super().__init__(*args, **kwargs)
        # TODO: Implementer filtreringer

    def clean_ski_item(self):
        """
        Validerer at ski-item er ledig for utlån.

        TODO for gruppen:
        1. Hent ski_item fra cleaned_data
        2. Sjekk at det ikke er None
        3. Sjekk at det er ledig (ski_item.er_ledig)
        4. Returner ski_item

        Feilmelding hvis ikke ledig:
        raise ValidationError(f"'{ski_item.navn}' er allerede utlånt")
        """
        pass

    def clean_planlagt_retur(self):
        """
        Validerer planlagt retur-dato.

        TODO for gruppen:
        1. Hent planlagt_retur fra cleaned_data
        2. Sjekk at den ikke er i fortiden
        3. Sjekk at den ikke er mer enn 30 dager frem (rimelig grense)
        4. Advar hvis helg (valgfritt)
        """
        pass

    def clean(self):
        """
        Cross-field validering for utlån.

        TODO for gruppen:
        1. Hent cleaned_data fra super().clean()
        2. Sjekk at bruker ikke har for mange aktive utlån (maks 3?)
        3. Sjekk at samme bruker ikke allerede låner samme type ski
        4. Returner cleaned_data
        """
        pass


class SokForm(forms.Form):
    """
    Form for avansert søk på tvers av systemet.

    TODO for gruppen:
    1. Legg til alle relevante søkekriterier
    2. Implementer smart autocomplete
    3. Legg til lagring av søk (avansert)
    """

    # Grunnleggende søk
    sok_tekst = forms.CharField(
        max_length=200,
        required=False,
        # TODO: Legg til widget og styling
        # widget=forms.TextInput(attrs={
        #     'class': 'form-control',
        #     'placeholder': 'Søk etter navn, type, bruker...'
        # })
    )

    # Filtrering på ski-type
    ski_type = forms.ChoiceField(
        choices=[('', 'Alle typer')] + SkiItem.SKI_TYPES,
        required=False,
        # TODO: Legg til styling
    )

    # Filtrering på tilgjengelighet
    kun_ledige = forms.BooleanField(
        required=False,
        label="Vis bare ledige items"
    )

    # Dato-område for utlån
    dato_fra = forms.DateField(
        required=False,
        # TODO: Legg til datepicker
        # widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    dato_til = forms.DateField(
        required=False,
        # TODO: Legg til datepicker
    )

    def clean(self):
        """
        Validerer søkekriterier.

        TODO for gruppen:
        1. Sjekk at minst ett søkekriterium er oppgitt
        2. Sjekk at dato_fra er før dato_til
        3. Sett default verdier hvis fornuftig
        """
        pass


class ReturForm(forms.Form):
    """
    Enkelt form for å markere utlån som returnert.

    TODO for gruppen:
    1. Legg til kommentar-felt for tilstandsvurdering
    2. Legg til mulighet for å rapportere skader
    3. Implementer automatisk oppdatering av ski-item tilstand
    """

    kommentar = forms.CharField(
        max_length=500,
        required=False,
        # TODO: Legg til textarea widget
        # widget=forms.Textarea(attrs={
        #     'class': 'form-control',
        #     'rows': 3,
        #     'placeholder': 'Valgfri kommentar om tilstand ved retur...'
        # })
    )

    ny_tilstand = forms.ChoiceField(
        choices=SkiItem._meta.get_field('tilstand').choices,
        required=False,
        help_text="Oppdater tilstand hvis den har endret seg"
    )

    def clean_kommentar(self):
        """
        Validerer kommentar.

        TODO for gruppen:
        1. Sjekk at kommentar ikke inneholder støtende innhold
        2. Trim whitespace
        3. Konverter til riktig format
        """
        pass


# TODO for gruppen: Vurder å lage ModelFormSet for bulk-operasjoner
# Fra Django dokumentasjon: https://docs.djangoproject.com/en/stable/topics/forms/formsets/

# UtlanFormSet = forms.modelformset_factory(
#     Utlan,
#     form=UtlanForm,
#     extra=3,  # Antall tomme skjemaer
#     can_delete=True
# )