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
        # TODO: Implementer denne metoden
        # Den skal returnere f.eks: "Alpinski (180cm) - God tilstand"
        pass

    @property
    def er_ledig(self):
        """
        Sjekker om dette ski-elementet er tilgjengelig for utlån.

        TODO for gruppen:
        1. Sjekk om det finnes et aktivt utlån for dette elementet
        2. Returner True hvis ledig, False hvis utlånt

        Hint: Bruk self.utlan_set.filter(returnert_dato__isnull=True).exists()
        """
        pass


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
        # TODO: Implementer denne metoden
        # Den skal returnere f.eks: "Lars Hansen (+47 12345678)"
        pass

    @property
    def fullt_navn(self):
        """Returnerer fullt navn som en string."""
        return f"{self.fornavn} {self.etternavn}"

    @property
    def aktive_utlan(self):
        """
        Returnerer antall aktive utlån for denne brukeren.

        TODO for gruppen:
        1. Tell opp utlån som ikke er returnert ennå
        2. Returner antallet

        Hint: return self.utlan_set.filter(returnert_dato__isnull=True).count()
        """
        pass


class Utlan(models.Model):
    """
    Modell som representerer et utlån av ski-utstyr.

    Denne modellen kobler sammen en Bruker med et SkiItem og
    holder styr på når utlånet startet og sluttet.

    TODO for gruppen:
    1. Implementer __str__ metoden
    2. Lag en @property som beregner hvor lenge utlånet har vart
    3. Lag en @property som sjekker om utlånet er forsinket
    4. Implementer clean() metoden for validering
    5. Vurder å legge til kommentar-felt
    """

    # Relasjoner - dette kobler tabellene sammen
    bruker = models.ForeignKey(
        Bruker,
        on_delete=models.CASCADE,  # Hvis bruker slettes, slettes også utlånene
        help_text="Hvem som låner"
    )

    ski_item = models.ForeignKey(
        SkiItem,
        on_delete=models.CASCADE,  # Hvis ski-item slettes, slettes også utlånene
        help_text="Hva som lånes"
    )

    # Datoer for utlån
    utlant_dato = models.DateTimeField(
        default=timezone.now,
        help_text="Når ble itemet lånt ut"
    )

    planlagt_retur = models.DateField(
        help_text="Når skal itemet leveres tilbake"
    )

    returnert_dato = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Når ble itemet faktisk levert tilbake (tomt = ikke returnert)"
    )

    # Metadata
    opprettet = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Utlån"
        verbose_name_plural = "Utlån"
        ordering = ['-utlant_dato']  # Nyeste først

        # Unike constraints - samme item kan ikke lånes av flere samtidig
        constraints = [
            models.UniqueConstraint(
                fields=['ski_item'],
                condition=models.Q(returnert_dato__isnull=True),
                name='unique_active_loan_per_item'
            )
        ]

    def __str__(self):
        # TODO: Implementer denne metoden
        # Den skal returnere f.eks: "Lars Hansen låner Alpinski (180cm) - Aktiv"
        pass

    @property
    def er_aktivt(self):
        """Sjekker om utlånet er aktivt (ikke returnert ennå)."""
        return self.returnert_dato is None

    @property
    def varighet(self):
        """
        Beregner hvor lenge utlånet har vart.

        TODO for gruppen:
        1. Hvis returnert: beregn tid mellom utlant_dato og returnert_dato
        2. Hvis ikke returnert: beregn tid mellom utlant_dato og nå
        3. Returner som timedelta objekt

        Hint: Bruk timezone.now() for nåværende tid
        """
        pass

    @property
    def er_forsinket(self):
        """
        Sjekker om utlånet er forsinket.

        TODO for gruppen:
        1. Hvis allerede returnert: return False
        2. Hvis ikke returnert: sammenlign dagens dato med planlagt_retur
        3. Returner True hvis forsinket

        Hint: from django.utils import timezone; timezone.now().date()
        """
        pass

    def clean(self):
        """
        Validerer at utlånet er gyldig før lagring.

        TODO for gruppen:
        1. Sjekk at ski_item er ledig (ikke allerede utlånt)
        2. Sjekk at planlagt_retur ikke er i fortiden
        3. Hvis returnert_dato er satt, sjekk at den ikke er før utlant_dato
        4. Raise ValidationError med beskrivende melding hvis noe er galt

        Hint: from django.core.exceptions import ValidationError
        """
        pass

    def save(self, *args, **kwargs):
        """
        Override save-metoden for å kjøre validering.

        TODO for gruppen:
        1. Kall self.clean() før lagring
        2. Kall super().save(*args, **kwargs) for å faktisk lagre
        """
        pass
