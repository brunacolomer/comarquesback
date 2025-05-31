import os
import django
import random
from comunitat.models import Usuari, Original, Repte, Copiat, Amistat

# Configurar l'entorn Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'el_teu_projecte.settings')
django.setup()
from django.core.management.base import BaseCommand

# Definició dels reptes originals
reptes_data = [
    {"titol": "Descobreix la gastronomia catalana", "permissos": "PUBLIC"},
    {"titol": "Fotografia la posta de sol", "permissos": "AMICS"},
    {"titol": "Dormir a totes les comarques", "permissos": "PUBLIC"},
    {"titol": "Cagar a cada comarca", "permissos": "PUBLIC"},
    {"titol": "Explora els mercats locals", "permissos": "AMICS"},
    {"titol": "Visita els monuments històrics", "permissos": "PUBLIC"},
    {"titol": "Fes una excursió natural", "permissos": "ME"},
    {"titol": "Prova un esport local", "permissos": "AMICS"},
    {"titol": "Aprèn una tradició", "permissos": "PUBLIC"},
    {"titol": "Visita un museu", "permissos": "ME"},
    {"titol": "Cerca els millors graffitis", "permissos": "AMICS"},
    {"titol": "Troba el millor parc", "permissos": "PUBLIC"},
    {"titol": "Recull una pedra de cada comarca", "permissos": "ME"},
    {"titol": "Dormir a totes les comarques", "permissos": "PUBLIC"},
    {"titol": "Prova un gelat a cada comarca", "permissos": "PUBLIC"},
    {"titol": "Fotografia un arbre singular", "permissos": "ME"},
    {"titol": "Participa en una fira local", "permissos": "AMICS"},
    {"titol": "Escapa't a un càmping", "permissos": "PUBLIC"},
    {"titol": "Assisteix a una sessió de cinema", "permissos": "ME"},
    {"titol": "Anar de festa major", "permissos": "AMICS"},
    {"titol": "Fes una ruta en bicicleta", "permissos": "AMICS"},
    {"titol": "Pesca en un llac tranquil", "permissos": "ME"},
    {"titol": "Explora un poble abandonat", "permissos": "PUBLIC"},
    {"titol": "Prova el plat típic de cada comarca", "permissos": "PUBLIC"},
    {"titol": "Observa les estrelles en una nit clara", "permissos": "ME"},
    {"titol": "Participa en una activitat solidària", "permissos": "ME"},
    {"titol": "Fotografia un animal autòcton", "permissos": "AMICS"},
    {"titol": "Neda en una cala secreta", "permissos": "PUBLIC"},
    {"titol": "Escolta una banda local en directe", "permissos": "ME"},
    {"titol": "Visita un castell medieval", "permissos": "PUBLIC"},
    {"titol": "Fes una ruta gastronòmica", "permissos": "AMICS"},
    {"titol": "Pren el sol en una platja desconeguda", "permissos": "ME"},
    {"titol": "Troba una cascada amagada", "permissos": "PUBLIC"},
    {"titol": "Camina per un camí de ronda", "permissos": "AMICS"},
    {"titol": "Fes un pícnic a la muntanya", "permissos": "ME"},
    {"titol": "Visita un molí antic", "permissos": "PUBLIC"},
    {"titol": "Prova un vi local", "permissos": "AMICS"},
    {"titol": "Dibuixa un paisatge natural", "permissos": "ME"}
]


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        usuaris = list(Usuari.objects.all())
        for repte_data in reptes_data:
            _usuari = random.choice(usuaris)
            _titol=repte_data["titol"]
            _visiblitat=random.choice(["ME", "AMICS", "PUBLIC"])
            _permissos=repte_data["permissos"]

            repte_original, created= Original.objects.get_or_create(
                titol=_titol,
                visiblitat=_visiblitat,
                usuari=_usuari,
                permissos = _permissos
            )
            print(f"Original creat: {_titol} - Usuari: {_usuari.username}")

            if _permissos == "PUBLIC" :
                n = random.randint(2000, 50000)
                for _ in range(n):
                    _usuaricopiat = random.choice(usuaris)
                    if _usuaricopiat!=_usuari :
                        Copiat.objects.get_or_create(
                            titol=_titol,
                            visiblitat = random.choice(["ME", "AMICS", "PUBLIC"]),
                            usuari = _usuaricopiat,
                            basat = repte_original
                        )
                        print(f"Còpia creada per {_usuaricopiat.username} basada en {repte_original.titol}")

            elif _permissos == "AMICS" :
                # Amics on l'usuari és `usuari1`
                amistats1 = Amistat.objects.filter(usuari1=_usuari).values_list('usuari2', flat=True)
                # Amics on l'usuari és `usuari2`
                amistats2 = Amistat.objects.filter(usuari2=_usuari).values_list('usuari1', flat=True)

                amics_ids = set(amistats1).union(set(amistats2))

                if len(amics_ids) > 0 :
                    n = random.randint(0, len(amics_ids))
                    for _ in range(n):
                        _usuaricopiat = random.choice(usuaris)
                        if _usuaricopiat!=_usuari :
                            Copiat.objects.get_or_create(
                                titol=_titol,
                                visiblitat = random.choice(["ME", "AMICS", "PUBLIC"]),
                                usuari = _usuaricopiat,
                                basat = repte_original
                            )
                            print(f"Còpia creada per {_usuaricopiat.username} basada en {repte_original.titol}")