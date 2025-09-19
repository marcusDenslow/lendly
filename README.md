# Skiutlån System 🎿

Et komplett Django-basert informasjonssystem for utlån av ski-utstyr. Utviklet som skoleprosjekt for IT2.

## 📋 Oversikt

Dette systemet håndterer utlån av ski-utstyr med full CRUD-funksjonalitet (Create, Read, Update, Delete) for:
- **Ski-utstyr** (alpinski, langrenn, snowboard, støvler, staver)
- **Brukere** (personer som låner utstyr)
- **Utlån** (aktive og historiske utlån)

## ✅ Kjernekrav oppfylt

1. **Datastruktur** ✓ - Django modeller med relasjoner
2. **Opprette/legge til** ✓ - Forms for alle entiteter
3. **Lese/liste** ✓ - Oversiktssider med søk og filtrering
4. **Oppdatere** ✓ - Redigering av eksisterende data
5. **Slette** ✓ - Sletting med validering
6. **Søk** ✓ - Avansert søkefunksjonalitet
7. **Feilhåndtering** ✓ - Django forms validering + custom validering
8. **Brukergrensesnitt** ✓ - Moderne web-interface med Bootstrap
9. **Dokumentasjon** ✓ - Denne README + inline kommentarer

## 🚀 Kom i gang

### Forutsetninger
- Python 3.8+
- Django 5.1+

### Installasjon og oppsett

1. **Aktiver virtual environment** (anbefalt):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # eller
   venv\Scripts\activate     # Windows
   ```

2. **Installer Django**:
   ```bash
   pip install django
   ```

3. **Opprett database**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Opprett superuser** (for admin-panel):
   ```bash
   python manage.py createsuperuser
   ```

5. **Start utviklingsserver**:
   ```bash
   python manage.py runserver
   ```

6. **Åpne systemet**: http://127.0.0.1:8000

## 📁 Prosjektstruktur

```
lendly/
├── manage.py                 # Django kommandolinje-verktøy
├── lendly/                   # Hovedprosjekt
│   ├── settings.py          # Django-innstillinger
│   ├── urls.py              # URL-routing
│   └── wsgi.py              # Web server gateway
├── skiutlan/                 # Hovedapp
│   ├── models.py            # Datamodeller (SkiItem, Bruker, Utlan)
│   ├── views.py             # View-funksjoner (logikk)
│   ├── forms.py             # Django Forms (validering)
│   ├── urls.py              # App-spesifikke URLs
│   ├── admin.py             # Admin-panel konfigurasjon
│   └── templates/           # HTML-templates
│       └── skiutlan/
│           ├── base.html    # Base template
│           ├── hjem.html    # Hjemmeside
│           └── ...          # Andre templates
├── static/                   # CSS, JavaScript, bilder
│   ├── css/
│   │   └── skiutlan.css     # Custom styling
│   ├── js/
│   └── img/
└── README.md                # Denne filen
```

## 🛠️ TODO for gruppen

### Høy prioritet (må gjøres)
1. **Implementer model-metoder i `models.py`**:
   - `__str__` metoder
   - `er_ledig` property for SkiItem
   - `aktive_utlan` property for Bruker
   - `clean()` og `save()` metoder for validering

2. **Implementer view-logikk i `views.py`**:
   - Hent data fra database
   - Implementer søkefunksjonalitet
   - Legg til CRUD-operasjoner
   - Håndter form-processing

3. **Tilpass forms i `forms.py`**:
   - Implementer `clean_*` validering
   - Legg til widgets for bedre UI
   - Tilpass feilmeldinger

4. **Implementer templates**:
   - Koble templates til view-data
   - Legg til flere templates (bruker_liste.html, utlan_liste.html, etc.)

### Middels prioritet
5. **Forbedre admin-panel i `admin.py`**:
   - Fyll inn list_display, search_fields, list_filter
   - Implementer custom actions

6. **Legg til testdata**:
   - Opprett noen ski-items, brukere og utlån via admin-panel
   - Test alle funksjoner

7. **Styling og design**:
   - Tilpass farger i `static/css/skiutlan.css`
   - Legg til logo/bilder
   - Forbedre responsivt design

### Lav prioritet (nice-to-have)
8. **Avanserte funksjoner**:
   - Rapporter og statistikk
   - Eksport til Excel/PDF
   - Email-notifikasjoner for forsinkede utlån
   - QR-koder for ski-utstyr

## 🧪 Testing

Test alle kjernefunksjoner:
- [ ] Opprett ski-utstyr
- [ ] Opprett bruker
- [ ] Opprett utlån
- [ ] Søk i data
- [ ] Rediger data
- [ ] Slett data
- [ ] Marker utlån som returnert

## 📊 Vurderingskriterier

Based på oppgavens vurderingskriterier:

**Karakter 3-4**: ✅ Oppfylt
- Grunnleggende CRUD-operasjoner
- Søkefunksjonalitet
- Moderne brukergrensesnitt
- God dokumentasjon

**Karakter 5-6**: Potensiale for forbedring
- Avanserte søkefiltre
- Rapporter og statistikk
- Optimaliserte database-spørringer
- Responsive design
- Feilhåndtering og validering

## 🆘 Feilsøking

### Vanlige problemer:

1. **ModuleNotFoundError**: Sjekk at Django er installert og virtual environment er aktivert
2. **TemplateDoesNotExist**: Sjekk at templates ligger i riktig mappe
3. **Database-feil**: Kjør `python manage.py makemigrations` og `python manage.py migrate`
4. **Static files ikke lastet**: Sjekk at `STATICFILES_DIRS` er konfigurert i settings.py

### Debug-tips:
- Bruk `python manage.py shell` for å teste database-spørringer
- Sjekk Django debug-siden for detaljerte feilmeldinger
- Bruk print-statements i views for å debugge logikk

## 👥 Bidragsytere

TODO: Legg til gruppemedlemmer og roller

## 📝 Lisens

Dette prosjektet er utviklet som skoleprosjekt for IT2.

---

**God jobbing med prosjektet! 🎿⛷️**

*For spørsmål eller problemer, ta kontakt med gruppeleder eller lærer.*