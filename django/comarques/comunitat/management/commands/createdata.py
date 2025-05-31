# comunitat/management/commands/createdata.py

import random
from faker import Faker

from django.core.management.base import BaseCommand
from comunitat.models import Usuari, Poblacio, Perfil

class Command(BaseCommand):
    help = "Crea dades fictícies per a usuaris, perfils i poblacions"

    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')

        # Crear poblacions
        poblacions = []
        for _ in range(10):
            nom = fake.city()
            p = Poblacio.objects.create(nom=nom)
            poblacions.append(p)
        self.stdout.write(f"{len(poblacions)} poblacions creades.")

        # Crear usuaris + perfils
        for i in range(100):
            username = fake.user_name()
            email = fake.email()
            poblacio = random.choice(poblacions)

            usuari = Usuari.objects.create_user(
                username=username,
                email=email,
                password='contrasenya',
                poblacio=poblacio
            )
            Perfil.objects.create(
                usuari=usuari,
                repte=None,  # o el que vulguis
            )
        self.stdout.write("100 usuaris i perfils creats.")
