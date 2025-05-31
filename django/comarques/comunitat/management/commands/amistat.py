import os
import django
import random
from faker import Faker
from comunitat.models import Usuari, Amistat

# Configurar l'entorn Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'el_teu_projecte.settings')
django.setup()
from django.core.management.base import BaseCommand
fake = Faker('es_ES')
def get_random_image_url():
    """ Genera una URL d'imatge aleatòria de Lorem Picsum """
    width = random.randint(300, 800)
    height = random.randint(300, 800)
    return f"https://picsum.photos/{width}/{height}"

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        num_amistats = 300000  # Nombre d'amicitats a crear
        usuaris = list(Usuari.objects.all())
        n = len(usuaris)

        if n < 2:
            print("Calen almenys 2 usuaris per crear amistats.")
            return

        amistats_creades = 0
        intents = 0

        while amistats_creades < num_amistats and intents < num_amistats * 2:
            # Seleccionem dos usuaris aleatoris
            usuari1 = random.choice(usuaris)
            usuari2 = random.choice(usuaris)

            # Evitar amistats amb un mateix usuari
            if usuari1 == usuari2:
                continue

            # Comprovar que l'amistat no existeix (en cap direcció)
            existent_amistat = Amistat.objects.filter(
                usuari1=usuari1, usuari2=usuari2
            ).exists() or Amistat.objects.filter(
                usuari1=usuari2, usuari2=usuari1
            ).exists()

            if not existent_amistat:
                # Crear l'amistat
                Amistat.objects.get_or_create(
                    usuari1=usuari1,
                    usuari2=usuari2,
                    descripcio=fake.sentence(),
                    foto=get_random_image_url()
                )

                print(f"Amistat creada: {usuari1.username} - {usuari2.username}")
                amistats_creades += 1

            intents += 1

        print(f"{amistats_creades} amistats creades.")