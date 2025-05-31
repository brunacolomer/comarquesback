import os
import django
import random
from django.utils import timezone
from datetime import  timedelta
from faker import Faker

# Configurar l'entorn Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'el_teu_projecte.settings')
django.setup()

from django.core.management.base import BaseCommand
from comunitat.models import Amistat, Missatge

fake = Faker('es_ES')

class Command(BaseCommand):
    help = "Crear missatges entre usuaris."

    def handle(self, *args, **kwargs):
        amistats = list(Amistat.objects.all())

        num_missatges = 500000  # Nombre de missatges a crear

        for _ in range(num_missatges):
            # Seleccionar emisor i receptor aleatoris
            amistat = random.choice(amistats)
            emisor = amistat.usuari1
            receptor = amistat.usuari2
            # Invertim aleatòriament emisor i receptor
            if random.choice([True, False]):
                emisor, receptor = receptor, emisor

            # Generar dataHora aleatòria
            dataHora = timezone.now() - timedelta(days=random.randint(0, 1000), hours=random.randint(0, 23), minutes=random.randint(0, 59))

            # Crear el missatge
            try:
                missatge = Missatge.objects.create(
                    emisor=emisor,
                    receptor=receptor,
                    dataHora=dataHora,
                    text=fake.sentence(nb_words=10)
                )
                print(f"Missatge creat: {emisor.username} -> {receptor.username} a les {dataHora}")

            except Exception as e:
                print(f"Error al crear missatge: {e}")
