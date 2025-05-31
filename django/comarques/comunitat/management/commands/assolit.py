import os
import django
import random
from faker import Faker

# Configurar l'entorn Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'el_teu_projecte.settings')
django.setup()

from django.core.management.base import BaseCommand
from comunitat.models import Assolit, Repte, Comarca

fake = Faker('es_ES')

class Command(BaseCommand):
    help = "Crear assoliments per reptes en comarques."

    def handle(self, *args, **kwargs):
        reptes = list(Repte.objects.all())
        comarques = list(Comarca.objects.all())

        if not reptes or not comarques:
            print("Calen reptes i comarques per crear assoliments.")
            return

        num_assolits = 100000  # Nombre d'assoliments a crear

        for _ in range(num_assolits):
            # Seleccionar un repte i una comarca aleatòriament
            repte = random.choice(reptes)
            comarca = random.choice(comarques)

            # Verificar que no existeixi ja aquest assoliment
            if Assolit.objects.filter(repte=repte, comarca=comarca).exists():
                print(f"L'assoliment ja existeix per {repte.titol} a {comarca.nom}.")
                continue

            # Crear assoliment
            assoliment = Assolit.objects.get_or_create(
                repte=repte,
                comarca=comarca,
                foto=f"https://picsum.photos/200/300?random={random.randint(1, 1000)}",
                descripcio=fake.sentence(nb_words=15)
            )

            print(f"Assoliment creat: {repte.titol} a {comarca.nom}")
