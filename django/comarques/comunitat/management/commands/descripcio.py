import os
import django
import random
from faker import Faker

# Configurar l'entorn Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'el_teu_projecte.settings')
django.setup()

from django.core.management.base import BaseCommand
from comunitat.models import Descripcio, Original, Comarca

fake = Faker('es_ES')

class Command(BaseCommand):
    help = "Crear descripcions per reptes originals en comarques."

    def handle(self, *args, **kwargs):
        originals = list(Original.objects.all())
        comarques = list(Comarca.objects.all())

        if not originals or not comarques:
            print("Calen reptes originals i comarques per crear descripcions.")
            return

        num_descripcions = 10000  # Nombre de descripcions a crear

        for _ in range(num_descripcions):
            # Seleccionar un repte original i una comarca aleatòriament
            original = random.choice(originals)
            comarca = random.choice(comarques)

            # Verificar que no existeixi ja aquesta descripció
            if Descripcio.objects.filter(original=original, comarca=comarca).exists():
                print(f"La descripció ja existeix per {original.titol} a {comarca.nom}.")
                continue

            # Crear descripció
            descripcio = Descripcio.objects.create(
                original=original,
                comarca=comarca,
                descripcio=fake.sentence(nb_words=20)
            )

            print(f"Descripció creada per {original.titol} a {comarca.nom}: {descripcio.descripcio}")
