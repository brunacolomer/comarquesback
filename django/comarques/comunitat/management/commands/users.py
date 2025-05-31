import os
import django
import random
from faker import Faker

# Configurar l'entorn Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'el_teu_projecte.settings')
django.setup()
from django.core.management.base import BaseCommand

from comunitat.models import Usuari, Poblacio

fake = Faker('es_ES')  # Idioma espanyol per a noms més realistes
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        n=15000 -14343
        poblacions = list(Poblacio.objects.all())

        for _ in range(n):
            username = fake.user_name()
            username = username + str(random.randint(1, 10000))  # Assegura que el nom d'usuari sigui únic
            email = fake.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            puntuacio = random.randint(0, 5000)
            poblacio = random.choice(poblacions)
            password = fake.password(length=8, special_chars=True, digits=True, upper_case=True, lower_case=True)

            usuari = Usuari.objects.get_or_create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                puntuacio=puntuacio,
                poblacio=poblacio,
                password=password
            )

            print(f"Usuari creat: {username, email, first_name, last_name, puntuacio, poblacio, password}")
