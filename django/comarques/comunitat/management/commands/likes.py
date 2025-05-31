import os
import django
import random

# Configurar l'entorn Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'el_teu_projecte.settings')
django.setup()

from django.core.management.base import BaseCommand
from comunitat.models import Perfil

class Command(BaseCommand):
    help = "Crear likes entre perfils."

    def handle(self, *args, **kwargs):
        perfils = list(Perfil.objects.all())

        if len(perfils) < 2:
            print("Calen almenys dos perfils per crear likes.")
            return

        for perfil in perfils:
            # Seleccionem un nombre aleatori de likes per a cada perfil
            num_likes = random.randint(0, 50)  # Màxim 5 likes per perfil

            # Obtenim una llista de perfils que poden rebre likes, excloent el perfil mateix
            possibles_likes = [p for p in perfils if p != perfil]

            # Seleccionem aleatòriament els perfils que rebran els likes
            likes_a_donar = random.sample(possibles_likes, min(num_likes, len(possibles_likes)))

            for like in likes_a_donar:
                if like not in perfil.likes.all():
                    perfil.likes.add(like)
                    print(f"{perfil.usuari.username} ha fet like a {like.usuari.username}")

        print("S'han creat els likes amb èxit.")