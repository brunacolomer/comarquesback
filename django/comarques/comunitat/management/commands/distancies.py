import random
from django.core.management.base import BaseCommand
from comunitat.models import Comarca, Distancia
import pandas as pd
import re
from unidecode import unidecode

import math
from math import radians, cos, sin, sqrt, atan2
def normalitza_nom(nom):
    if not isinstance(nom, str):
        return ""
    nom = nom.strip().lower()
    nom = unidecode(nom)
    # Substitueix apostrof corbat per recte abans de treure l'article
    nom = nom.strip().lower()
    nom = unidecode(nom)
    nom = re.sub(r"^(el|la|els|les|l[’'])\s*", "", nom)
    return nom


# Funció Haversine per calcular distància entre dues coordenades (en km)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radi de la Terra en km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

class Command(BaseCommand):
    help = "Genera distàncies aleatòries entre comarques"
    # Funció per convertir "1° 32' 17,47\"" → 1.538186
    def gms_a_decimal(self, text):
        match = re.match(r"(\d+)°\s*(\d+)'[\s]*(\d+,\d+)", text)
        if not match:
            return None
        graus = int(match.group(1))
        minuts = int(match.group(2))
        segons = float(match.group(3).replace(',', '.'))
        return graus + minuts / 60 + segons / 3600


    # Llegeix el CSV
  

    def handle(self, *args, **options):
        comarques = list(Comarca.objects.all())

        total = 0

        df = pd.read_csv("/home/bruna/Baixades/comdist.csv")
        print(df.columns.tolist())

        df = df.replace(r'\s*,\s*', ',', regex=True)

        # Aplica la conversió a cada columna
        df['long_est'] = df['Extrem oriental'].apply(self.gms_a_decimal)
        df['long_oest'] = df['Extrem occidental'].apply(self.gms_a_decimal)
        df['lat_nord'] = df['Extrem septentrional'].apply(self.gms_a_decimal)
        df['lat_sud'] = df['Extrem meridional'].apply(self.gms_a_decimal)

        # Calcula el punt mig
        
        df['lat_mig'] = (df['lat_nord'] + df['lat_sud']) / 2
        df['long_mig'] = (df['long_est'] + df['long_oest']) / 2

        # Mostra els resultats
        print(df[['Comarca', 'lat_mig', 'long_mig']])
        nom_to_comarca = {
            normalitza_nom(c.nom): c
            for c in Comarca.objects.all()
        }
        print(nom_to_comarca)
        total = 0
        for i in range(len(df)):
            for j in range(len(df)):
              
                row1 = df.iloc[i]
                row2 = df.iloc[j]

                nom1, lat1, lon1 = row1['Comarca'], row1['lat_mig'], row1['long_mig']
                nom2, lat2, lon2 = row2['Comarca'], row2['lat_mig'], row2['long_mig']
                dist_km = haversine(lat1, lon1, lat2, lon2)

                c1 = nom_to_comarca.get(normalitza_nom(nom1))
                #print(c1)
                c2 = nom_to_comarca.get(normalitza_nom(nom2))
                #print(c2)

               

                if c1 and c2:
                                        
                    if not Distancia.objects.filter(comarca1=c2, comarca2=c1).exists():


                     Distancia.objects.get_or_create(
                        comarca1=c1,
                        comarca2=c2,
                        defaults={'distancia': dist_km}
                    )
                    #Distancia.objects.create(origen=c2, desti=c1, km=dist_km)
                    #print(f"Distància entre {c1.nom} i {c2.nom}: {dist_km:.2f} km")
                    #total += 2

        # Mostra els resultats
        # print(df[['Comarca', 'lat_mig', 'long_mig']])


        self.stdout.write(self.style.SUCCESS(f"S'han creat {total} distàncies aleatòries."))
