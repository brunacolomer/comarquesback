import os
import django
import random
from faker import Faker

# Configurar l'entorn Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'el_teu_projecte.settings')
django.setup()

from django.core.management.base import BaseCommand
from comunitat.models import Usuari, Perfil, Repte

fake = Faker('es_ES')

def get_repte_preferit(usuari):
    """ Retorna un repte preferit per a un usuari, o None si no en té. """
    reptes = Repte.objects.filter(usuari=usuari)
    if reptes.exists():
        return random.choice(reptes)
    return None

class Command(BaseCommand):
    help = "Crear perfils per usuaris amb reptes preferits."
    
    def handle(self, *args, **kwargs):
        i = 0
        usuaris = Usuari.objects.all()

        for usuari in usuaris:
            # Comprovar si ja té un perfil
            if hasattr(usuari, 'creat'):
                print(f"L'usuari {usuari.username} ja té un perfil.")
                continue

            # Obtenir un repte preferit
            repte_preferit = get_repte_preferit(usuari)

            if not repte_preferit:
                print(f"L'usuari {usuari.username} no té reptes preferits. No es crearà perfil.")
                continue
            
            i= i+1
            if i> 7500 :
                break
            # Crear perfil
            perfil = Perfil.objects.get_or_create(
                usuari=usuari,
                repte=repte_preferit,
                descripcio=fake.sentence(nb_words=15),
                foto=f"https://picsum.photos/200/200?random={random.randint(1, 1000)}"
            )

            print(f"Perfil creat per {usuari.username} amb repte preferit: {repte_preferit.titol}")
