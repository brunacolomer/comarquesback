import os
import django
import random
from comunitat.models import Usuari, Original, Repte, Copiat, Amistat, Insignia

# Configurar l'entorn Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'el_teu_projecte.settings')
django.setup()
from django.core.management.base import BaseCommand

insignies_data = [
    {"titol": "Petit navegador", "text": "Per haver aconseguit un amic al Garraf", "icona": "https://example.com/icon1.png"},
    {"titol": "Cartòfil expert", "text": "Per haver creat 10 reptes originals", "icona": "https://example.com/icon2.png"},
    {"titol": "Amic viatger", "text": "Per tenir amistats en 5 comarques diferents", "icona": "https://example.com/icon3.png"},
    {"titol": "Explorador nocturn", "text": "Per haver completat un repte després de les 22:00", "icona": "https://example.com/icon4.png"},
    {"titol": "Col·leccionista d'insígnies", "text": "Per obtenir 5 insígnies", "icona": "https://example.com/icon5.png"},
    {"titol": "Fotògraf comarcal", "text": "Per penjar una foto a 3 comarques diferents", "icona": "https://example.com/icon6.png"},
    {"titol": "Mestre dels reptes", "text": "Per completar 20 reptes (originals o copiats)", "icona": "https://example.com/icon7.png"},
    {"titol": "Pioner/a", "text": "Per ser el primer en completar un repte original", "icona": "https://example.com/icon8.png"},
    {"titol": "Amistat estel·lar", "text": "Per tenir 10 amistats", "icona": "https://example.com/icon9.png"},
    {"titol": "Casteller digital", "text": "Per completar reptes en 3 comarques castelleres", "icona": "https://example.com/icon10.png"},
    {"titol": "Nòmada català", "text": "Per completar reptes a totes les vegueries", "icona": "https://example.com/icon11.png"},
    {"titol": "Sense fronteres", "text": "Per tenir amics en almenys 2 vegueries diferents", "icona": "https://example.com/icon12.png"},
    {"titol": "Fidel al territori", "text": "Per completar 3 reptes a la mateixa comarca", "icona": "https://example.com/icon14.png"},
    {"titol": "Enciclopèdia viva", "text": "Per haver escrit descripcions en 5 comarques", "icona": "https://example.com/icon15.png"},
    {"titol": "Travessia matinal", "text": "Per completar un repte abans de les 8:00", "icona": "https://example.com/icon16.png"},
    {"titol": "Mestre cartògraf", "text": "Per completar reptes en 10 comarques diferents", "icona": "https://example.com/icon17.png"},
    {"titol": "Coneixedor local", "text": "Per completar reptes en totes les comarques d'una mateixa vegueria", "icona": "https://example.com/icon18.png"},
    {"titol": "Guia cultural", "text": "Per haver estat copiat en 5 reptes originals", "icona": "https://example.com/icon19.png"},
    {"titol": "Tastador de tradicions", "text": "Per participar en festes locals de 3 comarques diferents", "icona": "https://example.com/icon20.png"},
  {"titol": "Cronista digital", "text": "Per escriure una crònica després de completar un repte", "icona": "https://example.com/icon21.png"},
  {"titol": "Rellotge humà", "text": "Per completar reptes a cada franja del dia (matí, tarda i nit)", "icona": "https://example.com/icon22.png"},
  {"titol": "Aliat del vent", "text": "Per completar un repte en un dia amb fort vent", "icona": "https://example.com/icon23.png"},
  {"titol": "Amic discret", "text": "Per fer 3 amistats sense enviar cap repte", "icona": "https://example.com/icon24.png"},
  {"titol": "Explorador puntual", "text": "Per completar un repte exactament a les 12:00", "icona": "https://example.com/icon25.png"},
  {"titol": "Caçador d'albades", "text": "Per penjar una foto abans de les 7:00", "icona": "https://example.com/icon26.png"},
{"titol": "Convidat sorpresa", "text": "Per completar un repte d'una altra comarca sense conèixer ningú allà", "icona": "https://example.com/icon27.png"},
{"titol": "Orfebre de reptes", "text": "Per editar i millorar 5 reptes propis", "icona": "https://example.com/icon28.png"},
{"titol": "Camí de ronda", "text": "Per completar 3 reptes seguits en comarques costaneres", "icona": "https://example.com/icon29.png"},
{"titol": "Creador de tendències", "text": "Per ser el primer a completar un repte creat per un amic", "icona": "https://example.com/icon30.png"},
    {"titol": "Amic de la natura", "text": "Per completar un repte en un parc natural", "icona": "https://example.com/icon31.png"},
    {"titol": "Creador de reptes", "text": "Per crear 5 reptes originals", "icona": "https://example.com/icon32.png"},
    {"titol": "Explorador urbà", "text": "Per completar un repte a una ciutat desconeguda", "icona": "https://example.com/icon33.png"},
    {"titol": "Amic de la història", "text": "Per completar un repte en un lloc històric", "icona": "https://example.com/icon34.png"},
    {"titol": "Creador de comunitat", "text": "Per tenir 20 amics a la plataforma", "icona": "https://example.com/icon35.png"},
    {"titol": "Explorador de la diversitat", "text": "Per completar reptes en 5 comarques amb cultures diferents", "icona": "https://example.com/icon36.png"},
    {"titol": "Navegant del temps", "text": "Per completar un repte en un dia de pluja", "icona": "https://example.com/icon37.png"},
    {"titol": "Amic de la música", "text": "Per completar un repte en un festival musical", "icona": "https://example.com/icon38.png"},
    {"titol": "Creador de records", "text": "Per penjar una foto a cada comarca", "icona": "https://example.com/icon39.png"},
    {"titol": "Amic de la gastronomia", "text": "Per completar un repte en un restaurant local", "icona": "https://example.com/icon40.png"}

]


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
       for data in insignies_data:
            insignia, created = Insignia.objects.get_or_create(
                titol=data["titol"],
                defaults={
                    "text": data["text"],
                    "icona": data["icona"]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Insígnia creada: {insignia.titol}"))
            else:
                self.stdout.write(self.style.WARNING(f"Ja existia: {insignia.titol}"))