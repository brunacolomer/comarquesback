import random
from django.core.management.base import BaseCommand
from comunitat.models import Usuari, Insignia

class Command(BaseCommand):
    help = "Assigna insígnies aleatòries a alguns usuaris"

    def handle(self, *args, **kwargs):
        usuaris = list(Usuari.objects.all())
        insignies = list(Insignia.objects.all())

        if not usuaris or not insignies:
            print("No hi ha usuaris o insígnies disponibles.")
            return

        for usuari in usuaris:
            # 50% de probabilitat de donar-li insígnies
            if random.random() < 0.5:
                num_insignies = random.randint(1, min(5, len(insignies)))
                seleccionades = random.sample(insignies, num_insignies)
                for ins in seleccionades:
                    usuari.insignies.add(ins)
                print(f"{usuari.username} ha rebut {num_insignies} insígnia/es.")
            else:
                print(f"{usuari.username} no ha rebut cap insígnia.")
