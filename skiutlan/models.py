"""
Django modeller for skiutlån-systemet.

Dette filen definerer databasestrukturene for vårt skiutlån-system.
Vi har tre hovedmodeller:
1. SkiItem - representerer et skielement som kan lånes
2. Bruker - representerer en person som kan låne ski
3. Utlan - representerer et aktivt utlån (kobler sammen bruker og skiitem)

Kjernekrav oppfylt:
- Datastruktur ✓ (Django models er avanserte datastrukturer)
- Opprette/legge til ✓ (create operasjoner)
- Lese/liste ✓ (read operasjoner)
- Oppdatere ✓ (update operasjoner)
- Slette ✓ (delete operasjoner)
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta


class SkiItem(models.Model):
    """
    Modell for et skielement som kan lånes ut.

    Eksempler på ski-items:
    - Alpinski
    - Langrennsski
    - Snowboard
    - Skistøvler
    - Skistaver

    TODO for gruppen:
    1. Legg til flere relevante felt (farge, årsmodell, etc.)
    2. Implementer __str__ metoden som returnerer en fin representasjon
    3. Legg til en @property metode som sjekker om itemet er ledig
    4. Vurder validering av størrelse (maks 50 for ski, maks 15 for støvler)
    """

    # VALG/CHOICES for type ski - dette gjør det lett å kategorisere
    SKI_TYPES = [
        ('alpinski', 'Alpinski'),
        ('langrenn', 'Langrennsski'),
        ('snowboard', 'Snowboard'),
        ('stovler', 'Skistøvler'),
        ('staver', 'Skistaver'),
    ]

    # Grunnleggende informasjon om ski-item
    navn = models.CharField(max_length=100, help_text="Navn på ski-elementet")
    type_ski = models.CharField(
        max_length=20,
        choices=SKI_TYPES,
        help_text="Type ski-element"
    )

    # Fysiske egenskaper
    storrelse = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(300)],
        help_text="Størrelse i cm for ski/staver, EU-størrelse for støvler"
    )

    # Status og tilstand
    tilstand = models.CharField(
        max_length=20,
        choices=[
            ('utmerket', 'Utmerket'),
            ('god', 'God'),
            ('slitt', 'Slitt'),
            ('reparasjon', 'Trenger reparasjon'),
        ],
        default='god'
    )

    # Metadata
    opprettet = models.DateTimeField(auto_now_add=True)
    oppdatert = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ski-element"
        verbose_name_plural = "Ski-elementer"
        ordering = ['type_ski', 'storrelse']  # Sorterer automatisk

    def __str__(self):
        return f"{self.get_type_ski_display()} ({self.storrelse}{'EU' if self.type_ski == 'stovler' else 'cm'}) - {self.get_tilstand_display()}"

    @property
    def er_ledig(self):
        """
        Sjekker om dette ski-elementet er tilgjengelig for utlån.
        """
        return not self.utlan_set.filter(returnert_dato__isnull=True).exists()


class Bruker(models.Model):
    """
    Modell for en person som kan låne ski-utstyr.

    Vi lager vår egen brukermodell i stedet for å bruke Django's
    innebygde User-modell for å holde det enkelt for dere.

    TODO for gruppen:
    1. Implementer __str__ metoden
    2. Legg til en @property som viser antall aktive utlån
    3. Vurder å legge til epost-validering
    4. Legg til en metode som sjekker om brukeren kan låne mer (maks 3 items?)
    """

    # Personlig informasjon
    fornavn = models.CharField(max_length=50)
    etternavn = models.CharField(max_length=50)
    telefon = models.CharField(
        max_length=15,
        unique=True,  # Hver bruker må ha unikt telefonnummer
        help_text="Telefonnummer med landkode (+47)"
    )

    # Valgfri informasjon
    epost = models.EmailField(blank=True, null=True)

    # Metadata
    registrert = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Bruker"
        verbose_name_plural = "Brukere"
        ordering = ['etternavn', 'fornavn']

    def __str__(self):
        return f"{self.fornavn} {self.etternavn} ({self.telefon})"

    @property
    def fullt_navn(self):
        """Returnerer fullt navn som en string."""
        return f"{self.fornavn} {self.etternavn}"

    @property
    def aktive_utlan(self):
        """
        Returnerer antall aktive utlån for denne brukeren.
        """
        return self.utlan_set.filter(returnert_dato__isnull=True).count()


class Utlan(models.Model):
    """
    Enkel modell for utlån av ski-utstyr.
    """

    bruker = models.ForeignKey(Bruker, on_delete=models.CASCADE)
    ski_item = models.ForeignKey(SkiItem, on_delete=models.CASCADE)
    utlant_dato = models.DateTimeField(auto_now_add=True)
    planlagt_retur = models.DateField()
    returnert_dato = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.bruker.fornavn} {self.bruker.etternavn} låner {self.ski_item.navn}"

    @property
    def er_aktivt(self):
        return self.returnert_dato is None

    @property
    def er_forsinket(self):
        """Sjekker om utlånet er forsinket."""
        if self.returnert_dato:
            return False
        from datetime import date
        return self.planlagt_retur < date.today()

    @property
    def varighet(self):
        """Beregner hvor lenge utlånet har vart."""
        from django.utils import timezone
        if self.returnert_dato:
            return self.returnert_dato - self.utlant_dato
        else:
            return timezone.now() - self.utlant_dato
