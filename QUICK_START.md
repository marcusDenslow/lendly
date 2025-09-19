# 🚀 Quick Start Guide - Skiutlån System

## For gruppen - Start her!

Dette er en komplett Django-app for skiutlån, men **mesteparten av koden må implementeres av dere**. Jeg har laget hele strukturen, dokumentasjonen og guidene - dere må fylle inn logikken.

## ✅ Hva er allerede gjort:

1. ✅ **Django prosjekt oppsatt** - fungerer out-of-the-box
2. ✅ **Database modeller definert** - SkiItem, Bruker, Utlan
3. ✅ **URL struktur** - alle ruter definert
4. ✅ **Template struktur** - moderne design med Bootstrap
5. ✅ **Forms struktur** - validering og skjemaer
6. ✅ **Admin panel** - konfigurasjon for dataadministrasjon
7. ✅ **Static files** - CSS og styling
8. ✅ **Komplett dokumentasjon** - alt er forklart

## 🚨 Hva DERE må gjøre:

### 1. FØRSTE SKRITT (5-10 min):
```bash
# Test at alt fungerer:
python manage.py runserver
# Gå til http://127.0.0.1:8000
# Du skal se hjemmesiden (den vil være tom siden views ikke er implementert)

# Opprett admin-bruker:
python manage.py createsuperuser
# Gå til http://127.0.0.1:8000/admin/
```

### 2. HØYESTE PRIORITET - Models (30-45 min):

Åpne `skiutlan/models.py` og implementer alle `pass`-statements:

```python
# Eksempel på hva dere må gjøre:
def __str__(self):
    return f"{self.navn} ({self.get_type_ski_display()})"

@property
def er_ledig(self):
    return not self.utlan_set.filter(returnert_dato__isnull=True).exists()
```

**TODO i models.py:**
- [ ] SkiItem.__str__()
- [ ] SkiItem.er_ledig property
- [ ] Bruker.__str__()
- [ ] Bruker.aktive_utlan property
- [ ] Utlan.__str__()
- [ ] Utlan.varighet property
- [ ] Utlan.er_forsinket property
- [ ] Utlan.clean() method
- [ ] Utlan.save() method

### 3. ANDRE PRIORITET - Views (60-90 min):

Åpne `skiutlan/views.py` og implementer views:

**Start med disse:**
- [ ] `hjem()` - fyll inn statistics
- [ ] `ski_item_liste()` - vis alle ski items
- [ ] `ski_item_opprett()` - opprett nye items

**Deretter:**
- [ ] Resten av ski_item views
- [ ] Bruker views
- [ ] Utlån views

### 4. TREDJE PRIORITET - Forms (30-45 min):

Åpne `skiutlan/forms.py` og implementer validering:
- [ ] Form.clean_*() metoder
- [ ] Widget styling
- [ ] Custom validering

### 5. FJERDE PRIORITET - Admin (15-30 min):

Åpne `skiutlan/admin.py` og fyll inn:
- [ ] list_display lister
- [ ] search_fields
- [ ] list_filter

## 🎯 Arbeidsfordeling forslag:

**Person 1: Models & Database**
- Implementer alle model-metoder
- Test at database fungerer
- Opprett testdata via admin

**Person 2: Views & Logic**
- Implementer view-funksjoner
- Koble sammen templates og data
- Implementer søkefunksjonalitet

**Person 3: Forms & Validation**
- Implementer form-validering
- Forbedre brukeropplevelse
- Test all input-validering

**Person 4: Design & Templates**
- Tilpass CSS og styling
- Forbedre templates
- Teste på mobile enheter

## 📋 Testing checklist:

Etter implementering, test at dette fungerer:

### Admin Panel:
- [ ] Kan opprette ski-items
- [ ] Kan opprette brukere
- [ ] Kan opprette utlån
- [ ] Søk fungerer i admin

### Web Interface:
- [ ] Hjemmeside viser statistikk
- [ ] Kan navigere til alle sider
- [ ] Kan opprette nye items via web
- [ ] Søk og filtrering fungerer
- [ ] Forms validerer korrekt
- [ ] Error messages vises

### Data Logic:
- [ ] Ski-items viser riktig status (ledig/utlånt)
- [ ] Utlån markeres som forsinket korrekt
- [ ] Kan ikke låne samme item til flere
- [ ] Retur-funksjonalitet fungerer

## 🆘 Hvis dere står fast:

### Debug steg:
1. **Sjekk Django error-side** - den viser nøyaktig hva som er galt
2. **Bruk Django shell**: `python manage.py shell`
   ```python
   from skiutlan.models import SkiItem
   items = SkiItem.objects.all()
   print(items)
   ```
3. **Sjekk at URL-er matcher** views og templates
4. **Test én ting av gangen** - ikke implementer alt samtidig

### Vanlige feil:
- **TemplateDoesNotExist**: Sjekk filsti og navn
- **NoReverseMatch**: Sjekk URL-navn i templates
- **AttributeError**: Sjekk at alle model-metoder er implementert
- **ValidationError**: Sjekk form.clean() metoder

## 📚 Django-ressurser:

- [Django Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
- [Model Field Reference](https://docs.djangoproject.com/en/stable/ref/models/fields/)
- [Form Validation](https://docs.djangoproject.com/en/stable/ref/forms/validation/)

## 🎯 Ferdigstillelse:

Når alt fungerer:
1. **Test alle kjernefunksjoner**
2. **Lag testdata** (minst 10 ski-items, 5 brukere, 5 utlån)
3. **Skriv teknisk rapport** basert på README
4. **Ta screenshots** av systemet
5. **Lever prosjekt**

**Lykke til! Dere har et solid fundament å bygge på! 🎿**