# FERIT konzultacije – Django projekt

Web aplikacija za rezervaciju konzultacija između **studenata** i **mentora** na FERIT-u.

## Uloge
- **Student**: registracija + pregled termina + rezervacija + pregled svojih rezervacija
- **Mentor**: upravljanje vlastitim terminima (dodavanje i pregled)
- **Admin**: puni pristup kroz Django admin

## Pokretanje (Windows / PowerShell)

```powershell
# 1) aktiviraj virtualno okruženje
.\venv\Scripts\Activate.ps1

# 2) instaliraj ovisnosti
pip install -r requirements.txt

# 3) migracije
python manage.py migrate

# 4) pokreni server
python manage.py runserver
```

Aplikacija je dostupna na: http://127.0.0.1:8000/

## Kreiranje admin korisnika

```powershell
python manage.py createsuperuser
```

## Napomena o grupama (mentor/student)
- Registracija dodaje korisnika u grupu **student**
- Mentora dodaješ tako da korisniku u adminu dodaš grupu **mentor**
