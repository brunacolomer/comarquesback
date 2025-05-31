# comunitat/management/commands/loadmunicipis.py

import csv
import requests
import pandas as pd
import re

from django.core.management.base import BaseCommand
from comunitat.models import Comarca, Poblacio

def neteja_nom(nom):
    if not isinstance(nom, str):
        return ""
    nom = re.sub(r'\(.*?\)', '', nom)     # Elimina (entre parèntesis)
    nom = re.sub(r'\[.*?\]', '', nom)     # Elimina [referències]
    nom = nom.strip()
    return nom.title()

class Command(BaseCommand):
    help = "Importa comarques reals de Catalunya des de la Viquipèdia"

    URL = "https://ca.wikipedia.org/wiki/Comarques_de_Catalunya"

    def handle(self, *args, **kwargs):
        self.stdout.write("Descarregant taules des de la Viquipèdia...")

        # Llegeix totes les taules amb classe 'wikitable'
        tables = pd.read_html(self.URL, attrs={"class": "wikitable"})

        self.stdout.write(f"Trobades {len(tables)} taules. Processant...")

        municipis_afegits = 0
        comarques_cache = {}

        for table in tables:
            # Noms de columnes pot variar, assegurem que les dues claus existeixen
            if "Comarca" in table.columns and "Habitants (2022)" in table.columns:
                for _, row in table.iterrows():
                    if row["Comarca"] == "Catalunya":
                        continue
                    nom_habitants = row["Habitants (2022)"].strip()
                    nom_comarca = row["Comarca"].strip()
                    nom_comarca = neteja_nom(nom_comarca)
                    nom_habitants = int(nom_habitants.replace(".", "").replace(",", ""))
                    print(f"Nom comarca: {nom_comarca} ", nom_habitants)
                    comarca, created = Comarca.objects.get_or_create(
                        nom=nom_comarca,
                        defaults={"habitants": nom_habitants}
                    )
                    if not created:
                        comarca.habitants = nom_habitants  # opcional: actualitza si ja existeix
                        comarca.save()



        self.stdout.write(self.style.SUCCESS(f"Import complet: {municipis_afegits} municipis afegits."))
